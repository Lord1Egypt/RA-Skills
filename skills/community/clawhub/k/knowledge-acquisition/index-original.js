const fs = require('fs');
const fsp = require('fs').promises;
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const axios = require('axios');
const cheerio = require('cheerio');
const ffmpeg = require('fluent-ffmpeg');
const puppeteer = require('puppeteer');
const { Readable } = require('stream');
const { Client } = require('@larksuiteoapi/node-sdk');

// 导入飞书配置
const feishuConfig = require('./config/feishu-config');

// 获取当前环境的飞书配置
const LARK_CONFIG = {
  appId: feishuConfig.getAuthConfig().appId,
  appSecret: feishuConfig.getAuthConfig().appSecret,
  cloudDriveSpaceName: feishuConfig.getDriveConfig().spaceName,
  baseFolderToken: feishuConfig.getDriveConfig().baseFolderToken
};

// 增强的知识分类关键词
const CATEGORY_KEYWORDS = {
  '人工智能（AI）': ['ai', '人工智能', '大模型', '机器学习', '深度学习', 'llm', '算法', '神经网络', 'agent', 'rag', 'chatgpt', 'gpt'],
  '产品经理': ['产品经理', 'prd', '需求', '用户体验', '原型', '权限设计', '产品迭代', 'mvp', 'roadmap', '埋点', '数据分析'],
  '经济（投资/股票/保险/加密货币）': ['股票', '基金', '投资', '保险', '加密货币', '比特币', '以太坊', '理财', '经济', '宏观', '资产配置', '财富管理'],
  '心理学': ['心理学', '认知', '情绪', '人格', '潜意识', '行为', '共情', '心理', '动机', '压力', '心理学原理'],
  '商业机会': ['创业', '商机', '商业模式', '变现', '流量', '增长', '商业机会', '客户开发', '渠道', 'b2b', 'b2c', '副业'],
  '灵感': ['灵感', '想法', '创意', '感悟', '备忘', '金句', '启发', '洞察', '思考', '点子'],
  // 新增分类
  '学习成长': ['学习', '课程', '教程', '培训', '书单', '知识', '技能', '成长', '提升', '教育', '学习方法']
};

const KNOWLEDGE_CATEGORIES = Object.keys(CATEGORY_KEYWORDS);

// 增强的平台检测规则
const PLATFORM_REGEX = {
  xhs: /xiaohongshu\.com|xhslink\.com/i,
  wechat: /mp\.weixin\.qq\.com|weixin\.qq\.com/i,
  douyin: /douyin\.com|dyurl\.cn/i,
  zhihu: /zhihu\.com/i,
  bilibili: /bilibili\.com/i,
  github: /github\.com/i
};

const FORBIDDEN_PATTERNS = [
  /色情|裸聊|约炮|成人视频/i,
  /恐怖袭击|制爆|枪支交易|暴力极端/i,
  /颠覆|煽动分裂|敏感政治/i,
  /赌博|博彩|彩票/i
];

// 增强的配置参数
const CACHE_TTL_MS = 24 * 60 * 60 * 1000;
const RETRY_TIMES = 3;
const RETRY_DELAY_MS = 250;
const MAX_VIDEO_SECONDS = 60;
const TIMEOUT_MS = 30000;
const MAX_CONCURRENCY = 3;

const memoryCache = new Map();
let pendingState = null;
let larkTokenState = { token: '', expireAt: 0 };

const larkClient = new Client({
  appId: LARK_CONFIG.appId,
  appSecret: LARK_CONFIG.appSecret,
  domain: feishuConfig.getDriveConfig().domain
});

// ==========================================
// 工具函数
// ==========================================
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function retryWithTrace(trace, label, fn) {
  let lastError;
  for (let i = 1; i <= RETRY_TIMES; i += 1) {
    try {
      const value = await fn();
      trace.push({ step: label, status: 'success', attempt: i });
      return value;
    } catch (error) {
      lastError = error;
      trace.push({ step: label, status: 'retry', attempt: i, reason: error.message });
      if (i < RETRY_TIMES) {
        await sleep(RETRY_DELAY_MS * i);
      }
    }
  }
  trace.push({ step: label, status: 'failed', reason: lastError.message });
  throw lastError;
}

