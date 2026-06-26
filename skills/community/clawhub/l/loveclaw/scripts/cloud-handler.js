/**
 * 八字缘分匹配 - 云端版会话处理 v2.0.0
 * 简化流程：手机号即账号，匹配后才能看到对方信息
 * v2.0.0: 多channel支持 - 用户通过什么渠道报名，就通过什么渠道收到通知
 */

const path = require('path');
const fs = require('fs');
require('./load-workspace-env').applyFromWorkspaceDotenv();

const cloudData = require('./cloud-data');
const bazi = require('./bazi');
const match = require('./match');
const reportTemplates = require('./report-templates');
const os = require('os');
const { execFileSync } = require('child_process');

function openclawCmd() {
  return process.env.OPENCLAW_BIN || 'openclaw';
}

function openclawExec(args, execOpts = {}) {
  const stdio = execOpts.stdio !== undefined ? execOpts.stdio : 'pipe';
  return execFileSync(openclawCmd(), args, {
    encoding: 'utf-8',
    stdio,
    ...execOpts,
  });
}


// ==================== SESSION MANAGEMENT ====================
const SESSION_FILE = os.homedir() + '/.openclaw/workspace/skills/loveclaw/sessions.json';
let userSessions = new Map(); // userId -> { state, data }
let idMap = {}; // phone -> userId

// Session states
const UserState = {
  NONE: 0,
  PHONE: 1,      // waiting for phone
  NAME: 2,      // waiting for name
  GENDER: 3,    // waiting for gender
  PREFERRED_GENDER: 4,
  BIRTH_DATE: 5,
  BIRTH_HOUR: 6,
  CITY: 7,
  PHOTO: 8,
  NOTIFY_PREF: 9,
  CONFIRM: 10,
};

// ==================== CRON AUTO-SETUP ====================

function loveclawScriptsDir() {
  return path.join(os.homedir(), '.openclaw', 'workspace', 'skills', 'loveclaw', 'scripts');
}

/** shell 单引号内安全的路径片段（避免 ~ 在 cron 执行环境中未展开） */
function shSingleQuoted(p) {
  return `'${String(p).replace(/'/g, "'\\''")}'`;
}

function normalizeDeliveryTo(channelInput, userId) {
  const channel = String(channelInput || '').trim().toLowerCase();
  const id = String(userId || '').trim();
  if (!id) return id;

  if (channel === 'feishu') {
    if (id.startsWith('user:') || id.startsWith('chat:')) return id;
    if (id.startsWith('ou_')) return `user:${id}`;
    if (id.startsWith('oc_')) return `chat:${id}`;
    return `chat:${id}`;
  }

  if (channel === 'whatsapp') {
    if (id.startsWith('+')) return id;
    if (/^1\d{10}$/.test(id)) return `+86${id}`;
    return id;
  }

  // telegram / wechat / discord / generic
  return id;
}

/**
 * 为单个用户创建晚间报告 cron
 */
function setupCronJobForUser(channel, userId, jobName) {
  try {
    let cronList = { jobs: [] };
    try {
      const output = openclawExec(['cron', 'list', '--json']);
      cronList = JSON.parse(output);
    } catch (e) {
      console.log('[CronSetup] 检查现有任务失败:', e.message);
    }
    
    // 检查是否已存在同名任务
    const exists = cronList.jobs.some(j => j.name === jobName);
    if (exists) {
      console.log(`[CronSetup] 任务 ${jobName} 已存在，跳过`);
      return;
    }
    
    const reportJs = path.join(loveclawScriptsDir(), 'cloud-cron.js');
    const reportHint =
      `执行晚间匹配报告：node ${reportJs} report。日志中【REPORTS_JSON】内 payload.version===2 时，请按 deliveries[] 逐项用 message 工具推送：若 delivery.imageUrl 存在，先把该 URL 原样发送给对应 channel/target/openId，再发送 delivery.message 原文；若无 imageUrl 则仅发送 delivery.message。勿改写文案。`;
    const toVal = normalizeDeliveryTo(channel, userId);
    openclawExec(
      [
        'cron',
        'add',
        '--name',
        jobName,
        '--cron',
        '0 20 * * *',
        '--tz',
        'Asia/Shanghai',
        '--message',
        reportHint,
        '--announce',
        '--channel',
        channel,
        '--to',
        toVal,
      ],
      { stdio: 'pipe' }
    );
    console.log(`[CronSetup] 已为用户创建 cron: ${jobName}`);
  } catch (e) {
    console.error('[CronSetup] 创建用户 cron 失败:', e.message);
  }
}

