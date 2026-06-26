#!/usr/bin/env node

/**
 * 🎬 Movie Butler - 观影小管家
 * 杜老师的专属观影助手 - 媒体库管理 + 电影查询 + 个性化推荐
 */

const fs = require('fs');
const path = require('path');

// 加载环境变量
require('dotenv').config({ path: path.join(__dirname, '../../../.env') });

// 配置
const TMDB_API_KEY = process.env.TMDB_API_KEY || 'bd1ba3aa647fbaa7b35e93db5164a53f';
const TMDB_BASE_URL = 'https://api.themoviedb.org/3';
const OMDb_API_KEY = process.env.OMDB_API_KEY || '9e58a5e3'; // OMDb API (IMDb 数据)
const EMBY_URL = process.env.EMBY_URL || 'http://192.168.0.151:8096';
const EMBY_USERNAME = process.env.EMBY_USERNAME || '喜悦影音';
const EMBY_PASSWORD = process.env.EMBY_PASSWORD || '';
const EMBY_API_KEY = process.env.EMBY_OPENCLAW_TOKEN || process.env.EMBY_API_KEY || '';
// 优先使用喜悦影音用户（主要观看账号）
const EMBY_USER_ID = process.env.EMBY_XIYUE_USER_ID || process.env.EMBY_OPENCLAW_USER_ID || process.env.EMBY_USER_ID || 'd088dd5b26514c94806a41c11a510855';
// 只检索这些媒体库（电影、剧集）
const EMBY_MEDIA_TYPES = ['Movie', 'Series'];
const MEMORY_FILE = path.join(__dirname, 'movie-memory.md');

// 工具函数
async function fetchJson(url, options = {}) {
    const headers = { 
        'Content-Type': 'application/json',
        'X-Emby-Token': EMBY_API_KEY,
        'X-Emby-Authorization': 'MediaBrowser Client="MovieButler",Device="PC",DeviceId="1",Version="1.0"',
        ...options.headers 
    };
    const res = await fetch(url, { headers, ...options });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
}

// ==================== TMDB 功能 ====================

async function searchMovie(query) {
    const url = `${TMDB_BASE_URL}/search/movie?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(query)}&language=zh-CN`;
    const data = await fetchJson(url);
    return data.results || [];
}

async function getMovieDetails(movieId) {
    const url = `${TMDB_BASE_URL}/movie/${movieId}?api_key=${TMDB_API_KEY}&language=zh-CN`;
    return await fetchJson(url);
}

async function getMovieCredits(movieId) {
    const url = `${TMDB_BASE_URL}/movie/${movieId}/credits?api_key=${TMDB_API_KEY}&language=zh-CN`;
    return await fetchJson(url);
}

async function getIMDbRating(imdbId) {
    if (!imdbId) return null;
    
    // 尝试多个 OMDb API Key
    const apiKeys = ['9e58a5e3', '23967f54', '79e28a36'];
    
    for (const key of apiKeys) {
        try {
            const url = `https://www.omdbapi.com/?i=${imdbId}&apikey=${key}`;
            const res = await fetch(url);
            const data = await res.json();
            
            if (data.Response === 'True' && data.imdbRating && data.imdbRating !== 'N/A') {
                return {
                    rating: parseFloat(data.imdbRating),
                    votes: data.imdbVotes || 'N/A',
                    id: data.imdbID
                };
            }
        } catch (e) {
            continue;
        }
    }
    
    // 如果 OMDb 失败，返回 null（不显示 IMDb 评分）
    return null;
}

async function getSimilarMovies(movieId) {
    const url = `${TMDB_BASE_URL}/movie/${movieId}/similar?api_key=${TMDB_API_KEY}&language=zh-CN`;
    const data = await fetchJson(url);
    return data.results || [];
}

async function getRecommendationsByGenre(genre, page = 1) {
    const genreMap = {
        '科幻': '878', '动作': '28', '剧情': '18', '喜剧': '35',
        '悬疑': '9648', '恐怖': '27', '爱情': '10749', '动画': '16',
        '冒险': '12', '犯罪': '80', '纪录': '99', '家庭': '10751'
    };
    const genreId = genreMap[genre] || '878';
    const url = `${TMDB_BASE_URL}/discover/movie?api_key=${TMDB_API_KEY}&language=zh-CN&sort_by=popularity.desc&with_genres=${genreId}&page=${page}`;
    const data = await fetchJson(url);
    return data.results || [];
}

// ==================== Emby 功能 ====================

async function getEmbyApiKey() {
    // 如果没有配置 API Key，尝试匿名访问
    if (EMBY_API_KEY) return EMBY_API_KEY;
    return 'anonymous';
}

async function getEmbyMediaFolders() {
    // 获取指定的媒体库（电影、剧集、演唱会）
    const url = `${EMBY_URL}/Library/MediaFolders?api_key=${EMBY_API_KEY}`;
    try {
        const data = await fetchJson(url);
        const folders = data.Items || [];
        console.log('Emby 媒体库:', folders.map(f => `${f.Name} (${f.CollectionType})`).join(', '));
        
        // 只保留电影、剧集、演唱会（按杜老师要求）
        const targetTypes = ['movies', 'tvshows', 'musicvideos'];
        const filtered = folders.filter(f => {
            const collectionType = (f.CollectionType || '').toLowerCase();
            return targetTypes.includes(collectionType);
        });
        
        console.log('目标媒体库:', filtered.map(f => f.Name).join(', '));
        return filtered.map(f => f.Id);
    } catch (e) {
        console.log('获取媒体库列表失败:', e.message);
        return [];
    }
}

async function searchEmbyLibrary(query, includeTypes = 'Movie,Series,MusicVideo', year = null) {
    // 构建查询 URL，支持年份精确匹配
    let url = `${EMBY_URL}/Users/${EMBY_USER_ID}/Items?SearchTerm=${encodeURIComponent(query)}&IncludeItemTypes=${includeTypes}&Limit=20&Recursive=true`;
    
    // 如果指定了年份，精确匹配
    if (year) {
        url += `&Years=${year}`;
    }
    
    try {
        const data = await fetchJson(url);
        return data.Items || [];
    } catch (e) {
        console.log('Emby 查询失败:', e.message);
        return [];
    }
}