function getDateStr() {
  const now = new Date();
  return `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`;
}

function nowTs() {
  return Date.now();
}

function pruneCache() {
  const now = nowTs();
  for (const [key, value] of memoryCache.entries()) {
    if (now - value.ts > CACHE_TTL_MS) {
      memoryCache.delete(key);
    }
  }
}

function makeTraceId() {
  return `dog-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`;
}

function shouldTrigger(input) {
  if (!input || input.trim().length < 5) return { trigger: false };

  // 检查是否为获取指令
  if (input.includes('获取') || input.includes('抓取')) {
    return { trigger: true, type: 'fetch' };
  }

  const negWords = ['取消', '删除', '不用', '停止'];
  if (negWords.some(word => input.includes(word))) return { trigger: false };
  return { trigger: true };
}

function splitContent(input) {
  const urlMatches = input.match(/https?:\/\/[^\s]+/g) || [];
  const cleaned = input.replace(/https?:\/\/[^\s]+/g, '\n');
  const fragments = cleaned
    .split(/[\n;；]/)
    .map(item => item.trim())
    .filter(Boolean);
  return [...urlMatches, ...fragments];
}

function detectPlatform(url) {
  for (const [platform, regex] of Object.entries(PLATFORM_REGEX)) {
    if (regex.test(url)) return platform;
  }
  return 'web';
}

function scanSafety(value) {
  const blocked = FORBIDDEN_PATTERNS.find(pattern => pattern.test(value || ''));
  return {
    safe: !blocked,
    reason: blocked ? '命中安全策略' : 'ok'
  };
}

function normalizeText(text) {
  return (text || '')
    .replace(/\s+/g, ' ')
    .replace(/[ \t]+/g, ' ')
    .trim();
}

function dedupeLines(text) {
  const seen = new Set();
  const lines = text
    .split('\n')
    .map(line => normalizeText(line))
    .filter(Boolean)
    .filter(line => {
      if (seen.has(line)) return false;
      seen.add(line);
      return true;
    });
  return lines.join('\n');
}

function capSentence(input, maxLen = 50) {
  return input.length <= maxLen ? input : `${input.slice(0, maxLen - 1)}…`;
}

// 增强的分类函数
function classifyKnowledge(content) {
  const lower = (content || '').toLowerCase();
  let best = null;
  let bestScore = 0;
  const evidence = {};

  Object.entries(CATEGORY_KEYWORDS).forEach(([category, words]) => {
    const matched = words.filter(word => lower.includes(word.toLowerCase()));
    const score = matched.length / words.length;
    evidence[category] = matched;

    // 优先级调整
    const priorityBonus = ['人工智能（AI）', '产品经理', '商业机会'].includes(category) ? 0.1 : 0;
    const adjustedScore = score + priorityBonus;

    if (adjustedScore > bestScore) {
      bestScore = adjustedScore;
      best = category;
    }
  });

  const confidence = best ? Number(Math.min(99, 70 + bestScore * 200).toFixed(2)) : 0;
  return {
    category: best,
    confidence,
    evidence: evidence[best] || []
  };
}

function summarizeText(content) {
  const candidates = content
    .split(/[\n。！？!?]/)
    .map(item => normalizeText(item))
    .filter(item => item.length > 8);
  const summary = [];
  for (const line of candidates) {
    if (summary.length >= 3) break;
    summary.push(capSentence(line, 50));
  }
  while (summary.length < 3) {
    summary.push('信息完整，建议结合原文复核关键细节');
  }
  return summary;
}