/**
 * 删除指定用户的晚间报告 cron
 */
function removeCronJobForUser(userId) {
  try {
    const jobName = `LoveClaw-晚间报告-${userId}`;
    let cronList = { jobs: [] };
    try {
      const output = openclawExec(['cron', 'list', '--json']);
      cronList = JSON.parse(output);
    } catch (e) {
      console.log('[CronSetup] 检查现有任务失败:', e.message);
    }
    
    const job = cronList.jobs.find(j => j.name === jobName);
    if (job) {
      openclawExec(['cron', 'remove', String(job.id)], { stdio: 'pipe' });
      console.log(`[CronSetup] 已删除用户 cron: ${jobName}`);
    }
  } catch (e) {
    console.error('[CronSetup] 删除用户 cron 失败:', e.message);
  }
}

/**
 * 必须同步执行：OpenClaw 常以短生命周期子进程调用 handleMessage，若用 setImmediate
 * 在 return 后进程即退出，则 openclaw cron 从未注册（每日匹配 / 晚间报告丢失）。
 */
function scheduleSetupCronJobs(channel = 'feishu') {
  try {
    setupCronJobs(channel || 'feishu');
  } catch (e) {
    console.error('[CronSetup] setupCronJobs:', e.message);
  }
}

function scheduleSetupCronJobForUser(channel, userId, jobName) {
  try {
    setupCronJobForUser(channel, userId, jobName);
  } catch (e) {
    console.error('[CronSetup] setupCronJobForUser:', e.message);
  }
}

function setupCronJobs(channel = 'feishu', target = '') {
  try {
    // 检查现有 cron 任务
    let cronList = { jobs: [] };
    try {
      const output = openclawExec(['cron', 'list', '--json']);
      cronList = JSON.parse(output);
    } catch (e) {
      // 如果没有 cron list 输出，继续尝试注册
      console.log('[CronSetup] 检查现有任务失败，继续注册:', e.message);
    }

    // 检查每日匹配任务是否存在
    const hasDailyMatch = cronList.jobs.some(j => j.name === 'LoveClaw-每日匹配');
    if (!hasDailyMatch) {
      try {
        const dir = loveclawScriptsDir();
        const dailyCmd = `cd ${shSingleQuoted(dir)} && node cloud-cron.js match`;
        openclawExec(
          [
            'cron',
            'add',
            '--name',
            'LoveClaw-每日匹配',
            '--cron',
            '50 19 * * *',
            '--tz',
            'Asia/Shanghai',
            '--message',
            dailyCmd,
            '--session',
            'isolated',
            '--no-deliver',
          ],
          { stdio: 'pipe' }
        );
        console.log(`[CronSetup] 每日匹配任务已注册 (channel: ${channel})`);
      } catch (e) {
        const stderr = e.stderr?.toString?.() || '';
        console.error('[CronSetup] 注册每日匹配任务失败:', e.message, stderr);
      }
    }

    // 晚间报告任务改为 per-user，在用户开启推送时单独创建
  } catch (e) {
    // 静默失败，不影响正常流程
    console.log('[CronSetup] 定时任务自动注册失败:', e.message);
  }
}

// Load sessions from file
function loadSessionsFromFile() {
  try {
    const dataStr = fs.readFileSync(SESSION_FILE, 'utf-8');
    const loaded = JSON.parse(dataStr);
    delete loaded._idMap;
    loaded._idMap = JSON.parse(dataStr)._idMap || {};
    return loaded;
  } catch {
    return { _idMap: {} };
  }
}

// Save sessions to file
function saveSessionsToFile(sessionList) {
  try {
    const allData = loadSessionsFromFile();
    for (const { userId, session } of sessionList) {
      if (userId) {
        allData[userId] = session;
      }
    }
    allData._idMap = idMap;
    fs.writeFileSync(SESSION_FILE, JSON.stringify(allData, null, 2));
  } catch (e) {
    console.error('Save error:', e.message);
  }
}