async function getEmbyMovies() {
    // 简化查询：全局搜索电影类型
    const url = `${EMBY_URL}/Users/${EMBY_USER_ID}/Items?IncludeItemTypes=Movie&Recursive=true&Limit=200&SortBy=DateCreated&SortOrder=Descending`;
    
    try {
        const data = await fetchJson(url);
        return data.Items || [];
    } catch (e) {
        console.log('Emby 获取列表失败:', e.message);
        return [];
    }
}

async function getEmbyRecentAdditions(limit = 10) {
    const folderIds = await getEmbyMediaFolders();
    let url = `${EMBY_URL}/Users/${EMBY_USER_ID}/Items?IncludeItemTypes=Movie,Series,MusicVideo&Recursive=true&Limit=${limit}&SortBy=DateCreated&SortOrder=Descending`;
    
    if (folderIds.length > 0) {
        url += `&ParentId=${folderIds.join(',')}`;
    }
    
    try {
        const data = await fetchJson(url);
        return data.Items || [];
    } catch (e) {
        return [];
    }
}

async function getEmbyRecentlyPlayed(limit = 10) {
    const url = `${EMBY_URL}/Users/${EMBY_USER_ID}/Items/Resume?Limit=${limit}&MediaTypes=Video,Audio`;
    try {
        const data = await fetchJson(url);
        return data.Items || [];
    } catch (e) {
        return [];
    }
}

async function syncEmbyWatchHistory() {
    // 获取 Emby 观看历史
    const url = `${EMBY_URL}/Users/${EMBY_USER_ID}/Items?Filters=IsPlayed&IncludeItemTypes=Movie&Recursive=true&Limit=50&SortBy=DatePlayed&SortOrder=Descending`;
    
    try {
        const data = await fetchJson(url);
        const watched = data.Items || [];
        
        // 同步到观影记录
        let content = '';
        if (fs.existsSync(MEMORY_FILE)) {
            content = fs.readFileSync(MEMORY_FILE, 'utf8');
        }
        
        // 添加每周观影计划部分（如果没有）
        if (!content.includes('## Emby 观看历史')) {
            content += '\n## Emby 观看历史（自动同步）\n\n*最近观看的电影，按时间排序*\n\n';
        }
        
        const historyList = watched.slice(0, 20).map(item => {
            const playedDate = item.UserData?.LastPlayedDate ? new Date(item.UserData.LastPlayedDate).toISOString().split('T')[0] : '未知';
            const playCount = item.UserData?.PlayCount || 1;
            return `- 《${item.Name}》(${item.ProductionYear || '未知'}) - 观看于 ${playedDate} (共${playCount}次)`;
        }).join('\n');
        
        // 更新文件（简化版，实际应该更智能地合并）
        const today = new Date().toISOString().split('T')[0];
        const syncEntry = `### 同步于 ${today}\n\n${historyList}\n\n`;
        
        const historyIndex = content.indexOf('## Emby 观看历史');
        if (historyIndex >= 0) {
            const nextSection = content.indexOf('##', historyIndex + 10);
            const insertPos = nextSection > 0 ? nextSection : content.length;
            content = content.slice(0, historyIndex) + '## Emby 观看历史（自动同步）\n\n*最近观看的电影，按时间排序*\n\n' + syncEntry + content.slice(insertPos);
        }
        
        fs.writeFileSync(MEMORY_FILE, content);
        return { success: true, count: watched.length };
    } catch (e) {
        console.log('Emby 观看历史同步失败:', e.message);
        return { success: false, error: e.message };
    }
}

async function getEmbyLibraryStats() {
    const movies = await getEmbyMovies();
    const folders = await getEmbyMediaFolders();
    
    // 获取媒体库详细信息
    const folderDetails = await Promise.all(
        folders.map(async id => {
            try {
                const res = await fetchJson(`${EMBY_URL}/Items/${id}?api_key=${EMBY_API_KEY}`);
                return { name: res.Name, type: res.CollectionType };
            } catch (e) {
                return { name: `库${id}`, type: 'unknown' };
            }
        })
    );
    
    return {
        totalMovies: movies.length,
        folders: folderDetails
    };
}

async function getEmbyGenres() {
    const folderIds = await getEmbyMediaFolders();
    let url = `${EMBY_URL}/Genres?IncludeItemTypes=Movie,Series,MusicVideo`;
    
    if (folderIds.length > 0) {
        url += `&ParentId=${folderIds.join(',')}`;
    }
    
    try {
        const data = await fetchJson(url);
        return data.Items || [];
    } catch (e) {
        return [];
    }
}

async function getEmbyMoviesByGenre(genre) {
    const folderIds = await getEmbyMediaFolders();
    let url = `${EMBY_URL}/Users/${EMBY_USER_ID}/Items?IncludeItemTypes=Movie,Series,MusicVideo&Recursive=true&Genres=${encodeURIComponent(genre)}&Limit=50`;
    
    if (folderIds.length > 0) {
        url += `&ParentId=${folderIds.join(',')}`;
    }
    
    try {
        const data = await fetchJson(url);
        return data.Items || [];
    } catch (e) {
        return [];
    }
}

// ==================== 观影记忆管理 ====================

function loadMemory() {
    if (!fs.existsSync(MEMORY_FILE)) {
        return { history: [], preferences: { genres: [], directors: [], avgRating: 0 } };
    }
    
    const content = fs.readFileSync(MEMORY_FILE, 'utf8');
    return { content, raw: content };
}

function saveMemory(entry) {
    const today = new Date().toISOString().split('T')[0];
    let content = '';
    
    if (fs.existsSync(MEMORY_FILE)) {
        content = fs.readFileSync(MEMORY_FILE, 'utf8');
    }
    
    const newEntry = `## ${today}\n\n### 《${entry.title}》\n- **评分**: ${entry.rating}/10\n- **感受**: ${entry.feeling}\n\n`;
    
    fs.writeFileSync(MEMORY_FILE, content + newEntry);
}