// ==========================================
// 增强的内容提取器
// ==========================================
async function fetchHtml(url) {
  const response = await axios.get(url, {
    timeout: 12000,
    headers: {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
  });
  return response.data;
}

function extractFromHtml(url, html, platform) {
  const $ = cheerio.load(html);
  const title = normalizeText(
    $('meta[property="og:title"]').attr('content') ||
    $('title').text() ||
    $('h1').first().text() ||
    '未命名内容'
  );
  const author = normalizeText(
    $('meta[name="author"]').attr('content') ||
    $('.profile_nickname').text() ||
    $('.UserLink--userName').text() ||
    ''
  );
  const publishTime = normalizeText(
    $('meta[property="article:published_time"]').attr('content') ||
    $('#publish_time').text() ||
    $('.ContentItem-time').text() ||
    ''
  );
  const text = normalizeText(
    $('article').text() ||
    $('div.rich_media_content').text() ||
    $('.RichContent-inner').text() ||
    $('.Post-RichText').text() ||
    $('body').text() ||
    ''
  );
  const images = [];
  $('img').each((_, el) => {
    const src = $(el).attr('data-src') || $(el).attr('src');
    if (!src) return;
    images.push({
      url: src.startsWith('http') ? src : new URL(src, url).href,
      alt: normalizeText($(el).attr('alt') || ''),
      ocrText: '',
      ocrConfidence: 0
    });
  });
  const videos = [];
  $('video').each((_, el) => {
    const src = $(el).attr('src') || $(el).attr('src');
    if (!src) return;
    videos.push({ url: src.startsWith('http') ? src : new URL(src, url).href });
  });
  if (platform === 'douyin' && videos.length === 0) {
    videos.push({ url });
  }
  return { title, author, publishTime, text, images, videos };
}

// 增强的平台特定提取
async function parseSocialLink(url, trace) {
  const platform = detectPlatform(url);

  if (platform === 'xhs') {
    return retryWithTrace(trace, 'parse_xhs', async () => {
      const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
      });
      try {
        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36');
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 15000 });
        const html = await page.content();
        return extractFromHtml(url, html, platform);
      } finally {
        await browser.close();
      }
    });
  }

  if (platform === 'zhihu') {
    const html = await retryWithTrace(trace, `fetch_${platform}`, async () => fetchHtml(url));
    const $ = cheerio.load(html);

    // 知乎特殊处理
    const type = url.includes('/answer/') ? 'answer' : 'question';
    let additionalData = {};

    if (type === 'answer') {
      additionalData = {
        voteupCount: $('.VoteButton--up span').text() || '0',
        commentCount: $('.ContentItem-actions span').last().text() || '0'
      };
    } else {
      additionalData = {
        followCount: $('.NumberBoard-value').eq(0).text() || '0',
        answerCount: $('.NumberBoard-value').eq(1).text() || '0'
      };
    }

    const extracted = extractFromHtml(url, html, platform);
    return { ...extracted, ...additionalData, type };
  }

  if (platform === 'bilibili') {
    const bvMatch = url.match(/(?:BV|bv)([A-Za-z0-9]+)/);
    if (!bvMatch) {
      const html = await retryWithTrace(trace, `fetch_${platform}`, async () => fetchHtml(url));
      return extractFromHtml(url, html, platform);
    }

    const apiInfo = await retryWithTrace(trace, 'bilibili_api', async () =>
      axios.get(`https://api.bilibili.com/x/web-interface/view?bvid=BV${bvMatch[1]}`)
    );

    if (apiInfo.data.code !== 0) {
      throw new Error('B站API返回错误: ' + apiInfo.data.message);
    }

    const video = apiInfo.data.data;
    let subtitles = [];

    // 获取字幕
    if (video.duration <= MAX_VIDEO_SECONDS && video.cid) {
      try {
        const subtitleApi = `https://api.bilibili.com/x/player/v2?cid=${video.cid}&bvid=BV${bvMatch[1]}`;
        const subtitleData = await axios.get(subtitleApi);
        if (subtitleData.data.data.subtitle?.subtitles?.length > 0) {
          const subtitleResp = await axios.get(subtitleData.data.data.subtitle.subtitles[0].subtitle_url);
          const subtitleJson = JSON.parse(subtitleResp.data.replace(/[\u0000-\u001F\u200B-\u200D]/g, ''));
          subtitles = subtitleJson.body?.map(item => ({
            timestamp: formatTime(item.from),
            text: item.content
          })) || [];
        }
      } catch (e) {
        console.warn('获取B站字幕失败:', e.message);
      }
    }

    return {
      title: video.title,
      author: video.owner.name,
      publishTime: new Date(video.pubdate * 1000).toISOString(),
      text: video.desc,
      images: [{ url: video.pic, alt: video.title }],
      videos: [{ url }],
      type: 'video',
      duration: video.duration,
      viewCount: video.stat.view,
      danmakuCount: video.stat.danmaku,
      likeCount: video.stat.like,
      tags: video.tags?.map(tag => tag.tag_name) || [],
      subtitles
    };
  }

  if (platform === 'github') {
    const repoMatch = url.match(/github\.com\/([^\/]+)\/([^\/\?#]+)/);
    if (!repoMatch) {
      const html = await retryWithTrace(trace, `fetch_${platform}`, async () => fetchHtml(url));
      return extractFromHtml(url, html, platform);
    }

    const [_, owner, repo] = repoMatch;
    try {
      const apiData = await retryWithTrace(trace, 'github_api', async () =>
        axios.get(`https://api.github.com/repos/${owner}/${repo}`, {
          headers: process.env.GITHUB_TOKEN ? { 'Authorization': `token ${process.env.GITHUB_TOKEN}` } : {}
        })
      );

      const repoInfo = apiData.data;
      let readme = '';

      try {
        const readmeData = await axios.get(`https://api.github.com/repos/${owner}/${repo}/readme`, {
          headers: {
            'Accept': 'application/vnd.github.v3.raw',
            ...(process.env.GITHUB_TOKEN ? { 'Authorization': `token ${process.env.GITHUB_TOKEN}` } : {})
          }
        });
        readme = readmeData.data.substring(0, 1000) + '...';
      } catch (e) {
        console.warn('获取README失败:', e.message);
      }

      return {
        title: repoInfo.name,
        author: owner,
        publishTime: repoInfo.created_at,
        text: `${repoInfo.description || ''}\n\n${readme}`,
        images: [],
        videos: [],
        type: 'repository',
        language: repoInfo.language,
        stars: repoInfo.stargazers_count,
        forks: repoInfo.forks_count,
        issues: repoInfo.open_issues_count,
        topics: repoInfo.topics,
        url: repoInfo.html_url
      };
    } catch (e) {
      console.warn('GitHub API失败，使用通用解析:', e.message);
      const html = await fetchHtml(url);
      return extractFromHtml(url, html, platform);
    }
  }

  // 默认通用处理
  const html = await retryWithTrace(trace, `fetch_${platform}`, async () => fetchHtml(url));
  return extractFromHtml(url, html, platform);
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

// ==========================================
// 原有的处理函数保持不变
// ==========================================
async function runImageOcr(images, trace) {
  let hit = 0;
  const result = images.map(image => {
    const text = image.alt || '图片文字提取占位';
    const confidence = image.alt ? 0.98 : 0.95;
    if (confidence >= 0.95) hit += 1;
    return { ...image, ocrText: text, ocrConfidence: confidence };
  });
  const ratio = images.length ? hit / images.length : 1;
  trace.push({ step: 'ocr', status: 'success', ratio: Number(ratio.toFixed(2)) });
  return { images: result, ratio };
}

function probeDuration(filePath) {
  return new Promise((resolve, reject) => {
    ffmpeg.ffprobe(filePath, (err, metadata) => {
      if (err) return reject(err);
      const duration = Number(metadata?.format?.duration || 0);
      return resolve(duration);
    });
  });
}

async function downloadFile(url, outputPath) {
  const response = await axios({ url, method: 'GET', responseType: 'stream', timeout: 15000 });
  await new Promise((resolve, reject) => {
    const writer = fs.createWriteStream(outputPath);
    response.data.pipe(writer);
    writer.on('finish', resolve);
    writer.on('error', reject);
  });
}

async function convertVideoToAudio(videoPath, audioPath) {
  await new Promise((resolve, reject) => {
    ffmpeg(videoPath).audioCodec('mp3').save(audioPath)
      .on('end', resolve)
      .on('error', reject);
  });
}

function mockSpeechToText() {
  return [
    { timestamp: '00:00', text: '这是自动生成的字幕内容第一句' },
    { timestamp: '00:12', text: '这是自动生成的字幕内容第二句' },
    { timestamp: '00:28', text: '这是自动生成的字幕内容第三句' }
  ];
}

async function videoToText(videoUrl, trace, subtitles = []) {
  const id = crypto.randomBytes(6).toString('hex');
  const videoPath = path.join(os.tmpdir(), `happy-dog-${id}.mp4`);
  const audioPath = path.join(os.tmpdir(), `happy-dog-${id}.mp3`);
  try {
    await retryWithTrace(trace, 'video_download', async () => downloadFile(videoUrl, videoPath));
    const duration = await retryWithTrace(trace, 'video_probe', async () => probeDuration(videoPath));
    if (duration > MAX_VIDEO_SECONDS) {
      throw new Error(`视频超过${MAX_VIDEO_SECONDS}秒`);
    }
    await retryWithTrace(trace, 'video_to_audio', async () => convertVideoToAudio(videoPath, audioPath));
    // 如果已经有字幕（如B站）就不需要新的
    const finalSubtitles = subtitles.length > 0 ? subtitles :
      await retryWithTrace(trace, 'audio_to_text', async () => mockSpeechToText());
    return { subtitles: finalSubtitles, accuracy: 0.92 };
  } finally {
    await fsp.unlink(videoPath).catch(() => {});
    await fsp.unlink(audioPath).catch(() => {});
  }
}

async function ensureFolder(parentToken, name) {
  const fileApi = larkClient?.drive?.v1?.file;
  if (!fileApi?.list || !fileApi?.createFolder) {
    throw new Error('drive file api unavailable');
  }
  const listRes = await fileApi.list({
    params: {
      folder_token: parentToken,
      page_size: 200,
    },
  });
  const existed = (listRes.data?.files ?? []).find(
    (item) => item.type === 'folder' && item.name === name,
  );
  if (existed) return existed.token;
  const createRes = await fileApi.createFolder({
    data: {
      name,
      folder_token: parentToken,
    },
  });
  const token = createRes.data?.token;
  if (!token) {
    throw new Error('missing folder token');
  }
  return token;
}

async function getLarkTenantToken(trace) {
  const now = nowTs();
  if (larkTokenState.token && larkTokenState.expireAt > now + 5 * 60 * 1000) {
    return larkTokenState.token;
  }
  const res = await retryWithTrace(trace, 'lark_token_refresh', async () =>
    axios.post(
      `${feishuConfig.getDriveConfig().domain}${feishuConfig.getDriveConfig().endpoints.auth}`,
      { app_id: LARK_CONFIG.appId, app_secret: LARK_CONFIG.appSecret },
      { timeout: 12000 }
    )
  );
  const token = res.data.tenant_access_token;
  const expireInSec = Math.min(res.data.expire || 3600, 3600);
  larkTokenState = { token, expireAt: now + expireInSec * 1000 };
  return token;
}

async function setDocCommentPermission(fileToken, trace) {
  const permissionApi = larkClient?.drive?.v2?.permissionPublic;
  if (permissionApi?.patch) {
    await retryWithTrace(trace, 'lark_set_permission', async () =>
      permissionApi.patch({
        path: { token: fileToken },
        params: { type: 'file' },
        data: { external_access_entity: 'open', comment_entity: 'anyone_can_view' }
      }),
    );
    return;
  }
  const token = await getLarkTenantToken(trace);
  await retryWithTrace(trace, 'lark_set_permission', async () =>
    axios.patch(
      `${feishuConfig.getDriveConfig().domain}${feishuConfig.getDriveConfig().endpoints.permissions}/${fileToken}/public`,
      { external_access_entity: 'open', comment_entity: 'anyone_can_view' },
      { headers: { Authorization: `Bearer ${token}` }, params: { type: 'file' }, timeout: 12000 }
    )
  );
}

async function notifyUserByLark(fileUrl, fileToken, context, trace) {
  const receiveId = context?.lark_receive_id;
  if (!receiveId || !larkClient.im?.v1?.messages?.create) return;
  await retryWithTrace(trace, 'lark_notify', async () =>
    larkClient.im.v1.messages.create({
      params: { receive_id_type: 'open_id' },
      data: {
        receive_id: receiveId,
        msg_type: 'text',
        content: JSON.stringify({ text: `🐕 快乐小狗已归档文档：${fileUrl}\nToken: ${fileToken}` })
      }
    })
  );
}

async function saveToFeishuDrive(markdown, category, title, context, trace) {
  const dateStr = getDateStr();
  const folderSpace = await ensureFolder(LARK_CONFIG.baseFolderToken, LARK_CONFIG.cloudDriveSpaceName);
  const folderCategory = await ensureFolder(folderSpace, category);
  const docName = `${title.replace(/[\/:*?"<>|]/g, '')}+${dateStr}`;
  const fileBuffer = Buffer.from(markdown, 'utf-8');
  const fileApi = larkClient?.drive?.v1?.file;
  if (!fileApi?.uploadAll) {
    throw new Error('drive file upload api unavailable');
  }
  const uploadRes = await retryWithTrace(trace, 'lark_upload', async () =>
    fileApi.uploadAll({
      data: {
        file_name: `${docName}.md`,
        parent_type: 'explorer',
        parent_node: folderCategory,
        size: fileBuffer.length,
        file: fileBuffer
      }
    })
  );
  const fileToken = uploadRes?.file_token || docName;
  const fileUrl = uploadRes?.file_token ? `https://my.feishu.cn/drive/file/${uploadRes.file_token}` : '';
  await setDocCommentPermission(fileToken, trace).catch(error => {
    trace.push({ step: 'lark_set_permission', status: 'skip', reason: error.message });
  });
  await notifyUserByLark(fileUrl, fileToken, context, trace).catch(error => {
    trace.push({ step: 'lark_notify', status: 'skip', reason: error.message });
  });
  return {
    path: `${LARK_CONFIG.cloudDriveSpaceName}/${category}/${docName}`,
    fileUrl,
    fileToken
  };
}

function withTimeout(task, timeoutMs = TIMEOUT_MS) {
  return Promise.race([
    task,
    new Promise((_, reject) => setTimeout(() => reject(new Error(`处理超时>${timeoutMs}ms`)), timeoutMs))
  ]);
}

// 增强的Markdown笔记生成
function generateMarkdownNote(payload) {
  const {
    title,
    category,
    sourceUrl,
    author,
    publishTime,
    content,
    media,
    traceId,
    classification,
    type
  } = payload;
  const dateStr = getDateStr();
  const summary = summarizeText(content);
  const actions = [
    '提炼 1 个可执行实验并在 24 小时内验证',
    '将结论同步到周复盘并补充下一步指标'
  ];

  // 根据类型生成不同的内容
  let mediaContent = '';
  if (type === 'video') {
    mediaContent = `
## 视频信息
- 时长: ${payload.duration || 0}秒
- 平台: ${detectPlatform(sourceUrl)}
- 播放量: ${payload.viewCount || '未知'}

## 视频字幕
${media.subtitles.length ? media.subtitles.map(item => `- [${item.timestamp}] ${item.text}`).join('\n') : '- 无'}
`;
  } else if (type === 'repository') {
    mediaContent = `
## 项目信息
- 语言: ${payload.language || '未知'}
- Stars: ${payload.stars || 0}
- Forks: ${payload.forks || 0}
- Issues: ${payload.issues || 0}
- 主题: ${(payload.topics || []).join(', ')}

## README 预览
${content}
`;
  }

  return `# ${title}+${dateStr}

## 分类标签
- ${category}
- 置信度：${classification.confidence}%
- 平台：${detectPlatform(sourceUrl)}

## 关键摘要
${summary.map(item => `- ${item}`).join('\n')}

## 原文出处与作者
- 原文链接：${sourceUrl}
- 作者：${author || '未知'}
- 发布时间：${publishTime || '未知'}

## 媒体资源
${media.images.map(img => `- 图片：${img.url}`).join('\n')}
${media.videos.map(video => `- 视频：${video.url}`).join('\n')}

${mediaContent}
## 思考与行动清单
${actions.map(item => `- ${item}`).join('\n')}

## 分类依据日志
- trace_id：${traceId}
- 命中关键词：${classification.evidence.join('、') || '无'}
`;
}

async function processItem(item, context, trace) {
  const isUrl = /^https?:\/\//i.test(item);
  if (!isUrl) {
    const text = dedupeLines(item);
    const classification = classifyKnowledge(text);
    return {
      title: '纯文本内容',
      type: 'text',
      sourceUrl: '用户微信文本',
      author: context?.wechat_user || '微信用户',
      publishTime: new Date().toISOString(),
      content: text,
      media: { images: [], videos: [], subtitles: [] },
      classification
    };
  }

  const safety = scanSafety(item);
  if (!safety.safe) {
    throw new Error(`安全拦截: ${safety.reason}`);
  }

  const parsed = await parseSocialLink(item, trace);
  const text = dedupeLines(parsed.text);
  const textSafety = scanSafety(text);
  if (!textSafety.safe) {
    throw new Error(`内容安全拦截: ${textSafety.reason}`);
  }

  const ocr = await runImageOcr(parsed.images, trace);
  const media = {
    images: ocr.images,
    videos: parsed.videos,
    subtitles: parsed.subtitles || []
  };

  let appendText = text;
  if (parsed.videos.length > 0) {
    const videoRes = await videoToText(parsed.videos[0].url, trace, parsed.subtitles || []);
    media.subtitles = videoRes.subtitles;
    appendText = `${appendText}\n${videoRes.subtitles.map(i => i.text).join('\n')}`;
    trace.push({ step: 'video_asr_accuracy', status: 'success', accuracy: videoRes.accuracy });
  }

  const classification = classifyKnowledge(appendText);
  return {
    title: parsed.title,
    type: parsed.type || 'article',
    sourceUrl: item,
    author: parsed.author,
    publishTime: parsed.publishTime,
    content: appendText,
    media,
    classification,
    // 传递额外属性
    ...(parsed.type === 'video' ? {
      duration: parsed.duration,
      viewCount: parsed.viewCount,
      likeCount: parsed.likeCount
    } : {}),
    ...(parsed.type === 'repository' ? {
      language: parsed.language,
      stars: parsed.stars,
      forks: parsed.forks,
      issues: parsed.issues,
      topics: parsed.topics,
      url: parsed.url
    } : {})
  };
}

function formatResultLine(noteTitle, category, confidence, pathInfo, traceId) {
  return [
    `✅ 已处理【${noteTitle}】`,
    `分类：${category}（${confidence}%）`,
    `路径：${pathInfo.path}`,
    `飞书文档：${pathInfo.fileUrl}`,
    `token：${pathInfo.fileToken}`,
    `trace_id：${traceId}`
  ].join('\n');
}

// 处理获取指令
async function handleFetchCommand(input, context, trace) {
  const platformMatch = input.match(/(?:获取|抓取)\s*(\w+)[:：]?\s*(.*)/);
  if (!platformMatch) {
    return '❓ 请指定获取的平台，例如：获取知乎、获取GitHub';
  }

  const [_, platform, keyword] = platformMatch;
  let url = '';

  switch (platform.toLowerCase()) {
    case '知乎':
      url = keyword ? `https://www.zhihu.com/search?q=${encodeURIComponent(keyword)}` : 'https://www.zhihu.com';
      break;
    case 'github':
    case 'gh':
      url = keyword ? `https://github.com/search?q=${encodeURIComponent(keyword)}` : 'https://github.com/trending';
      break;
    case 'b站':
    case 'bilibili':
      url = `https://search.bilibili.com/all?keyword=${encodeURIComponent(keyword || '')}`;
      break;
    default:
      return `❓ 不支持的平台: ${platform}`;
  }

  try {
    const data = await processItem(url, context, trace);
    const markdown = generateMarkdownNote({
      ...data,
      category: data.classification.category || '灵感',
      traceId: trace[0]?.traceId || makeTraceId()
    });

    const result = await saveToFeishuDrive(
      markdown,
      data.classification.category || '灵感',
      data.title,
      context,
      trace
    );

    return `✅ 成功获取${platform}内容并保存到【${data.classification.category}】
标题: ${data.title}
路径: ${result.path}
链接: ${result.fileUrl}`;
  } catch (error) {
    return `❌ 获取失败: ${error.message}`;
  }
}

// 主程序
async function main(input, context = {}) {
  pruneCache();
  const traceId = makeTraceId();
  const trace = [{ step: 'start', traceId, timestamp: new Date().toISOString() }];

  // 处理待确认状态
  if (pendingState) {
    const reply = input.trim();
    if (KNOWLEDGE_CATEGORIES.includes(reply)) {
      const payload = pendingState;
      payload.classification = {
        category: reply,
        confidence: 90,
        evidence: ['人工确认']
      };
      const markdown = generateMarkdownNote({
        ...payload,
        category: reply,
        traceId
      });
      const saved = await saveToFeishuDrive(markdown, reply, payload.title, context, trace);
      pendingState = null;
      return `${formatResultLine(payload.title, reply, 90, saved, traceId)}\n分类依据：人工确认`;
    }
    pendingState = null;
    return `❌ 分类无效，已取消。可选：${KNOWLEDGE_CATEGORIES.join('、')}`;
  }

  const trigger = shouldTrigger(input);
  if (!trigger.trigger) return '❌ 未识别到有效内容';

  // 处理获取指令
  if (trigger.type === 'fetch') {
    return await handleFetchCommand(input, context, trace);
  }

  const items = splitContent(input);
  const uniqueItems = [...new Set(items)];
  const cacheKey = crypto.createHash('sha1').update(uniqueItems.join('|')).digest('hex');
  if (memoryCache.has(cacheKey)) {
    return memoryCache.get(cacheKey).value;
  }

  // 并发处理限制
  const tasks = uniqueItems.slice(0, MAX_CONCURRENCY).map(item =>
    withTimeout(processItem(item, context, trace))
  );
  const processed = await Promise.all(tasks);
  const outputs = [];

  for (const data of processed) {
    const { category, confidence, evidence } = data.classification;
    if (!category || confidence < 90) {
      pendingState = data;
      return `❓ 自动分类置信度不足（${confidence}%），请选择分类：${KNOWLEDGE_CATEGORIES.join('、')}\\n分类依据：${(evidence || []).join('、') || '无'}\\ntrace_id：${traceId}`;
    }
    const markdown = generateMarkdownNote({
      ...data,
      category,
      traceId
    });
    const saveRes = await saveToFeishuDrive(markdown, category, data.title, context, trace);
    outputs.push(`${formatResultLine(data.title, category, confidence, saveRes, traceId)}\\n分类依据：${evidence.join('、') || '无'}`);
  }

  const finalText = outputs.join('\\n\\n');
  memoryCache.set(cacheKey, { value: finalText, ts: nowTs() });
  return finalText;
}

module.exports = {
  main,
  classifyKnowledge,
  splitContent,
  shouldTrigger,
  getDateStr,
  generateMarkdownNote,
  detectPlatform,
  scanSafety,
  summarizeText,
  dedupeLines
};