// Get or create user session - NEVER overwrites existing session data
function getUserSession(userId) {
  if (userSessions.has(userId)) {
    return userSessions.get(userId);
  }
  // New user - load from file
  const loaded = loadSessionsFromFile();
  const idMapLoad = loaded._idMap || {};
  delete loaded._idMap;
  for (const [k, v] of Object.entries(loaded)) {
    v._idMap = idMapLoad[k];
    userSessions.set(k, v);
  }
  // 与磁盘上的 _idMap 同步，否则首次 save 会用内存里的 {} 覆盖掉已持久化的 phone→userId 映射
  Object.assign(idMap, idMapLoad);
  if (idMapLoad[userId] && userSessions.has(idMapLoad[userId])) {
    return userSessions.get(idMapLoad[userId]);
  } else if (userSessions.has(userId)) {
    return userSessions.get(userId);
  }
  const newSession = { state: UserState.NONE, data: {} };
  userSessions.set(userId, newSession);
  return newSession;
}

/** 从消息中解析可由云函数 fetch 的图片 URL（Markdown、飞书/ Lark 域名等） */
function extractLikelyImageUrl(message) {
  if (!message || typeof message !== 'string') return null;
  const trimmed = message.trim();
  const md = trimmed.match(/!\[[^\]]*\]\((https?:\/\/[^)\s]+)\)/);
  if (md) return md[1].replace(/&amp;/g, '&');
  const urls = trimmed.match(/https?:\/\/[^\s\])'"<>]+/g);
  if (!urls) return null;
  for (let u of urls) {
    u = u.replace(/[.,;)\]'"<>]+$/g, '');
    if (/\.(jpe?g|png|gif|webp|bmp)(\?|$)/i.test(u)) return u;
    if (/open\.feishu|feishu\.cn|larksuite|internal-api-drive|open\.larksuite|sf3-cn|internal-api-im/i.test(u)) {
      return u;
    }
  }
  return null;
}

function expandUserPath(p) {
  if (!p || typeof p !== 'string') return p;
  if (p.startsWith('~/')) return path.join(os.homedir(), p.slice(2));
  if (p === '~') return os.homedir();
  return p;
}

/**
 * 解析 OpenClaw 注入的 [media attached…] 行中的本地路径（飞书下载后的临时文件）。
 * 兼容：[media attached: p (mime) | p]、[media attached 1/2: …]、以及首行 [media attached: N files]。
 */
function extractMediaAttachedLocalPaths(message) {
  if (!message || typeof message !== 'string') return [];
  const out = [];
  const lines = message.split(/\r?\n/);
  const multiOnly = /^\[media attached:\s*\d+\s+files]\s*$/i;
  for (const raw of lines) {
    const line = raw.trim();
    if (!line.startsWith('[')) continue;
    if (multiOnly.test(line)) continue;
    const m = line.match(/^\[media attached(?:\s+\d+\/\d+)?:\s*(.+)]\s*$/);
    if (!m) continue;
    let rest = m[1].trim();
    const parenIdx = rest.indexOf(' (');
    const beforePipe = parenIdx === -1 ? rest : rest.slice(0, parenIdx);
    const candidate = expandUserPath(beforePipe.split(/\s+\|/)[0].trim());
    if (!candidate || /^\d+$/.test(candidate)) continue;
    out.push(candidate);
  }
  return out;
}