function parseMemory() {
    if (!fs.existsSync(MEMORY_FILE)) return { movies: [], totalRating: 0, count: 0, weeklyPicks: [], context: {} };
    
    const content = fs.readFileSync(MEMORY_FILE, 'utf8');
    const movies = [];
    const weeklyPicks = [];
    const lines = content.split('\n');
    
    let currentMovie = null;
    let inWeeklySection = false;
    let inContextSection = false;
    let context = {};
    
    for (const line of lines) {
        if (line.startsWith('## 每周观影')) {
            inWeeklySection = true;
            continue;
        }
        if (line.startsWith('## 背景记录')) {
            inWeeklySection = false;
            inContextSection = true;
            continue;
        }
        if (line.startsWith('### 《') && !inWeeklySection) {
            if (currentMovie && !inWeeklySection) movies.push(currentMovie);
            const title = line.match(/《(.+)》/)?.[1] || '未知';
            currentMovie = { title, rating: 0, feeling: '', date: '' };
        } else if (line.startsWith('#### 第') && inWeeklySection) {
            const weekMatch = line.match(/第 (\d+) 周/);
            const date = line.match(/\((\d{4}-\d{2}-\d{2})\)/)?.[1];
            if (weekMatch) {
                currentMovie = { week: parseInt(weekMatch[1]), date, movie: '', reason: '' };
            }
        } else if (line.startsWith('- **电影**:') && inWeeklySection && currentMovie) {
            currentMovie.movie = line.replace('- **电影**:', '').trim();
        } else if (line.startsWith('- **理由**:') && inWeeklySection && currentMovie) {
            currentMovie.reason = line.replace('- **理由**:', '').trim();
            weeklyPicks.push({...currentMovie});
        } else if (line.includes('**评分**:') && !inWeeklySection && currentMovie) {
            const rating = parseInt(line.match(/(\d+)/)?.[1] || '0');
            if (currentMovie) currentMovie.rating = rating;
        } else if (line.includes('**感受**:') && !inWeeklySection && currentMovie) {
            const feeling = line.replace(/.*\*\*感受\*\*:\s*/, '').trim();
            if (currentMovie) currentMovie.feeling = feeling;
        } else if (line.includes('**心情**:') && inContextSection) {
            context.mood = line.replace(/.*\*\*心情\*\*:\s*/, '').trim();
        } else if (line.includes('**工作**:') && inContextSection) {
            context.work = line.replace(/.*\*\*工作\*\*:\s*/, '').trim();
        } else if (line.includes('**最近关注**:') && inContextSection) {
            context.interests = line.replace(/.*\*\*最近关注\*\*:\s*/, '').trim();
        }
    }
    if (currentMovie && !inWeeklySection && currentMovie.title) movies.push(currentMovie);
    
    const totalRating = movies.reduce((sum, m) => sum + m.rating, 0);
    return { movies, totalRating, count: movies.length, weeklyPicks, context };
}

function saveWeeklyPick(week, date, movie, reason) {
    let content = '';
    if (fs.existsSync(MEMORY_FILE)) {
        content = fs.readFileSync(MEMORY_FILE, 'utf8');
    }
    
    // 检查是否已有每周观影部分
    if (!content.includes('## 每周观影计划')) {
        content += '\n## 每周观影计划\n\n';
    }
    
    const newEntry = `#### 第 ${week} 周 (${date})\n- **电影**: 《${movie}》\n- **理由**: ${reason}\n\n`;
    
    // 插入到每周观影部分
    const weeklyIndex = content.indexOf('## 每周观影计划');
    const nextSection = content.indexOf('##', weeklyIndex + 10);
    const insertPos = nextSection > 0 ? nextSection : content.length;
    
    content = content.slice(0, insertPos) + newEntry + '\n' + content.slice(insertPos);
    fs.writeFileSync(MEMORY_FILE, content);
}

function saveContext(context) {
    let content = '';
    if (fs.existsSync(MEMORY_FILE)) {
        content = fs.readFileSync(MEMORY_FILE, 'utf8');
    }
    
    // 检查是否已有背景记录部分
    if (!content.includes('## 背景记录')) {
        content += '\n## 背景记录\n\n';
    }
    
    const date = new Date().toISOString().split('T')[0];
    let contextSection = `### ${date}\n`;
    if (context.mood) contextSection += `- **心情**: ${context.mood}\n`;
    if (context.work) contextSection += `- **工作**: ${context.work}\n`;
    if (context.interests) contextSection += `- **最近关注**: ${context.interests}\n`;
    contextSection += '\n';
    
    // 插入到背景记录部分
    const contextIndex = content.indexOf('## 背景记录');
    const nextSection = content.indexOf('##', contextIndex + 10);
    const insertPos = nextSection > 0 ? nextSection : content.length;
    
    content = content.slice(0, insertPos) + contextSection + content.slice(insertPos);
    fs.writeFileSync(MEMORY_FILE, content);
}

// ==================== 格式化输出 ====================

