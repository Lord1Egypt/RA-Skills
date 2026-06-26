const http = require('http');
const { execFile } = require('child_process');
const os = require('os');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');

// 读取配置文件（与 CLI 同级目录的 config.json）
const configPath = path.join(__dirname, 'config.json');
let CONFIG = { host: '127.0.0.1', port: 23330 };
try {
  const configData = fs.readFileSync(configPath, 'utf-8');
  CONFIG = JSON.parse(configData);
} catch (err) {
  // 配置文件不存在或解析失败，使用默认值
}

// 检查是否本机模式
function isLocalHost() {
  const h = (CONFIG.host || '').toLowerCase();
  return h === '127.0.0.1' || h === 'localhost';
}

function checkLocal() {
  if (!isLocalHost()) {
    console.log('❌ 非本地无法调用该功能');
    process.exit(1);
  }
}

// HTTP 请求封装
function request(path) {
  return new Promise((resolve, reject) => {
    const req = http.get(`http://${CONFIG.host}:${CONFIG.port}${path}`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve(data);
        }
      });
    });

    req.on('error', reject);
    req.setTimeout(5000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
  });
}

// 格式化时间
function formatTime(seconds) {
  if (!seconds || isNaN(seconds)) return '0:00';
  const totalSeconds = Math.floor(seconds);
  const minutes = Math.floor(totalSeconds / 60);
  const secs = totalSeconds % 60;
  return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

// 格式化状态输出
function formatStatus(data) {
  if (!data || !data.name) {
    return '⏹️  未在播放';
  }

  const progress = data.progress || 0;
  const duration = data.duration || 0;
  const status = data.status === 'playing' ? '▶️' : '⏸️';
  const volume = data.volume !== undefined ? `${data.volume}%` : '未知';
  const mute = data.mute ? ' (已静音)' : '';
  const collect = data.collect === true ? '❤️ 已收藏' : (data.collect === false ? '🤍 未收藏' : '');

  return `${status}  ${data.name}${data.singer ? ` - ${data.singer}` : ''}
   歌手: ${data.singer || '未知'}
   专辑: ${data.albumName || '未知'}
   进度: ${formatTime(progress)} / ${formatTime(duration)}
   音量: ${volume}${mute}${collect ? '\n   收藏: ' + collect : ''}
   歌词: ${data.lyricLineText || '无'}`;
}

// 唤起 Scheme URL（跨平台）
// 安全白名单：仅允许 lxmusic:// 协议
const ALLOWED_SCHEMES = ['lxmusic:'];
function openSchemeUrl(url) {
  // 验证 URL scheme 白名单
  try {
    const scheme = new URL(url).protocol;
    if (!ALLOWED_SCHEMES.includes(scheme)) {
      return Promise.reject(new Error(`Blocked scheme: ${scheme}. Allowed: ${ALLOWED_SCHEMES.join(', ')}`));
    }
  } catch (e) {
    return Promise.reject(new Error(`Invalid URL: ${url}`));
  }

  return new Promise((resolve, reject) => {
    const platform = os.platform();
    let cmd, args;

    if (platform === 'win32') {
      cmd = 'cmd';
      args = ['/c', 'start', '', url];
    } else if (platform === 'darwin') {
      cmd = 'open';
      args = ['-g', url];
    } else {
      cmd = 'xdg-open';
      args = [url];
    }

    // execFile: 不经过 shell 解释，参数逐个传递，防止注入
    execFile(cmd, args, { timeout: 5000 }, (err) => {
      if (err && err.code !== null) reject(err);
      else resolve();
    });
  });
}

// API 封装
const api = {
  status: () => request('/status?filter=status,name,singer,albumName,lyricLineText,duration,progress,playbackRate,volume,mute,collect'),
  play: () => request('/play'),
  pause: () => request('/pause'),
  next: () => request('/skip-next'),
  prev: () => request('/skip-prev'),
  seek: (offset) => request(`/seek?offset=${offset}`),
  volume: (vol) => request(`/volume?volume=${vol}`),
  mute: (mute) => request(`/mute?mute=${mute}`),
  collect: () => request('/collect'),
  uncollect: () => request('/uncollect'),
};

// ============ SQLite 歌单查询 ============
const SOURCE_NAMES = { kw: '酷我', kg: '酷狗', tx: 'QQ', wy: '网易云', mg: '咪咕' };

function getLxDataDbPath() {
  const platform = os.platform();
  let base;
  if (platform === 'win32') {
    base = process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming');
  } else if (platform === 'darwin') {
    base = path.join(os.homedir(), 'Library', 'Application Support');
  } else {
    base = process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config');
  }
  return path.join(base, 'lx-music-desktop', 'LxDatas', 'lx.data.db');
}

function queryPlaylists(dbPath) {
  if (!fs.existsSync(dbPath)) {
    console.log(`❌ 数据库不存在: ${dbPath}`);
    process.exit(1);
  }
  // 用 Python 查询 SQLite（Node.js 内置无 SQLite 支持）
  const scriptPath = path.join(__dirname, 'list.py');
  if (!fs.existsSync(scriptPath)) {
    console.log(`❌ 脚本不存在: ${scriptPath}`);
    process.exit(1);
  }
  try {
    const result = execSync(`python "${scriptPath}" --db "${dbPath}"`, { encoding: 'utf-8', timeout: 10000 });
    return JSON.parse(result);
  } catch (err) {
    console.log(`❌ 查询失败: ${err.message}`);
    process.exit(1);
  }
}

function queryPlaylistSongs(dbPath, listId) {
  if (!fs.existsSync(dbPath)) {
    console.log(`❌ 数据库不存在: ${dbPath}`);
    process.exit(1);
  }
  const scriptPath = path.join(__dirname, 'list.py');
  if (!fs.existsSync(scriptPath)) {
    console.log(`❌ 脚本不存在: ${scriptPath}`);
    process.exit(1);
  }
  try {
    const result = execSync(`python "${scriptPath}" songs "${listId}" --db "${dbPath}"`, { encoding: 'utf-8', timeout: 10000 });
    return JSON.parse(result);
  } catch (err) {
    console.log(`❌ 查询失败: ${err.message}`);
    process.exit(1);
  }
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  // 智能参数获取：支持带空格的歌名/关键词
  // 从指定位置开始合并所有剩余参数
  function getArgsFrom(index) {
    return args.slice(index).join(' ');
  }

  if (!command) {
    console.log('用法: node lx-music-cli.js <命令> [参数]');
    console.log('');
    console.log('命令:');
    console.log('  search <关键词> [源]     搜索歌曲（本机）');
    console.log('  searchPlay <歌名> [歌手] 搜索并播放（本机）');
    console.log('  play                    播放');
    console.log('  pause                   暂停');
    console.log('  toggle                  切换播放/暂停（本机）');
    console.log('  next                    下一首');
    console.log('  prev                    上一首');
    console.log('  seek <偏移量(秒)>       调整播放进度');
    console.log('  status                  播放状态');
    console.log('  now                     当前歌曲');
    console.log('  lyric                   歌词');
    console.log('  volume <0-100>          设置音量');
    console.log('  mute                    静音');
    console.log('  unmute                  取消静音');
    console.log('  list                    列出本地歌单');
    console.log('  listsongs <歌单ID>      查看歌单中的歌曲');
    console.log('  listplay <歌单ID>       播放本地歌单（本机）');
    console.log('  openlist <源> <歌单ID>   打开歌单（本机）');
    console.log('  playlist <源> <歌单ID> [起始序号] 播放歌单（本机）');
    console.log('  collect                 收藏');
    console.log('  uncollect               取消收藏');
    console.log('  dislike                 不喜欢（本机）');
    process.exit(1);
  }

  try {
    switch (command) {
      case 'search': {
        checkLocal();
        let keyword = getArgsFrom(1);
        let source = '';
        
        // 如果参数超过1个且最后一个是源（2个字母），分离出来
        const parts = keyword.split(' ');
        const validSources = ['kw', 'kg', 'tx', 'wy', 'mg'];
        if (parts.length > 1 && validSources.includes(parts[parts.length - 1])) {
          source = parts.pop();
          keyword = parts.join(' ');
        }
        
        if (!keyword) {
          console.log('❌ 用法: search <关键词> [源]');
          console.log('   例: search 周杰伦');
          console.log('   例: search Beat It');
          console.log('   例: search 周杰伦 kw');
          process.exit(1);
        }
        const encodedKeyword = encodeURIComponent(keyword);
        const url = source
          ? `lxmusic://music/search/${source}/${encodedKeyword}`
          : `lxmusic://music/search/${encodedKeyword}`;
        await openSchemeUrl(url);
        console.log(`🔍 搜索: ${keyword}${source ? ` (源: ${source})` : ''}`);
        break;
      }

      case 'searchPlay': {
        checkLocal();
        let songName, singer;
        
        if (args.length >= 4) {
          // 3个及以上参数：尝试识别歌手（最后一个参数如果是常见歌手名）
          const commonSingers = ['周杰伦', '林俊杰', '张学友', '刘德华', '邓紫棋', '薛之谦', '陈奕迅', '王菲', '那英', '李宗盛', 'Adele', 'Avril', 'Westlife', 'Backstreet', 'Michael', 'Jackson'];
          const lastArg = args[args.length - 1];
          if (commonSingers.some(s => lastArg.toLowerCase().includes(s.toLowerCase()))) {
            singer = lastArg;
            songName = args.slice(1, -1).join(' ');
          } else {
            songName = getArgsFrom(1);
          }
        } else if (args.length === 3) {
          // 2个参数：可能是 "歌名 歌手" 或 "多词歌名"
          const commonSingers = ['周杰伦', '林俊杰', '张学友', '刘德华', '邓紫棋', '薛之谦', '陈奕迅', '王菲', '那英', '李宗盛', 'Adele', 'Avril', 'Westlife', 'Backstreet', 'Michael', 'Jackson'];
          if (commonSingers.some(s => args[2].toLowerCase().includes(s.toLowerCase()))) {
            songName = args[1];
            singer = args[2];
          } else {
            songName = getArgsFrom(1);
          }
        } else {
          songName = args[1] || '';
        }
        
        if (!songName) {
          console.log('❌ 用法: searchPlay <歌名> [歌手]');
          console.log('   例: searchPlay 晴天');
          console.log('   例: searchPlay Beat It');
          console.log('   例: searchPlay God is a girl');
          console.log('   例: searchPlay 晴天 周杰伦');
          process.exit(1);
        }
        const query = singer ? `${songName}-${singer}` : songName;
        const encodedQuery = encodeURIComponent(query);
        const url = `lxmusic://music/searchPlay/${encodedQuery}`;
        await openSchemeUrl(url);
        console.log(`🎵 尝试播放: ${query}`);
        break;
      }

      case 'play': {
        await api.play();
        console.log('▶️  播放');
        break;
      }

      case 'pause': {
        await api.pause();
        console.log('⏸️  暂停');
        break;
      }

      case 'toggle': {
        checkLocal();
        await openSchemeUrl('lxmusic://player/togglePlay');
        console.log('⏯️  切换播放/暂停');
        break;
      }

      case 'next': {
        await api.next();
        console.log('⏭️  下一首');
        break;
      }

      case 'prev': {
        await api.prev();
        console.log('⏮️  上一首');
        break;
      }

      case 'seek': {
        const offset = parseInt(args[1]);
        if (isNaN(offset) || offset < 0) {
          console.log('❌ 用法: seek <偏移量(秒)>');
          process.exit(1);
        }
        await api.seek(offset);
        console.log(`⏩ 跳转到 ${offset} 秒`);
        break;
      }

      case 'status': {
        const data = await api.status();
        console.log(formatStatus(data));
        break;
      }

      case 'now': {
        const data = await api.status();
        if (data && data.name) {
          console.log(`${data.name} - ${data.singer || '未知歌手'}`);
        } else {
          console.log('⏹️  未在播放');
        }
        break;
      }

      case 'lyric': {
        const data = await api.status();
        if (data && data.lyric) {
          console.log(data.lyric);
        } else {
          console.log('无歌词');
        }
        break;
      }

      case 'volume': {
        const vol = parseInt(args[1]);
        if (isNaN(vol) || vol < 0 || vol > 100) {
          console.log('❌ 用法: volume <0-100>');
          process.exit(1);
        }
        await api.volume(vol);
        console.log(`🔊 音量设置为 ${vol}%`);
        break;
      }

      case 'mute': {
        await api.mute(true);
        console.log('🔇 静音');
        break;
      }

      case 'unmute': {
        await api.mute(false);
        console.log('🔊 取消静音');
        break;
      }

      case 'list': {
        const dbPath = getLxDataDbPath();
        const playlists = queryPlaylists(dbPath);
        if (playlists.length === 0) {
          console.log('📋 暂无本地歌单');
        } else {
          console.log('📋 本地歌单:');
          for (const pl of playlists) {
            const src = pl.sourceName || (pl.source ? SOURCE_NAMES[pl.source] || pl.source : '本地');
            const count = pl.songCount !== undefined ? ` (${pl.songCount}首)` : '';
            console.log(`  ${pl.id}  ${pl.name}  [${src}]${count}`);
          }
        }
        break;
      }

      case 'listsongs': {
        const listId = args[1];
        if (!listId) {
          console.log('❌ 用法: listsongs <歌单ID>');
          console.log('   用 list 命令查看歌单ID');
          process.exit(1);
        }
        const dbPath2 = getLxDataDbPath();
        const data = queryPlaylistSongs(dbPath2, listId);
        if (data.error) {
          console.log(`❌ ${data.error}`);
          process.exit(1);
        }
        console.log(`📋 ${data.playlist} (${data.total}首):`);
        for (const s of data.songs) {
          console.log(`  ${s.index}. ${s.name} - ${s.singer}`);
        }
        break;
      }

      case 'listplay': {
        checkLocal();
        const listId2 = args[1];
        if (!listId2) {
          console.log('❌ 用法: listplay <歌单ID>');
          console.log('   用 list 命令查看歌单ID');
          process.exit(1);
        }
        const dbPath3 = getLxDataDbPath();
        // 先查歌单的 source 和 sourceId
        if (!fs.existsSync(dbPath3)) {
          console.log(`❌ 数据库不存在: ${dbPath3}`);
          process.exit(1);
        }
        const scriptPath2 = path.join(__dirname, 'list.py');
        try {
          const playResult = execSync(`python "${scriptPath2}" play "${listId2}" --db "${dbPath3}"`, { encoding: 'utf-8', timeout: 10000 });
          const pr = JSON.parse(playResult);
          if (pr.error) {
            console.log(`❌ ${pr.error}`);
          } else {
            console.log(`▶️  播放歌单: ${pr.source}/${pr.sourceId}`);
          }
        } catch (err) {
          console.log(`❌ 播放失败: ${err.message}`);
        }
        break;
      }

      case 'openlist': {
        checkLocal();
        const source = args[1];
        const id = args[2];
        if (!source || !id) {
          console.log('❌ 用法: openlist <源> <歌单ID>');
          console.log('  源: kw(酷我), kg(酷狗), tx(QQ), wy(网易), mg(咪咕)');
          process.exit(1);
        }
        const url = `lxmusic://songlist/open/${source}/${id}`;
        await openSchemeUrl(url);
        console.log(`📂 打开歌单: ${source} ${id}`);
        break;
      }

      case 'playlist': {
        checkLocal();
        const plSource = args[1];
        const plId = args[2];
        const startIndex = args[3] || '1';
        if (!plSource || !plId) {
          console.log('❌ 用法: playlist <源> <歌单ID> [起始序号]');
          console.log('  源: kw(酷我), kg(酷狗), tx(QQ), wy(网易), mg(咪咕)');
          process.exit(1);
        }
        const url = `lxmusic://songlist/play/${plSource}/${plId}/${startIndex}`;
        await openSchemeUrl(url);
        console.log(`▶️  播放歌单: ${plSource} ${plId} (从第 ${startIndex} 首开始)`);
        break;
      }

      case 'collect': {
        await api.collect();
        console.log('❤️  已收藏');
        break;
      }

      case 'uncollect': {
        await api.uncollect();
        console.log('💔 已取消收藏');
        break;
      }

      case 'dislike': {
        checkLocal();
        await openSchemeUrl('lxmusic://player/dislike');
        console.log('👎 已标记不喜欢');
        break;
      }

      default:
        console.log(`❌ 未知命令: ${command}`);
        console.log('使用 "node lx-music-cli.js" 查看帮助');
        process.exit(1);
    }
  } catch (error) {
    console.error(`❌ 错误: ${error.message}`);
    process.exit(1);
  }
}

main();