/** OpenClaw 工具链常用单独一行 MEDIA:`path`（非 URL） */
function parseMediaLineLocalPath(message) {
  if (!message || typeof message !== 'string') return '';
  for (const line of message.split(/\r?\n/)) {
    const t = line.trim();
    if (!t.toLowerCase().startsWith('media:')) continue;
    let raw = t.slice(6).trim();
    const bt = raw.match(/^`([^`]+)`$/);
    if (bt) raw = bt[1];
    if (raw.startsWith('http://') || raw.startsWith('https://')) continue;
    const p = expandUserPath(raw);
    if (p && fs.existsSync(p)) return p;
  }
  return '';
}

/**
 * 云端是否像「已完成报名」：仅主键 userId、无任何业务列时视为未建档。
 * 控制台若只清属性未删主键，getProfile 仍 200，会导致误判「已报名」。
 */
function profileLooksRegistered(p) {
  if (!p || typeof p !== 'object') return false;
  const keys = ['name', 'gender', 'birthDate', 'city', 'preferredGender', 'photoOssUrl', 'baziYear', 'notifyEnabled'];
  return keys.some((k) => {
    const v = p[k];
    return v != null && String(v).trim() !== '';
  });
}

// ==================== HANDLER ====================

/**
 * @param {string} userId - User identifier
 * @param {string} message - User message
 * @param {string} channel - User's channel (feishu/webchat/etc), defaults to webchat
 * @param {string} mediaPath - Optional local file path for media attachments
 */
async function handleMessage(userId, message, channel = 'webchat', mediaPath = '') {
  const session = getUserSession(userId);
  
  // Ensure channel is stored in session for notification routing
  if (channel && !session.data.channel) {
    session.data.channel = channel;
  }
  
  try {
    // 渠道偶发首尾空白；宿主或用户有时带「技能」后缀（与代码字面量不一致会导致未进入报名）
    const msg = typeof message === 'string' ? message.trim() : String(message ?? '');
    const isStartLoveclaw = msg === '启动爱情龙虾' || msg === '启动爱情龙虾技能';

    // ==================== 全局命令（任何状态都响应） ====================
    // 今日匹配：按时段返回查询指引或完整晚间报告
    if (msg === '今日匹配') {
      const phoneOrId = String(session.data.phone || userId);
      const profile = await cloudData.getProfile(phoneOrId).catch(() => null);
      if (!profile) {
        return { text: '你还没有报名，请先发送「启动爱情龙虾」' };
      }

      const shHour = getShanghaiHour();
      if (shHour < 20) {
        return {
          text:
            '⏰ 今日匹配结果将在今晚 20:00 后生成并可查询。\n' +
            '请在 20:00 后再输入「今日匹配」。\n\n' +
            '如果你想先看历史结果，可输入「匹配记录」。',
        };
      }

      const report = await cloudData.getMyReport(phoneOrId);
      if (report.status === 'matched' && report.message) {
        return { text: report.message };
      }

      if (report.status === 'no_match') {
        return { text: report.message || reportTemplates.formatEveningMatchFail(profile.name) };
      }

      return {
        text:
          '🕗 20:00 后再来查一次吧，今日匹配报告还在准备中。\n' +
          '若想查看过往结果，可输入「匹配记录」。',
      };
    }

    if (msg === '匹配记录') {
      const phoneOrId = session.data.phone || userId;
      const profile = await cloudData.getProfile(phoneOrId);
      if (!profile) return { text: '你还没有报名，请先发送「启动爱情龙虾」' };
      return await formatMatchHistory(profile);
    }

    // 取消报名：任何状态都可以取消
    if (msg === '取消报名') {
      const phoneOrId = session.data.phone || userId;
      const profile = await cloudData.getProfile(phoneOrId);
      if (!profile) return { text: '你还没有报名，无需取消' };
      await cloudData.deleteProfile(phoneOrId);
      resetUserSession(userId);
      resetUserSession(phoneOrId);
      return { text: '已取消报名，你的所有信息已删除。如需重新报名，请发送「启动爱情龙虾」。' };
    }
    
    // 开启/关闭每日推送
    if (msg === '开启推送' || msg === '关闭推送') {
      const phoneOrId = session.data.phone || userId;
      const profile = await cloudData.getProfile(phoneOrId);
      if (!profile) return { text: '你还没有报名，请先发送「启动爱情龙虾」' };
      
      const enable = msg === '开启推送';
      await cloudData.updateProfile(phoneOrId, { notifyEnabled: enable ? '1' : '0' });
      
      if (enable) {
        // 创建 per-user cron
        const userChannel = profile.channel || 'feishu';
        const cronJobName = `LoveClaw-晚间报告-${userId}`;
        scheduleSetupCronJobForUser(userChannel, userId, cronJobName);
        return { text: '✅ 已开启每日推送，每晚 20:00 将推送匹配结果到你的频道' };
      } else {
        // 删除该用户的 cron
        removeCronJobForUser(userId);
        return { text: '❌ 已关闭每日推送，可随时输入「今日匹配」查询' };
      }
    }
    
    // ==================== STATE: NONE (start) ====================
    if (session.state === UserState.NONE) {
      if (isStartLoveclaw) {
        session.state = UserState.PHONE;
        saveSessionsToFile([{ userId, session }]);
        // 尽早注册全局「每日匹配」cron（幂等）；异步执行以免 openclaw cron 阻塞首条回复（常数秒）
        scheduleSetupCronJobs(channel || session.data.channel || 'feishu');
        return { text: '请输入你的手机号（用于登录和匹配通知）' };
      }
      if (msg === '我的档案' || msg === '查看档案') {
        const phoneOrId = session.data.phone || userId;
        const profile = await cloudData.getProfile(phoneOrId);
        if (!profile) return { text: '你还没有报名，请先发送「启动爱情龙虾」' };
        return await formatProfile(profile);
      }
      return { text: '发送「启动爱情龙虾」开始缘分匹配，或「我的档案」查看个人信息' };
    }

    // ==================== PHONE ====================
    // 允许在任何非 NONE 状态重新开始
    if (isStartLoveclaw && session.state !== UserState.NONE) {
      session.state = UserState.PHONE;
      session.data = { channel: session.data.channel };
      saveSessionsToFile([{ userId, session }]);
      scheduleSetupCronJobs(channel || session.data.channel || 'feishu');
      return { text: '请输入你的手机号（用于登录和匹配通知）' };
    }
    if (/^1\d{10}$/.test(msg) && session.state === UserState.PHONE) {
      const existing = await cloudData.getProfile(msg).catch(() => null);
      if (existing && profileLooksRegistered(existing)) {
        // 已注册：先问每日推送（与新用户一致），再进入 CONFIRM 看摘要
        const existingNotifyEnabled = existing.notifyEnabled;
        session.data = { ...existing, phone: msg };
        if (session.data.notifyEnabled === undefined && existingNotifyEnabled !== undefined) {
          session.data.notifyEnabled = existingNotifyEnabled;
        }
        session.state = UserState.NOTIFY_PREF;
        saveSessionsToFile([{ userId, session }]);
        return {
          text:
            '📱 检测到该手机号已报名。\n\n' +
            '📬 是否开启每日匹配结果推送？\n每晚 20:00 将推送匹配结果到当前频道。\n\n' +
            '回复「是」开启，「否」关闭。\n' +
            '选择后将显示你的档案摘要；无误请回复「确认」，若要改资料可按摘要下方说明操作。'
        };
      }
      session.data.phone = msg;
      // Keep BOTH keys (old userId AND phone) so subsequent messages from either ID work
      const oldUserId = [...userSessions.entries()].find(([k, v]) => v === session)?.[0];
      if (oldUserId && oldUserId !== msg) {
        idMap[msg] = oldUserId; // phone -> original userId
        userSessions.set(msg, session); // also store under phone
        // Do NOT delete old key - keep both mappings active
      }
      session.state = UserState.NAME;
      saveSessionsToFile([{ userId, session }]);
      return { text: `手机号 ${msg} 已绑定\n请输入你的姓名（或昵称）` };
    }

    // ==================== NAME ====================
    if (session.state === UserState.NAME) {
      session.data.name = message;
      session.state = UserState.GENDER;
      saveSessionsToFile([{ userId, session }]);
      return { text: '请选择你的性别：男 / 女' };
    }

    // ==================== GENDER ====================
    if (session.state === UserState.GENDER) {
      if (!['男', '女'].includes(message)) {
        return { text: '请回复「男」或「女」' };
      }
      session.data.gender = message;
      session.state = UserState.PREFERRED_GENDER;
      saveSessionsToFile([{ userId, session }]);
      return { text: `你的性别是${message}，希望认识什么性别？\n请回复：男 / 女 / 不限` };
    }

    // ==================== PREFERRED GENDER ====================
    if (session.state === UserState.PREFERRED_GENDER) {
      if (!['男', '女', '不限'].includes(message)) {
        return { text: '请回复「男」「女」或「不限」' };
      }
      session.data.preferredGender = message;
      session.state = UserState.BIRTH_DATE;
      saveSessionsToFile([{ userId, session }]);
      return { text: '请输入你的出生日期\n格式：YYYY-MM-DD\n例如：1995-05-20' };
    }

    // ==================== BIRTH DATE ====================
    if (session.state === UserState.BIRTH_DATE) {
      const bdMatch = message.match(/^(\d{4})-(\d{1,2})-(\d{1,2})$/);
      if (!bdMatch) {
        return { text: '日期格式不正确，请使用 YYYY-MM-DD，例如：1995-05-20' };
      }
      const date = new Date(message);
      if (isNaN(date.getTime())) {
        return { text: '日期无效，请检查后重试' };
      }
      session.data.birthDate = message;
      session.data.birthDateObj = date;
      session.state = UserState.BIRTH_HOUR;
      saveSessionsToFile([{ userId, session }]);
      return { text: '请输入出生时辰（0-23）\n请直接输入数字，例如：14（代表下午2点）\n也可输入地支：子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥' };
    }

    // ==================== BIRTH HOUR ====================
    if (session.state === UserState.BIRTH_HOUR) {
      const diZhiMap = { '子': 23, '丑': 1, '寅': 3, '卯': 5, '辰': 7, '巳': 9, '午': 11, '未': 13, '申': 15, '酉': 17, '戌': 19, '亥': 21 };
      const input = message.trim();
      let hour;
      if (/^\d{1,2}$/.test(input) && parseInt(input) >= 0 && parseInt(input) <= 23) {
        hour = parseInt(input);
      } else if (diZhiMap.hasOwnProperty(input)) {
        hour = diZhiMap[input];
      } else {
        return { text: '请输入 0-23 之间的数字，或地支（子丑寅卯辰巳午未申酉戌亥）' };
      }
      session.data.birthHour = hour;
      session.state = UserState.CITY;
      saveSessionsToFile([{ userId, session }]);
      return { text: '请输入你所在城市（例如：上海、北京、深圳）\n注意只写城市名，不要带「市」字' };
    }

    // ==================== CITY ====================
    if (session.state === UserState.CITY) {
      session.data.city = message;
      session.state = UserState.PHOTO;
      saveSessionsToFile([{ userId, session }]);
      return { text: '请发送一张照片用于匹配展示\n（可上传图片，或回复「跳过」不展示照片）' };
    }

    // ==================== PHOTO ====================
    if (session.state === UserState.PHOTO) {
      const pushPrefReply = {
        text: `📬 每日推送设置\n\n是否开启每日匹配结果推送？\n\n回复「是」开启每晚 20:00 自动推送\n回复「否」不推送，可随时输入「今日匹配」查询`,
      };

      // 先解析图片（mediaPath / 飞书 [media attached:…] / URL / base64），再处理「跳过」。
      // 避免极端情况下文案与附件顺序导致误判，确保有本地路径时一定尝试上传。
      let localPath = '';
      const directMedia = mediaPath ? expandUserPath(mediaPath) : '';
      if (directMedia && fs.existsSync(directMedia)) {
        localPath = directMedia;
      } else {
        for (const p of extractMediaAttachedLocalPaths(message)) {
          if (fs.existsSync(p)) {
            localPath = p;
            break;
          }
        }
      }
      if (!localPath) {
        const fromMediaLine = parseMediaLineLocalPath(message);
        if (fromMediaLine) localPath = fromMediaLine;
      }
      if (!localPath) {
        const t = expandUserPath(typeof message === 'string' ? message.trim() : '');
        if (t.startsWith('/') && fs.existsSync(t)) localPath = t;
      }

      let photoInput;
      if (localPath) {
        try {
          const imgBuffer = fs.readFileSync(localPath);
          photoInput = imgBuffer.toString('base64');
          console.log('[PHOTO] read local file:', localPath, 'size:', imgBuffer.length);
        } catch (readErr) {
          console.error('[PHOTO] read file failed:', localPath, readErr.message);
        }
      } else if (message.startsWith('http://') || message.startsWith('https://')) {
        photoInput = message.trim();
      } else if (message.includes('http://') || message.includes('https://')) {
        const u = extractLikelyImageUrl(message);
        if (u) photoInput = u;
      } else if (message.startsWith('data:')) {
        photoInput = message;
      }

      if (photoInput) {
        try {
          const ossUrl = await cloudData.uploadPhoto(session.data.phone || userId, photoInput);
          session.data.photoOssUrl = ossUrl;
          console.log('[PHOTO] 上传成功:', ossUrl);
        } catch (e) {
          console.error('[uploadPhoto error]', e.message);
          return {
            text: `照片上传到云端失败：${e.message}\n请检查 LOVECLAW_API_TOKEN 与网络后重试，或回复「跳过」继续报名（不使用照片）。`,
          };
        }
        session.state = UserState.NOTIFY_PREF;
        saveSessionsToFile([{ userId, session }]);
        return pushPrefReply;
      }

      if (msg === '跳过') {
        delete session.data.photoOssUrl;
        session.state = UserState.NOTIFY_PREF;
        saveSessionsToFile([{ userId, session }]);
        return pushPrefReply;
      }

      console.log('[PHOTO] unrecognized format:', String(message).substring(0, 120));
      return {
        text:
          '未能识别图片：请直接发送一张图片（或带图片附件），也可粘贴以 http 开头的图片链接。\n' +
          '若暂不使用照片，请回复「跳过」。\n' +
          '（若已发图仍失败，多为渠道未把本地路径传给技能，可查看 Gateway 日志中的 [PHOTO]）',
      };
    }

    // ==================== NOTIFY_PREF ====================
    if (session.state === UserState.NOTIFY_PREF) {
      const m = message.trim();
      const yes = ['是', '好的', '要', '开启', '开', '好', '嗯'].includes(m);
      const no = ['否', '不', '不要', '不用', '关闭', '关', '别'].includes(m);
      if (!yes && !no) {
        return { text: '请回复「是」开启每晚推送，或「否」不推送。' };
      }
      session.data.notifyEnabled = yes;
      session.state = UserState.CONFIRM;
      saveSessionsToFile([{ userId, session }]);
      return formatSummary(session.data);
    }

    // ==================== CONFIRM ====================
    if (msg === '确认' && session.state === UserState.CONFIRM) {
      // Channel from the current call's parameter (most reliable)
      const notifyChannel = session.data.channel || channel || 'webchat';
      try {
        // Calculate bazi
        const baziResult = bazi.calculateBazi(session.data.birthDate, session.data.birthHour);
        const profile = {
          ...session.data,
          userId: session.data.phone, // phone as primary ID
          channel: notifyChannel, // USE THE CHANNEL FROM SESSION (set during registration flow)
          openId: userId, // Feishu open_id for notification routing
          bazi: baziResult,
          createdAt: new Date().toISOString(),
          todayMatchDone: false,
          todayMatchDate: '',
          matchedWith: '',
          matchedWithHistory: []
        };
        // 重试一次应对偶发 412/网络抖动
        let saveErr;
        for (let i = 0; i < 2; i++) {
          try { await cloudData.saveProfile(profile); saveErr = null; break; }
          catch (e) { saveErr = e; await new Promise(r => setTimeout(r, 1500)); }
        }
        if (saveErr) return { text: `保存遇到网络问题，请再回复一次「确认」重试` };
        
        // 注册成功后为用户创建 per-user cron（如果开启了推送）
        if (session.data.notifyEnabled) {
          const cronChannel = session.data.channel || 'feishu';
          scheduleSetupCronJobForUser(cronChannel, userId, `LoveClaw-晚间报告-${userId}`);
        }
        
        // Clear session
        const phone = session.data.phone;
        saveSessionsToFile([{ userId, session: { state: UserState.NONE, data: { phone } } }]);
        delete idMap[phone];
        userSessions.delete(userId);
        userSessions.delete(phone);
        
        // 自动创建每日匹配 cron（全局，所有用户共用）
        scheduleSetupCronJobs(session.data.channel || 'feishu');
        
        const notifyText = session.data.notifyEnabled
          ? '✅ 已开启每晚 20:00 推送，匹配结果将自动通知你'
          : '❌ 未开启推送，可随时发送「我的档案」查询';
        return {
          text: `报名成功！🎉\n\n已将你的信息纳入匹配队列，每日19:50自动匹配。\n${notifyText}\n\n💡 温馨提示：\n- 输入「我的档案」可查看个人信息和匹配记录\n- 输入「开启推送」可重新开启每日推送\n- 输入「取消报名」可删除云端档案与匹配记录，并清除你上传的照片；删除后如需参与匹配请重新发送「启动爱情龙虾」报名。输入「今日匹配」可在未开启每日推送匹配报告的情况下自主查询，同时，如部分用户出现报告未成功投递的情况，也可通过「今日匹配」主动查询。\n- 任务说明：关闭「每日匹配」后将不再生成新的匹配结果；关闭「每日报告」仅影响自动推送，你仍可通过「今日匹配」手动查询当日结果。`
        };
      } catch (e) {
        return { text: `保存遇到网络问题，请再回复一次「确认」重试` };
      }
    }

    // CONFIRM not matched but session is CONFIRM - show summary again
    if (session.state === UserState.CONFIRM) {
      return formatSummary(session.data);
    }

    // Fallback
    return { text: '请完成当前步骤，或发送「启动爱情龙虾」重新开始' };

  } catch (e) {
    return { text: '处理出错: ' + e.message };
  }
}

function formatSummary(data) {
  const genderText = data.gender === '男' ? '女性' : '男性';
  const bd = data.birthDate;
  const hour = data.birthHour;
  const baziPreview = tryBazi(data);
  return {
    text: `📋 信息确认\n\n姓名：${data.name}\n性别：${data.gender}，希望认识：${data.preferredGender}\n生日：${bd} ${data.birthHour}时\n城市：${data.city}\n${baziPreview}\n\n以上信息确认无误？确认报名请回复「确认」，修改请重新发送对应信息。`
  };
}

function tryBazi(data) {
  try {
    const result = bazi.calculateBazi(data.birthDate, data.birthHour);
    return `八字：${result.year}年 ${result.month}月 ${result.day}日 ${result.hour}时`;
  } catch {
    return '';
  }
}

/**
 * 根据 matchedWithHistory 中的 userId 查到对方姓名
 */
async function getPartnerName(userId) {
  try {
    const partner = await cloudData.getProfile(userId);
    return partner ? partner.name : null;
  } catch {
    return null;
  }
}

async function formatProfile(profile) {
  let baziStr = '未知';
  if (profile.bazi && profile.bazi.year) {
    baziStr = `${profile.bazi.year}年 ${profile.bazi.month}月 ${profile.bazi.day}日 ${profile.bazi.hour}时`;
  } else if (profile.baziYear) {
    baziStr = `${profile.baziYear}年 ${profile.baziMonth}月 ${profile.baziDay}日 ${profile.baziHour || ''}时`;
  }

  const matched = profile.matchedWithHistory || [];
  let matchedList = '暂无';
  if (matched.length > 0) {
    const items = await Promise.all(
      matched.map(async (m) => {
        const name = await getPartnerName(m.userId);
        const nameStr = name ? `${name}（${m.userId}）` : `（${m.userId}）`;
        const scoreStr = m.compatibility ? ` ${m.compatibility}分` : '';
        const dateStr = m.date ? ` ${m.date}` : '';
        return `  • ${nameStr}${scoreStr}${dateStr}`;
      })
    );
    matchedList = items.join('\n');
  }

  return {
    text: `📋 你的档案\n\n姓名：${profile.name}\n性别：${profile.gender}，喜欢：${profile.preferredGender}\n生日：${profile.birthDate} ${profile.birthHour}时\n城市：${profile.city}\n八字：${baziStr}\n\n匹配历史：\n${matchedList}\n\n发送「启动爱情龙虾」可重新报名`
  };
}

async function formatMatchHistory(profile) {
  const matched = profile.matchedWithHistory || [];
  if (matched.length === 0) {
    return { text: '你还没有历史匹配记录，今晚 20:00 后可输入「今日匹配」查看当日结果。' };
  }
  const items = await Promise.all(
    matched.map(async (m, idx) => {
      const name = await getPartnerName(m.userId);
      const nameStr = name ? `${name}（${m.userId}）` : `（${m.userId}）`;
      const scoreStr = m.compatibility ? ` ${m.compatibility}分` : '';
      const dateStr = m.date ? ` ${m.date}` : '';
      return `${idx + 1}. ${nameStr}${scoreStr}${dateStr}`;
    })
  );
  return {
    text: `📚 匹配记录\n\n${items.join('\n')}\n\n💡 输入「今日匹配」可查看今日结果（20:00 后）`
  };
}

function getShanghaiHour() {
  const parts = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Asia/Shanghai',
    hour12: false,
    hour: '2-digit',
  }).formatToParts(new Date());
  const hourPart = parts.find(p => p.type === 'hour');
  return hourPart ? Number(hourPart.value) : 0;
}

function buildBaziObject(profile) {
  if (profile?.bazi && typeof profile.bazi === 'object' && profile.bazi.yearGan) {
    return profile.bazi;
  }
  return {
    yearGan: profile?.baziYearGan || profile?.baziYear?.replace(profile?.baziYearZhi || '', '') || '',
    yearZhi: profile?.baziYearZhi || profile?.baziYear?.slice(-1) || '',
    monthGan: profile?.baziMonthGan || profile?.baziMonth?.replace(profile?.baziMonthZhi || '', '') || '',
    monthZhi: profile?.baziMonthZhi || profile?.baziMonth?.slice(-1) || '',
    dayGan: profile?.baziDayGan || profile?.baziDay?.replace(profile?.baziDayZhi || '', '') || '',
    dayZhi: profile?.baziDayZhi || profile?.baziDay?.slice(-1) || '',
    hourGan: profile?.baziHourGan || profile?.baziHour?.replace(profile?.baziHourZhi || '', '') || '',
    hourZhi: profile?.baziHourZhi || profile?.baziHour?.slice(-1) || '',
  };
}

function hasValidBazi(profile) {
  if (!profile) return false;
  const b = buildBaziObject(profile);
  return b.yearGan && b.yearZhi && b.monthGan && b.monthZhi && b.dayGan && b.dayZhi && b.hourGan && b.hourZhi;
}

function resetUserSession(userId) {
  userSessions.delete(userId);
}

// 定时任务由 SKILL.md 初始化规则注册（agent 执行 openclaw cron add）

module.exports = {
  handleMessage,
  resetUserSession,
  getUserSession: (uid) => userSessions.get(uid),
};