async function formatMovieInfo(movie, credits, inEmby, embyItem) {
    const year = movie.release_date?.split('-')[0] || '未知';
    const genres = movie.genres?.map(g => g.name).join('、') || '未知';
    const director = credits?.crew?.find(p => p.job === 'Director')?.name || '未知';
    const cast = credits?.cast?.slice(0, 5).map(a => a.name).join('、') || '未知';
    const runtime = movie.runtime || 0;
    
    // 获取 IMDb 评分（如果可用）
    const imdbId = movie.imdb_id;
    const imdbData = imdbId ? await getIMDbRating(imdbId) : null;
    
    // 如果获取失败，使用 TMDB 的 IMDb 链接
    const imdbLink = imdbId ? `https://www.imdb.com/title/${imdbId}/` : null;
    
    let statusSection = '';
    
    if (inEmby) {
        const quality = embyItem?.MediaSources?.[0]?.Video3DFormat ? '3D' : 
                       embyItem?.MediaSources?.[0]?.VideoRange?.includes('HDR') ? 'HDR' : 'SDR';
        const resolution = embyItem?.Width >= 3840 ? '4K' : embyItem?.Width >= 1920 ? '1080P' : '720P';
        
        // 生成 Emby 播放链接（正确的格式）
        const embyId = embyItem?.Id;
        const serverId = embyItem?.ServerId || '72dc6cc25fad43c68df334b40b5e167a';
        const playUrls = embyId ? {
            // 正确的 Emby 链接格式：#!/item?id=xxx&serverId=xxx
            play: `${EMBY_URL}/web/index.html#!/item?id=${embyId}&serverId=${serverId}`,
            // 备用格式
            details: `${EMBY_URL}/web/index.html#!/details?id=${embyId}&serverId=${serverId}`
        } : { play: EMBY_URL, details: EMBY_URL };
        
        statusSection = `
📊 **服务器状态**: ✅ 已有
🎞️ **画质**: ${resolution} ${quality}
📁 **位置**: ${embyItem?.ContainerPath || '媒体库'}
🔗 **播放链接**: [▶️ 点击播放](${playUrls.play})
`;
    } else {
        const downloadSuggestion = movie.vote_average >= 7.5 ? 
            `💡 **建议**: 这部高分电影（⭐${movie.vote_average.toFixed(1)}）值得收藏！您可以手动下载添加到服务器～` :
            `💡 **建议**: 如果您感兴趣，可以手动下载添加到服务器`;
        
        statusSection = `
📊 **服务器状态**: ❌ 暂无
${downloadSuggestion}
🔍 **下载提示**: 建议搜索 "${movie.title} ${year} 1080P 中字" 或 "4K BluRay"
`;
    }
    
    // 构建评分显示
    let ratingSection = `⭐ **TMDB 评分**: ${movie.vote_average.toFixed(1)}/10 (${movie.vote_count}人评分)\n`;
    if (imdbData) {
        ratingSection += `⭐ **IMDb 评分**: ${imdbData.rating}/10 (${imdbData.votes})\n`;
    } else if (imdbLink) {
        ratingSection += `🔗 **IMDb 链接**: [查看 IMDb](${imdbLink})\n`;
    }
    
    return `
🎬 **《${movie.title}》** (${year})

${ratingSection}🎭 **类型**: ${genres}
🎬 **导演**: ${director}
🌟 **主演**: ${cast}
⏱️ **时长**: ${runtime ? `${runtime}分钟` : '未知'}

📝 **简介**:
${movie.overview || '暂无简介'}

${statusSection}
${movie.poster_path ? `![海报](https://image.tmdb.org/t/p/w500${movie.poster_path})` : ''}
`.trim();
}

function formatEmbyMovieList(movies, prefix = '') {
    if (movies.length === 0) return '没有找到相关电影';
    
    const list = movies.slice(0, 10).map((m, i) => {
        const year = m.ProductionYear || '';
        const rating = m.CommunityRating ? `⭐${m.CommunityRating.toFixed(1)}` : '';
        return `${prefix}${i+1}. 《${m.Name}》${year ? `(${year})` : ''} ${rating}`;
    }).join('\n');
    
    return list + (movies.length > 10 ? `\n... 共${movies.length}部` : '');
}

// ==================== 智能推荐算法 ====================

function getWeekNumber() {
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 1);
    const diff = now - start;
    const oneWeek = 604800000;
    return Math.ceil(diff / oneWeek);
}

function analyzePreferences(memory) {
    const { movies } = memory;
    if (movies.length === 0) return { topGenres: [], topDirectors: [], avgRating: 0, preferredLength: 'any' };
    
    // 统计类型偏好
    const genreCount = {};
    const directorCount = {};
    let totalRating = 0;
    
    movies.forEach(m => {
        totalRating += m.rating;
        if (m.genres) {
            m.genres.forEach(g => {
                genreCount[g] = (genreCount[g] || 0) + 1;
            });
        }
        if (m.director) {
            directorCount[m.director] = (directorCount[m.director] || 0) + 1;
        }
    });
    
    const topGenres = Object.entries(genreCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([g]) => g);
    
    const topDirectors = Object.entries(directorCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([d]) => d);
    
    return {
        topGenres,
        topDirectors,
        avgRating: totalRating / movies.length,
        preferredLength: movies.length > 5 ? 'long' : 'any'
    };
}

async function generateWeeklyRecommendation(embyMovies, memory, context = {}) {
    const { weeklyPicks, movies: watchedMovies } = memory;
    const prefs = analyzePreferences(memory);
    
    // 获取本周
    const weekNum = getWeekNumber();
    const date = new Date().toISOString().split('T')[0];
    
    // 检查是否已有本周推荐
    const existingPick = weeklyPicks.find(p => p.week === weekNum);
    if (existingPick) {
        return `📅 **第 ${weekNum} 周推荐已生成**\n\n🎬 电影：《${existingPick.movie}》\n💡 理由：${existingPick.reason}`;
    }
    
    // 过滤已观看的
    const watchedTitles = new Set(watchedMovies.map(m => m.title?.toLowerCase()));
    const unwatched = embyMovies.filter(m => !watchedTitles.has(m.Name?.toLowerCase()));
    
    if (unwatched.length === 0) {
        return '🎉 Emby 上的电影您都看完啦！需要添加新片源～';
    }
    
    // 智能评分算法
    const scored = unwatched.map(movie => {
        let score = 0;
        const reasons = [];
        
        // 基础评分（Emby 评分）
        const embyRating = movie.CommunityRating || 0;
        score += embyRating * 10;
        if (embyRating >= 8.0) {
            reasons.push(`高分佳作 (⭐${embyRating.toFixed(1)})`);
        }
        
        // 类型匹配
        const movieGenres = movie.GenreItems?.map(g => g.Name) || [];
        const genreMatch = movieGenres.some(g => prefs.topGenres.includes(g));
        if (genreMatch) {
            score += 30;
            const matched = prefs.topGenres.filter(g => movieGenres.includes(g));
            if (matched.length > 0) {
                reasons.push(`您喜欢的${matched.join('/')}类型`);
            }
        }
        
        // 导演匹配
        const director = movie.People?.find(p => p.Type === 'Director')?.Name;
        if (director && prefs.topDirectors.includes(director)) {
            score += 40;
            reasons.push(`钟爱的导演：${director}`);
        }
        
        // 时长考虑（周末适合看长的）
        const runtime = movie.RunTimeTicks ? Math.floor(movie.RunTimeTicks / 600000000) : 0;
        const isWeekend = new Date().getDay() >= 5;
        if (isWeekend && runtime > 150) {
            score += 15;
            reasons.push('周末适合沉浸式观影');
        } else if (!isWeekend && runtime < 120) {
            score += 10;
            reasons.push('工作日轻松观影');
        }
        
        // 最近添加的优先
        if (movie.DateCreated) {
            const createdDate = new Date(movie.DateCreated);
            const daysSinceAdded = (Date.now() - createdDate) / (1000 * 60 * 60 * 24);
            if (daysSinceAdded < 7) {
                score += 20;
                reasons.push('新片推荐');
            }
        }
        
        // 上下文匹配（如果有）
        if (context.mood) {
            const moodMap = {
                '累': ['喜剧', '动画', '家庭'],
                '开心': ['动作', '冒险', '科幻'],
                '思考': ['剧情', '悬疑', '纪录'],
                '放松': ['喜剧', '爱情', '家庭']
            };
            const moodGenres = moodMap[context.mood] || [];
            const moodMatch = movieGenres.some(g => moodGenres.includes(g));
            if (moodMatch) {
                score += 25;
                reasons.push(`适合${context.mood}的时候看`);
            }
        }
        
        if (context.work && context.work.includes('忙')) {
            score += 15;
            reasons.push('忙碌一周，值得犒劳自己');
        }
        
        return { movie, score, reasons: reasons.slice(0, 3) };
    });
    
    // 排序并获取最佳推荐
    scored.sort((a, b) => b.score - a.score);
    const top3 = scored.slice(0, 3);
    
    if (top3.length === 0) {
        return '暂时没有找到合适的推荐';
    }
    
    const best = top3[0];
    const year = best.movie.ProductionYear || '';
    const genres = best.movie.GenreItems?.map(g => g.Name).join('、') || '';
    const runtime = best.movie.RunTimeTicks ? Math.floor(best.movie.RunTimeTicks / 600000000) : 0;
    const director = best.movie.People?.find(p => p.Type === 'Director')?.Name || '';
    
    // 生成推荐理由
    const reasonText = best.reasons.length > 0 ? best.reasons.join('；') : '综合评分最高';
    
    // 保存推荐
    saveWeeklyPick(weekNum, date, best.movie.Name, reasonText);
    
    return `
🎬 **第 ${weekNum} 周 · 每周一部电影**

## 本周推荐

### 《${best.movie.Name}》${year ? `(${year})` : ''}

⭐ **评分**: ${best.movie.CommunityRating?.toFixed(1) || 'N/A'}/10
🎭 **类型**: ${genres}
🎬 **导演**: ${director}
⏱️ **时长**: ${runtime ? `${runtime}分钟` : '未知'}

💡 **推荐理由**:
${reasonText}

---

## 备选方案

${top3.slice(1, 3).map((r, i) => {
    const rYear = r.movie.ProductionYear || '';
    const rRating = r.movie.CommunityRating?.toFixed(1) || 'N/A';
    return `${i+2}. 《${r.movie.Name}》${rYear ? `(${rYear})` : ''} ⭐${rRating}`;
}).join('\n')}

---
*小暖阳：看完记得告诉我感受哦～ 我会记录您的喜好，下次推荐更精准！* 🍿
`.trim();
}

// ==================== 主函数 ====================

async function movieButler(command, context = {}) {
    const cmd = command.toLowerCase();
    
    // ========== 查询电影信息（全网 + 服务器） ==========
    if (cmd.includes('查询') || cmd.includes('搜索') || cmd.includes('介绍') || cmd.includes('详情')) {
        const match = command.match(/[""]([^"""]+)[""]|《([^》]+)》/);
        const query = match ? (match[1] || match[2]) : command.replace(/查询 | 搜索 | 介绍 | 详情/g, '').trim();
        
        // 提取年份（如果有）
        const yearMatch = command.match(/(\d{4})/);
        const year = yearMatch ? yearMatch[1] : null;
        
        if (!query) return '请告诉我电影名字，例如："查询《肖申克的救赎》"';
        
        // 先查 TMDB 获取准确信息
        const tmdbResults = await searchMovie(query);
        
        if (tmdbResults.length === 0) {
            // TMDB 没找到，只查 Emby
            const embyResults = await searchEmbyLibrary(query, 'Movie,Series', year);
            if (embyResults.length > 0) {
                const first = embyResults[0];
                return `📺 **服务器查询结果**\n\n✅ Emby 服务器上有"${first.Name}" (${first.ProductionYear || '未知'})\n\n🌐 **全网查询**\n\n❌ TMDB 未找到详细信息`;
            }
            return `没有找到关于"${query}"的电影信息`;
        }
        
        // 获取 TMDB 结果的年份
        const tmdbYear = year || tmdbResults[0].release_date?.split('-')[0];
        
        // 用年份精确查询 Emby
        const embyResults = await searchEmbyLibrary(query, 'Movie,Series', tmdbYear);
        const inEmby = embyResults.length > 0;
        const embyItem = embyResults[0];
        
        // TMDB 查询结果处理
        if (tmdbResults.length === 0) {
            if (inEmby) {
                return `📺 **服务器查询结果**\n\n✅ Emby 服务器上有"${query}"\n\n🌐 **全网查询**\n\n❌ TMDB 未找到详细信息（可能是冷门影片）`;
            }
            return `没有找到关于"${query}"的电影信息`;
        }
        
        // 获取详细信息
        const movie = tmdbResults[0];
        const [details, credits] = await Promise.all([
            getMovieDetails(movie.id),
            getMovieCredits(movie.id)
        ]);
        
        // 格式化输出（包含全网信息 + 服务器状态 + 下载建议 + IMDb 评分）
        return await formatMovieInfo(details, credits, inEmby, embyItem);
    }
    
    // ========== Emby 相关查询 ==========
    
    // Emby 媒体库统计
    if (cmd.includes('多少') || cmd.includes('统计') || cmd.includes('数量')) {
        const movies = await getEmbyMovies();
        return `📊 **Emby 媒体库统计**\n\n🎬 电影数量：${movies.length} 部\n\n*仅统计「电影」和「剧集」媒体库*`;
    }
    
    // Emby 上有 XXX 吗
    if (cmd.includes('emby') && (cmd.includes('有') || cmd.includes('吗'))) {
        const match = command.match(/[""]([^"""]+)[""]|《([^》]+)》/);
        const query = match ? (match[1] || match[2]) : command.replace(/emby 有 | 吗 | 上/g, '').trim();
        
        const results = await searchEmbyLibrary(query);
        if (results.length > 0) {
            const years = results.map(r => r.ProductionYear).filter(Boolean).join(', ');
            return `✅ Emby 服务器上有"${query}"，共找到 ${results.length} 部相关影片 ${years ? `(${years})` : ''}`;
        }
        return `❌ Emby 服务器上没有"${query}"`;
    }
    
    // Emby 有哪些电影 / 媒体库统计
    if (cmd.includes('emby') && (cmd.includes('哪些') || cmd.includes('多少') || cmd.includes('统计'))) {
        const stats = await getEmbyLibraryStats();
        return `📊 **Emby 媒体库统计**\n\n🎬 总电影数：${stats.totalMovies} 部\n\n📁 媒体库：${stats.folders.map(f => f.name).join(', ') || '默认'}`;
    }
    
    // Emby 最近添加
    if (cmd.includes('最近添加') || cmd.includes('新片')) {
        const recent = await getEmbyRecentAdditions(10);
        if (recent.length === 0) return '最近没有添加新电影';
        
        const list = recent.map((m, i) => `${i+1}. 《${m.Name}》${m.ProductionYear ? `(${m.ProductionYear})` : ''}`).join('\n');
        return `🆕 **最近添加的电影**\n\n${list}`;
    }
    
    // Emby 最近播放
    if (cmd.includes('最近播放') || cmd.includes('观看历史')) {
        const recent = await getEmbyRecentlyPlayed(10);
        if (recent.length === 0) return '最近没有观看记录';
        
        const list = recent.map((m, i) => `${i+1}. 《${m.Name}》${m.ProductionYear ? `(${m.ProductionYear})` : ''}`).join('\n');
        return `📺 **最近播放**\n\n${list}`;
    }
    
    // Emby 按类型查询
    if (cmd.includes('emby') && cmd.includes('科幻') || cmd.includes('emby') && cmd.includes('动作') || cmd.includes('emby') && cmd.includes('剧情')) {
        const genreMatch = command.match(/科幻 | 动作 | 剧情 | 喜剧 | 悬疑 | 恐怖 | 爱情 | 动画 | 冒险 | 犯罪/);
        const genre = genreMatch ? genreMatch[0] : '科幻';
        
        const movies = await getEmbyMoviesByGenre(genre);
        return `🎬 **Emby 上的${genre}电影**\n\n${formatEmbyMovieList(movies)}`;
    }
    
    // ========== 观影记录 ==========
    if (cmd.includes('看了') || cmd.includes('评分') || cmd.includes('感受')) {
        const match = command.match(/[""]([^"""]+)[""]|《([^》]+)》/);
        const title = match ? (match[1] || match[2]) : '未知电影';
        const ratingMatch = command.match(/(\d+)[分\/](\d+)|评分 [：:]\s*(\d+)/);
        const rating = parseInt(ratingMatch?.[1] || ratingMatch?.[3] || '0');
        const feeling = command.replace(/看了 | 评分 | 感受/g, '').replace(/[《》""]/g, '').trim();
        
        saveMemory({ title, rating, feeling });
        return `📝 已记录您对《${title}》的观影感受！评分：${rating}/10`;
    }
    
    // 观影统计报告
    if (cmd.includes('统计') || cmd.includes('报告') || cmd.includes('总结')) {
        const { movies } = parseMemory();
        
        if (movies.length === 0) {
            // 尝试从 Emby 同步
            const syncResult = await syncEmbyWatchHistory();
            if (syncResult.success) {
                return `📊 **观影统计报告**\n\n已从 Emby 同步 ${syncResult.count} 部观看记录，请再次查询统计～`;
            }
            return '还没有观影记录，看完电影记得告诉我感受哦～';
        }
        
        // 统计分析
        const avgRating = (movies.reduce((sum, m) => sum + m.rating, 0) / movies.length).toFixed(1);
        const maxRating = Math.max(...movies.map(m => m.rating));
        const minRating = Math.min(...movies.map(m => m.rating));
        
        // 类型统计（需要从 TMDB 获取，简化版手动统计）
        const genreCount = {};
        movies.forEach(m => {
            if (m.genres) {
                m.genres.forEach(g => {
                    genreCount[g] = (genreCount[g] || 0) + 1;
                });
            }
        });
        
        const topGenres = Object.entries(genreCount)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([g, c]) => `${g} (${c}部)`)
            .join(', ');
        
        // 最高评分电影
        const bestMovie = movies.find(m => m.rating === maxRating);
        
        return `
📊 **观影统计报告**

**总体数据**
🎬 已观影：${movies.length} 部
⭐ 平均评分：${avgRating}/10
🏆 最高评分：${maxRating}/10《${bestMovie?.title}》
📉 最低评分：${minRating}/10

**类型偏好**
${topGenres || '暂无数据'}

**最近观看**
${movies.slice(-5).reverse().map((m, i) => `${i+1}. 《${m.title}》⭐${m.rating}/10`).join('\n')}

---
*小暖阳：继续记录，我会更懂您的喜好！*
`.trim();
    }
    
    // 查看观影历史
    if (cmd.includes('观影记录') || cmd.includes('看过哪些') || cmd.includes('观影历史')) {
        const { movies } = parseMemory();
        if (movies.length === 0) return '还没有观影记录，看完电影记得告诉我感受哦～';
        
        const list = movies.slice(-10).map((m, i) => `${i+1}. 《${m.title}》⭐${m.rating}/10`).join('\n');
        return `📝 **观影记录**（最近 10 部）\n\n${list}\n\n共记录 ${movies.length} 部电影`;
    }
    
    // ========== 每周观影推荐 ==========
    if (cmd.includes('每周') || cmd.includes('本周') || cmd.includes('周推荐')) {
        const embyMovies = await getEmbyMovies();
        const memory = parseMemory();
        
        // 分析上下文（从命令中提取）
        const context = {};
        if (cmd.includes('累') || cmd.includes('忙')) context.mood = '累';
        if (cmd.includes('开心') || cmd.includes('高兴')) context.mood = '开心';
        if (cmd.includes('周末')) context.isWeekend = true;
        
        return await generateWeeklyRecommendation(embyMovies, memory, context);
    }
    
    // 记录背景信息
    if (cmd.includes('心情') || cmd.includes('工作') || cmd.includes('最近')) {
        const context = {};
        if (cmd.includes('心情')) {
            context.mood = command.replace(/.*心情 [是：:]\s*/, '').trim();
        }
        if (cmd.includes('工作')) {
            context.work = command.replace(/.*工作 [是：:]\s*/, '').trim();
        }
        if (cmd.includes('最近')) {
            context.interests = command.replace(/.*最近 [在：:]\s*/, '').trim();
        }
        saveContext(context);
        return '📝 已记录您的近况，推荐会更精准哦～';
    }
    
    // ========== 推荐功能 ==========
    if (cmd.includes('推荐')) {
        // 优先推荐 Emby 上有的
        if (cmd.includes('emby') || cmd.includes('服务器')) {
            const embyMovies = await getEmbyMovies();
            const { movies: watched } = parseMemory();
            const watchedTitles = new Set(watched.map(m => m.title.toLowerCase()));
            
            // 过滤没看过的
            const unwatched = embyMovies.filter(m => !watchedTitles.has(m.Name?.toLowerCase()));
            
            if (unwatched.length === 0) return 'Emby 上的电影您都看过啦！';
            
            // 按评分排序
            unwatched.sort((a, b) => (b.CommunityRating || 0) - (a.CommunityRating || 0));
            
            const list = unwatched.slice(0, 10).map((m, i) => 
                `${i+1}. 《${m.Name}》${m.ProductionYear ? `(${m.ProductionYear})` : ''} ⭐${m.CommunityRating?.toFixed(1) || 'N/A'}`
            ).join('\n');
            
            return `💡 **Emby 上您还没看过的高分电影**\n\n${list}`;
        }
        
        // 根据类型推荐
        const genreMatch = command.match(/科幻 | 动作 | 剧情 | 喜剧 | 悬疑 | 恐怖 | 爱情 | 动画 | 冒险 | 犯罪/);
        const genre = genreMatch ? genreMatch[0] : '科幻';
        
        const movies = await getRecommendationsByGenre(genre);
        if (movies.length === 0) return '暂时没有找到推荐';
        
        const list = movies.slice(0, 10).map((m, i) => 
            `${i+1}. 《${m.title}》(${m.release_date?.split('-')[0]}) ⭐${m.vote_average.toFixed(1)}`
        ).join('\n');
        
        return `💡 **为您推荐${genre}电影**\n\n${list}`;
    }
    
    // ========== 批量查询/推荐 ==========
    
    // 批量推荐（"推荐 10 部科幻电影"）
    const batchMatch = command.match(/推荐\s*(\d+)\s*部\s*(.*)/);
    if (batchMatch) {
        const count = Math.min(parseInt(batchMatch[1]), 20);
        const genre = batchMatch[2].trim() || '科幻';
        
        const movies = await getRecommendationsByGenre(genre, 1);
        const list = movies.slice(0, count).map((m, i) => 
            `${i+1}. 《${m.title}》(${m.release_date?.split('-')[0]}) ⭐${m.vote_average.toFixed(1)}`
        ).join('\n');
        
        return `💡 **为您推荐${count}部${genre}电影**\n\n${list}`;
    }
    
    // ========== 演员/导演专题 ==========
    
    // 演员作品查询（"李连杰的所有作品"）
    if (cmd.includes('作品') || cmd.includes('电影')) {
        const actorMatch = command.match(/(.*)的 (?:所有 | 全部)?(?:作品 | 电影)/);
        if (actorMatch) {
            const personName = actorMatch[1].trim();
            const tmdbResults = await searchMovie(''); // 先搜索人物
            
            // 搜索人物
            const personUrl = `${TMDB_BASE_URL}/search/person?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(personName)}&language=zh-CN`;
            const personData = await fetchJson(personUrl);
            
            if (personData.results && personData.results.length > 0) {
                const personId = personData.results[0].id;
                const creditsUrl = `${TMDB_BASE_URL}/person/${personId}/movie_credits?api_key=${TMDB_API_KEY}&language=zh-CN`;
                const credits = await fetchJson(creditsUrl);
                
                const movies = credits.cast.sort((a, b) => new Date(b.release_date) - new Date(a.release_date)).slice(0, 15);
                const list = movies.map((m, i) => 
                    `${i+1}. 《${m.title}》(${m.release_date?.split('-')[0] || '未知'}) ⭐${m.vote_average?.toFixed(1) || 'N/A'}`
                ).join('\n');
                
                return `🎬 **${personName} 作品列表**（最近 15 部）\n\n${list}`;
            }
            
            return `没有找到"${personName}"的相关信息`;
        }
    }
    
    // 导演作品查询（"诺兰导演的电影"）
    if (cmd.includes('导演')) {
        const directorMatch = command.match(/(.*)导演 (?:的)?(?:电影 | 作品)?/);
        if (directorMatch) {
            const directorName = directorMatch[1].trim();
            
            // 搜索导演（通过电影搜索间接获取）
            const searchUrl = `${TMDB_BASE_URL}/search/movie?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(directorName)}&language=zh-CN&include_adult=false`;
            const searchData = await fetchJson(searchUrl);
            
            if (searchData.results && searchData.results.length > 0) {
                // 获取第一部电影的导演信息
                const firstMovie = searchData.results[0];
                const creditsUrl = `${TMDB_BASE_URL}/movie/${firstMovie.id}/credits?api_key=${TMDB_API_KEY}`;
                const credits = await fetchJson(creditsUrl);
                
                // 找到匹配的导演
                const director = credits.crew.find(p => p.job === 'Director' && p.name.includes(directorName));
                
                if (director) {
                    const personUrl = `${TMDB_BASE_URL}/person/${director.id}/movie_credits?api_key=${TMDB_API_KEY}&language=zh-CN`;
                    const personCredits = await fetchJson(personUrl);
                    
                    const movies = personCredits.cast.sort((a, b) => new Date(b.release_date) - new Date(a.release_date)).slice(0, 15);
                    const list = movies.map((m, i) => 
                        `${i+1}. 《${m.title}》(${m.release_date?.split('-')[0] || '未知'}) ⭐${m.vote_average?.toFixed(1) || 'N/A'}`
                    ).join('\n');
                    
                    return `🎬 **${directorName} 导演作品**（最近 15 部）\n\n${list}`;
                }
            }
            
            return `没有找到"${directorName}"导演的作品信息`;
        }
    }
    
    // 类似电影推荐
    if (cmd.includes('类似') || cmd.includes('同类型')) {
        const match = command.match(/[""]([^"""]+)[""]|《([^》]+)》/);
        const query = match ? (match[1] || match[2]) : '';
        
        if (!query) return '请告诉我哪部电影，例如："推荐类似《星际穿越》的电影"';
        
        const results = await searchMovie(query);
        if (results.length === 0) return `没有找到"${query}"`;
        
        const similar = await getSimilarMovies(results[0].id);
        if (similar.length === 0) return '没有找到类似电影';
        
        const list = similar.slice(0, 10).map((m, i) => 
            `${i+1}. 《${m.title}》(${m.release_date?.split('-')[0]}) ⭐${m.vote_average.toFixed(1)}`
        ).join('\n');
        
        return `💡 **类似《${query}》的电影**\n\n${list}`;
    }
    
    // ========== 高级功能 ==========
    
    // 家庭电影之夜推荐
    if (cmd.includes('家庭') || cmd.includes('一起看') || cmd.includes('全家')) {
        const embyMovies = await getEmbyMovies();
        
        // 筛选适合全家观看的（动画、家庭、冒险类型，评分>7）
        const familyFriendly = embyMovies.filter(m => {
            const genres = (m.GenreItems || []).map(g => g.Name.toLowerCase());
            const rating = m.CommunityRating || 0;
            return (genres.some(g => ['animation', 'family', 'adventure'].includes(g)) && rating >= 7.0);
        }).slice(0, 10);
        
        if (familyFriendly.length === 0) {
            return '💡 **家庭电影之夜推荐**\n\n服务器上适合全家观看的电影不多，建议添加一些动画片或家庭喜剧～';
        }
        
        const list = familyFriendly.map((m, i) => 
            `${i+1}. 《${m.Name}》(${m.ProductionYear || '未知'}) ⭐${m.CommunityRating?.toFixed(1) || 'N/A'}`
        ).join('\n');
        
        return `
👨‍👩‍👦 **家庭电影之夜推荐**

适合全家一起观看的电影：

${list}

---
*小暖阳：记得准备爆米花哦！* 🍿
`.trim();
    }
    
    // 相似影片推荐（基于 Emby 已有）
    if (cmd.includes('相似') && cmd.includes('推荐')) {
        const match = command.match(/类似 | 相似.*《(.+ )》/);
        if (match) {
            const movieName = match[1];
            // 先查 TMDB 获取相似影片
            const tmdbResults = await searchMovie(movieName);
            if (tmdbResults.length > 0) {
                const similar = await getSimilarMovies(tmdbResults[0].id);
                const list = similar.slice(0, 10).map((m, i) => 
                    `${i+1}. 《${m.title}》(${m.release_date?.split('-')[0]}) ⭐${m.vote_average.toFixed(1)}`
                ).join('\n');
                
                return `💡 **类似《${movieName}》的电影**\n\n${list}`;
            }
        }
    }
    
    // 新片提醒（最近添加的电影）
    if (cmd.includes('新片') || cmd.includes('最近添加') || cmd.includes('新添加')) {
        const recent = await getEmbyRecentAdditions(10);
        if (recent.length === 0) return '最近没有添加新电影';
        
        const list = recent.map((m, i) => 
            `${i+1}. 《${m.Name}》(${m.ProductionYear || '未知'}) ${m.CommunityRating ? `⭐${m.CommunityRating.toFixed(1)}` : ''}`
        ).join('\n');
        
        return `🆕 **最近添加的电影**\n\n${list}`;
    }
    
    // 同步 Emby 观看历史
    if (cmd.includes('同步') && (cmd.includes('emby') || cmd.includes('观看') || cmd.includes('历史'))) {
        const syncResult = await syncEmbyWatchHistory();
        if (syncResult.success) {
            return `✅ 已从 Emby 同步 ${syncResult.count} 部观看记录！`;
        }
        return `❌ 同步失败：${syncResult.error}`;
    }
    
    // ========== 默认帮助 ==========
    return `
🎬 **观影小管家** 为您服务！

**电影查询**
🔍 查询《肖申克的救赎》- 获取电影详情
🔍 《星际穿越》的详细信息

**Emby 媒体库**
📺 Emby 有哪些科幻电影？
📺 Emby 有《盗梦空间》吗？
📺 我的服务器有多少部电影？
📺 最近添加了什么电影？
📺 最近播放了什么？

**观影记录**
📝 看了《XXX》，很震撼，评分 9 分
📝 我的观影记录

**🎯 每周一部电影**
📅 本周推荐什么电影？
📅 这周有什么好电影推荐
📅 周末了，推荐部电影
📅 最近工作很累，推荐部轻松的

**背景记录**（让推荐更精准）
💭 今天心情很好
💭 最近工作很忙
💭 最近对科幻题材感兴趣

**个性化推荐**
💡 推荐科幻电影
💡 推荐类似《星际穿越》的电影
💡 Emby 上有什么高分电影推荐？

请告诉我您的需求～
`.trim();
}

// CLI 执行
if (require.main === module) {
    const args = process.argv.slice(2).join(' ');
    movieButler(args).then(console.log).catch(console.error);
}

module.exports = { movieButler, searchMovie, getMovieDetails, searchEmbyLibrary, getEmbyMovies, getEmbyRecentAdditions };
