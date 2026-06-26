/**
 * hike-planner.js - State Machine + Command Handlers
 *
 * 6 条主命令:cmdInit / cmdStatus / cmdToday / cmdLog / cmdList / cmdSet
 * Agent 通过 module.exports 调用各函数,逐步填充 TripPlan,最终生成 出行计划文档。
 *
 * v1.2.0
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

// ── 常量 ──────────────────────────────────────────────

const DEFAULT_OUTPUT_DIR = path.join(__dirname, '..', 'planner');
const STATE_FILE_NAME = '.hike-planner-state.json';
const TEMPLATE_NAME = 'PLAN_TEMPLATE.md';
const CONFIG_DIR = path.join(__dirname, '..', 'planner');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

const STATUS = {
  IDLE: 'IDLE',
  COLLECTING: 'COLLECTING',
  PLANNING: 'PLANNING',
  CONFIRMED: 'CONFIRMED',
  ACTIVE: 'ACTIVE',
  COMPLETED: 'COMPLETED',
};

const WEEKDAYS = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];

// 节点实际状态
const NODE_STATUS = {
  COMPLETED: 'completed',   // ✅ 完成
  CHANGED: 'changed',       // 🔄 变更
  SKIPPED: 'skipped',       // ❌ 跳过
  PENDING: 'pending',       // ⏸️ 待定
};

const NODE_STATUS_ICONS = {
  completed: '✅',
  changed: '🔄',
  skipped: '❌',
  pending: '⏸️',
};

// 偏差阈值
const DEVIATION_THRESHOLDS = {
  timeMinutes: 30,    // 时间偏差 > 30min 提醒
  costYuan: 50,       // 费用偏差 > ¥50 提醒
};

// ── 订单短信解析正则 ──────────────────────────────

const SMS_PATTERNS = {
  // 12306 火车票订单短信
  // "您的订单D2008,成都东07:50-剑门关09:21,二等座01车02A号,订单E123456789"
  // "订单号E123456789,车次D2008,成都东07:50-剑门关09:21,二等座01车02A号"
  train: [
    // 模式1: 订单+车次号 直接格式(12306 常见:您的订单D2008,成都东07:50-剑门关09:21,二等座...)
    /订单\s*([GCKDTZYL]\d+)(?:次)?[,,、\s]*([\u4e00-\u9fa5]+?(?:东|南|西|北|关|桥|口|岭|站)?)\s*(\d{1,2}:\d{2})[--~至到]\s*([\u4e00-\u9fa5]+?(?:东|南|西|北|关|桥|口|岭|站)?)\s*(\d{1,2}:\d{2})[,,、\s]*([\u4e00-\u9fa5]+座\d*车?\d*[号座FABC]?\d*).*?订单[号编]?\s*([A-Za-z0-9]+)/,
    // 模式2: 车次 + 出发站时间-到达站时间 + 座位 + 订单号
    /车次\s*([GCKDTZYL]\d+).*?([\u4e00-\u9fa5]+?(?:东|南|西|北|关|桥|口|岭|站)?)\s*(\d{1,2}:\d{2})\s*[--~至到]\s*([\u4e00-\u9fa5]+?(?:东|南|西|北|关|桥|口|岭|站)?)\s*(\d{1,2}:\d{2}).*?([\u4e00-\u9fa5]+座?(?:\d+车\d+[号座FABC]?\d*)?).*?订单[号编]?\s*([A-Za-z0-9]+)/,
    // 模式3: 订单号 + 车次 变体
    /订单[号编]?\s*([A-Za-z0-9]+).*?车次\s*([GCKDTZYL]\d+).*?([\u4e00-\u9fa5]+?(?:东|南|西|北|关|桥|口|岭|站)?)\s*(\d{1,2}:\d{2})\s*[--~至到]\s*([\u4e00-\u9fa5]+?(?:东|南|西|北|关|桥|口|岭|站)?)\s*(\d{1,2}:\d{2}).*?([\u4e00-\u9fa5]+座)/,
  ],
  // 航司/机票订单短信
  // "航班CA1234,北京-成都,2026-05-13 08:00-10:30,经济舱,订单FL9876543"
  flight: [
    /航班\s*([A-Z]{2}\d+).*?([\u4e00-\u9fa5]+)\s*[--~至到]\s*([\u4e00-\u9fa5]+).*?(\d{4}-\d{2}-\d{2})\s*(\d{1,2}:\d{2})\s*[--~至到]\s*(\d{1,2}:\d{2}).*?([\u4e00-\u9fa5]+舱).*?订单[号编]?\s*([A-Za-z0-9]+)/,
    /订单[号编]?\s*([A-Za-z0-9]+).*?航班\s*([A-Z]{2}\d+).*?([\u4e00-\u9fa5]+)\s*[--~至到]\s*([\u4e00-\u9fa5]+).*?(\d{4}-\d{2}-\d{2})\s*(\d{1,2}:\d{2})\s*[--~至到]\s*(\d{1,2}:\d{2})/,
  ],
  // 酒店订单短信
  // "XX宾馆已预订,入住2026-05-14,退房2026-05-16,标准间含双早,订单H123456"
  hotel: [
    /([\u4e00-\u9fa5]+(?:酒店|宾馆|客栈|民宿|饭店|公寓|旅社))[,,已]*(?:已)?预订[成已]?功?.{0,10}入住[日时]?(?:间)?[::]?\s*(\d{4}-\d{2}-\d{2}).{0,10}(?:退[房住]|离店)[日时]?(?:间)?[::]?\s*(\d{4}-\d{2}-\d{2}).*?([\u4e00-\u9fa5]+(?:房|间)).*?订单[号编]?\s*([A-Za-z0-9]+)/,
    /订单[号编]?\s*([A-Za-z0-9]+).*?([\u4e00-\u9fa5]+(?:酒店|宾馆|客栈|民宿|饭店|公寓|旅社)).*?入住[日时]?(?:间)?[::]?\s*(\d{4}-\d{2}-\d{2}).*?(?:退[房住]|离店)[日时]?(?:间)?[::]?\s*(\d{4}-\d{2}-\d{2}).*?([\u4e00-\u9fa5]+(?:房|间))/,
    // 简化: 酒店名 + 入住日期范围内 days
    /([\u4e00-\u9fa5]+(?:酒店|宾馆|客栈|民宿|饭店|公寓|旅社)).*?(\d{4}-\d{2}-\d{2}).*?([\u4e00-\u9fa5]+(?:房|间)).*?订单[号编]?\s*([A-Za-z0-9]+)/,
  ],
};

/**
 * 获取节点的交通标签(用于时间线展示)
 * 徒步节点 → "🥾 徒步"
 * taxi/car → "🚗 包车"
 * bus → "🚌 公交"
 * train → "🚄 火车"
 * flight → "✈️ 飞机"
 * metro → "🚇 地铁"
 */
function getNodeTransportLabel(node) {
  const labelMap = {
    hiking: '🥾 徒步',
    taxi: '🚗 包车',
    car: '🚗 自驾',
    selfdrive: '🚗 自驾',
    bus: '🚌 公交',
    train: '🚄 火车',
    flight: '✈️ 飞机',
    metro: '🚇 地铁',
    hotel: '🏨 入住',
    food: '🍴 餐饮',
    rest: '💤 休息',
    sightseeing: '📸 游览',
    other: '📍 其他',
  };
  return labelMap[node.type] || `📍 ${node.type || '其他'}`;
}

/**
 * 为某一天的节点生成路线类型列表(逗号分隔),供地图渲染脚本使用
 * 在相邻节点间生成一段路线,根据两个节点的类型决定路线类型:
 * - 如果前后都是 hiking 节点 → walking
 * - 包车/出租/自驾之间 → driving
 * - 火车/飞机到达后到下一节点之间 → driving(接驳段)
 * - 火车/飞机出发前的节点 → driving(送站段)
 *
 * @returns {object} { routeTypes: string, segments: [{from,to,routeType}] }
 */
function getRouteTypesForDay(day) {
  const nodes = day.nodes;
  if (nodes.length < 2) return { routeTypes: '', segments: [] };

  const segments = [];
  for (let i = 0; i < nodes.length - 1; i++) {
    const a = nodes[i];
    const b = nodes[i + 1];
    let routeType = 'driving';

    // 如果两端都是徒步 → walking
    if (a.type === 'hiking' && b.type === 'hiking') {
      routeType = 'walking';
    }
    // 如果任一端是徒步(开始/结束徒步的接驳段)→ driving
    else if (a.type === 'hiking' || b.type === 'hiking') {
      routeType = 'driving';
    }
    // 火车/飞机段 → straight
    else if ((a.type === 'train' || a.type === 'flight') &&
             (b.type === 'train' || b.type === 'flight')) {
      routeType = 'straight';
    }
    // 从火车/飞机下来后 → driving(接驳)
    else if (a.type === 'train' || a.type === 'flight') {
      routeType = 'driving';
    }
    // 去往火车/飞机前 → driving(送站)
    else if (b.type === 'train' || b.type === 'flight') {
      routeType = 'driving';
    }
    // 其他按节点类型
    else {
      routeType = getNodeRouteType(a.type) === 'walking' ? 'walking' : getNodeRouteType(a.type);
    }

    segments.push({
      from: a.name,
      to: b.name,
      routeType: routeType,
    });
  }

  const routeTypes = segments.map(s => s.routeType).join(',');
  return { routeTypes, segments };
}

// ── 工具函数 ──────────────────────────────────────────

function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
    }
  } catch (e) {
    // ignore
  }
  return { outputDir: '', webBaseUrl: 'http://localhost' };
}

function saveConfig(config) {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf8');
}

function getOutputDir(options) {
  // 优先级:options.outputDir > hike-select 保存的 > DEFAULT_OUTPUT_DIR
  if (options && options.outputDir) return options.outputDir;
  const config = loadConfig();
  if (config.outputDir) return config.outputDir;
  return DEFAULT_OUTPUT_DIR;
}

function getStatePath(outputDir) {
  return path.join(outputDir, STATE_FILE_NAME);
}

function formatDate(dateStr) {
  const d = new Date(dateStr + 'T00:00:00+08:00');
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${m}/${day}`;
}

function formatFullDate(dateStr) {
  const d = new Date(dateStr + 'T00:00:00+08:00');
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`;
}

function getWeekday(dateStr) {
  const d = new Date(dateStr + 'T00:00:00+08:00');
  return WEEKDAYS[d.getDay()];
}

function getToday() {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function generateTripId(destination, startDate, slug) {
  const s = slug || destination
    .replace(/[\u4e00-\u9fa5]/g, '')        // strip Chinese chars
    .replace(/[^a-zA-Z0-9-]/g, '')           // keep alphanumeric + hyphen
    .toLowerCase()
    .replace(/-+/g, '-')                      // collapse consecutive hyphens
    .replace(/^-|-$/g, '');                   // trim leading/trailing hyphens
  const date = startDate.substring(0, 7);    // YYYY-MM
  return s ? `${s}-${date}` : date;
}

/**
 * 根据行程数据生成计划文件名(基于 trip.title 实际标题)
 * 格式: <标题>.md
 * 例: 海坨山姜庄子村小环线出行计划.md、日本·东京→京都→大阪 8天行程规划.md
 */
function getPlanFilename(trip) {
  // 从 trip.title 提取(如不存在则 fallback 到默认标题)
  const h1 = trip.title || `🥾 ${trip.destination || '旅行'}出行计划`;
  const safe = h1
    .replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE00}-\u{FE0F}]/gu, '')  // 去 emoji
    .replace(/[\\/:*?"<>|]/g, '')           // 仅去非法文件名字符,保留 ·→空格中文等
    .trim();
  return safe + '.md';
}

function dateDiff(a, b) {
  return Math.round((new Date(b + 'T00:00:00+08:00') - new Date(a + 'T00:00:00+08:00')) / 86400000);
}

// ── 状态读写 ──────────────────────────────────────────

function loadState(outputDir) {
  const filePath = getStatePath(outputDir);
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, 'utf8'));
    }
  } catch (e) {
    // ignore
  }
  return { status: STATUS.IDLE, trips: {} };
}

/**
 * 加载状态,优先使用配置的输出目录,若无活跃行程则回退到默认目录。
 * 保证 hike-select 切换输出目录后,cmdLog/cmdStatus/cmdToday 仍能找到之前创建的行程。
 */
function loadStateWithFallback() {
  const configuredDir = getOutputDir();
  const state = loadState(configuredDir);
  if (state.activeTripId && state.trips[state.activeTripId]) {
    return { state, dir: configuredDir };
  }
  // 回退到默认目录
  if (configuredDir !== DEFAULT_OUTPUT_DIR) {
    const defaultState = loadState(DEFAULT_OUTPUT_DIR);
    if (defaultState.activeTripId && defaultState.trips[defaultState.activeTripId]) {
      return { state: defaultState, dir: DEFAULT_OUTPUT_DIR };
    }
    // 即使没有活跃行程,也合并两个目录的行程
    if (Object.keys(defaultState.trips).length > 0) {
      const merged = { ...defaultState };
      for (const [id, trip] of Object.entries(state.trips)) {
        if (!merged.trips[id]) merged.trips[id] = trip;
      }
      merged.activeTripId = merged.activeTripId || state.activeTripId;
      return { state: merged, dir: configuredDir };
    }
  }
  return { state, dir: configuredDir };
}

function saveState(state, outputDir) {
  const filePath = getStatePath(outputDir);
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(filePath, JSON.stringify(state, null, 2), 'utf8');
}

function getTrip(state, tripId) {
  if (state.activeTripId && tripId == null) {
    return state.trips[state.activeTripId] || null;
  }
  return tripId ? (state.trips[tripId] || null) : null;
}

// ── TripPlan 工厂 ─────────────────────────────────────

function createTripPlan(destination, options) {
  const outputDir = getOutputDir(options);
  const now = new Date().toISOString();
  return {
    tripId: '',
    title: '',
    status: STATUS.COLLECTING,
    destination: destination || '',
    destinationRegion: '',  // 目的地省市区县,用于地理编码消歧义
    dates: { start: '', end: '' },
    origin: '',
    returnTo: '',
    participants: 1,
    preferences: {
      transport: '',
      accommodation: '',
      fitness: '',
      interests: [],
    },
    outputDir: outputDir,
    createdAt: now,
    updatedAt: now,
    days: [],
    hikingRoutes: [],
    culture: {},
    equipment: {},
    todos: [],
    totalBudget: 0,
    mapUrls: [],
    logs: [],
    orderConfirmations: [],   // 已解析的订单短信
    actuals: {
      totalCost: null,
      totalTime: null,
      totalDistance: null,
      notes: [],
      deviations: [],          // 偏差记录 [{ type, node, planned, actual, diff, alert }]
    },
  };
}

// ── 命令:hike(纯查询) ─────────────────────────────

/**
 * 查询目的地介绍 + 经典徒步路线。纯查询模式,不创建行程、不管理状态。
 *
 * @param {string} destination - 目的地(必填)
 * @param {string} [activity] - 活动类型(可选,如 "徒步")
 * @returns {object} { queryMode, destination, cultureSearch, routeSearch, outputTemplate }
 */
function cmdHike(destination, activity) {
  if (!destination || typeof destination !== 'string' || destination.trim().length === 0) {
    return { error: '请指定目的地,例如:hike 四姑娘山' };
  }

  const dest = destination.trim();

  return {
    queryMode: true,
    destination: dest,
    activity: activity || null,
    message: '此结果为查询模式,不接入行程管理。如需创建行程计划,请使用 hike-init。',

    // 文化信息搜索任务
    cultureSearch: {
      categories: ['地理风貌', '历史渊源', '人文与诗词', '遗存遗迹', '美食特产'],
      tasks: [
        { source: 'wikipedia', query: dest, purpose: '地理风貌、历史渊源、文化背景' },
        { source: 'web_search', query: `${dest} 历史文化 诗词`, purpose: '人文诗词、典故、名人' },
        { source: 'xiaohongshu', query: `${dest} 美食 特产`, purpose: '当地特色美食、推荐店铺' },
      ],
    },

    // 徒步路线搜索任务
    routeSearch: {
      tasks: [
        { source: '两步路', query: `${dest} 徒步 轨迹`, purpose: '经典徒步路线 + GPX/KML 轨迹数据' },
        { source: 'xiaohongshu', query: `${dest} 徒步路线 攻略`, purpose: '真实用户经验和实拍照片' },
        { source: 'bilibili', query: `${dest} 徒步 vlog`, purpose: '视频实拍路况和体验' },
      ],
    },

    // 输出格式指引
    outputTemplate: {
      culture: {
        header: '## 行程详情',
        sections: '按 3-5 个类别输出(地理风貌/历史渊源/人文与诗词/遗存遗迹/美食特产等),每类 2-4 句话,标注信息来源',
      },
      routes: {
        header: '## 徒步路线详情',
        fields: ['路线名', '距离', '爬升', '下降', '预计用时', '路线类型', '关键节点', '⚠️ 提示'],
      },
      footer: '> 📌 此结果为查询模式,不接入行程管理。如需创建行程计划,请使用 `hike-init`。',
    },
  };
}

// ── 命令:hike-init ───────────────────────────────────

/**
 * 初始化行程,日期/目的地/活动直接从参数解析。
 * 新格式:hike-init <startDate> <destination> <activity>
 * 示例:hike-init 2026-06-01 古蜀道 徒步+文化探访
 *
 * 向后兼容旧的 cmdInit(destination, options) 调用风格。
 *
 * @param {string} startDate - 出发日期 YYYY-MM-DD(必填)
 * @param {string} destination - 目的地(必填)
 * @param {string} activity - 活动描述,如 "徒步+文化探访"(必填)
 * @param {object} [options] - { outputDir, confirmed }
 * @returns {object} { tripId, status, collectPrompt } - collectPrompt 仅含缺失的补充问题
 */
function cmdInit(startDate, destination, activity, options) {
  // ── 向后兼容:旧格式 cmdInit(destination, options) ──
  // 情况1:destination 是 object → cmdInit(dest, {outputDir:'...'})
  // 情况2:destination 为 undefined → cmdInit('华山') 只传了1个参数
  if (destination === undefined || typeof destination === 'object') {
    const oldDest = startDate || '';
    const oldOpts = (typeof destination === 'object') ? destination : {};
    return _cmdInitLegacy(oldDest, oldOpts);
  }
  // 情况3:传了2个非object参数,但第一个不像日期 → 旧格式
  if (activity === undefined && !/^\d{4}-\d{2}-\d{2}$/.test(startDate || '')) {
    return _cmdInitLegacy(startDate || '', {});
  }

  const opts = (typeof options === 'object' && options !== null) ? options : {};
  const outputDir = getOutputDir(opts);
  let state = loadState(outputDir);

  // ── 目的地必填校验 ──
  // 未提供目的地时不初始化,等待用户明确目的地
  if (!destination || !destination.trim()) {
    return {
      error: '请先明确目的地,例如:hike-init 2026-06-01 大觉寺 徒步',
      needsDestination: true,
    };
  }

  // 检查是否已有进行中的行程
  if (state.activeTripId) {
    const activeTrip = state.trips[state.activeTripId];
    if (activeTrip && activeTrip.status !== STATUS.COMPLETED) {
      return {
        error: `已有进行中的行程「${activeTrip.destination}」(${activeTrip.tripId}),请先完成或取消`,
        activeTripId: activeTrip.tripId,
      };
    }
  }

  // ── 持久化同意确认 ──
  // 首次调用(无 confirmed)返回同意请求;用户确认后传 { confirmed: true } 继续
  if (!opts.confirmed) {
    return {
      needsConsent: true,
      consentType: 'output_dir',
      outputDir: outputDir,
      message: `行程计划将保存到 ${outputDir}。同一服务器的其他用户可能可以查看这些数据。是否继续?`,
    };
  }

  const trip = createTripPlan(destination, opts);
  trip.tripId = generateTripId(destination, startDate);
  trip.dates.start = startDate;
  trip.dates.end = startDate; // 默认单日,后续通过 cmdSetRequirements 修正
  // 文件名格式: 🥾 目的地·活动出行计划
  if (activity && activity.trim()) {
    const actTrimmed = activity.trim();
    const isMultiPart = /[+、/ ]/.test(actTrimmed);
    const hasHiking = actTrimmed.includes('徒步');
    if (isMultiPart || hasHiking) {
      trip.title = `🥾 ${destination}·${actTrimmed}出行计划`;
    } else {
      trip.title = `🥾 ${destination}·${actTrimmed}徒步出行计划`;
    }
  } else {
    trip.title = `🥾 ${destination}出行计划`;
  }

  // 活动描述写入 interests + fitness 推导
  const activityParts = (activity || '').split(/[+、\/]/).map(s => s.trim()).filter(Boolean);
  trip.preferences.interests = activityParts;
  // 从活动关键词推导体力水平
  if (/高强度|重装|穿越/.test(activity)) trip.preferences.fitness = '高强度';
  else if (/休闲|轻松|观光|文化/.test(activity)) trip.preferences.fitness = '轻松';

  state.trips[trip.tripId] = trip;
  state.activeTripId = trip.tripId;
  saveState(state, outputDir);

  // ── 构建精简的补问清单(只问还缺的) ──
  const missing = [];
  const hasAll = !!activity && !!destination && !!startDate;

  if (!activity) {
    missing.push({ id: 'activity', label: '活动类型(如 徒步+文化探访)', required: true });
  }
  if (!destination) {
    missing.push({ id: 'destination', label: '目的地(如 古蜀道)', required: true });
  }
  if (!startDate) {
    missing.push({ id: 'startDate', label: '出发日期(如 2026-06-01)', required: true });
  }

  // 即便三个必填项都有,也补问一些可选信息
  const optionalQuestions = [
    { id: 'endDate', label: '返回日期(单日可不填)', required: false },
    { id: 'destinationRegion', label: '目的地在哪个省/市/县?(如 北京市延庆区,用于精确地图定位)', required: false },
    { id: 'origin', label: '从哪个城市出发?', required: false },
    { id: 'returnTo', label: '回到哪个城市?(同出发可不填)', required: false },
    { id: 'participants', label: '几个人?', required: false, default: '1' },
    { id: 'transport', label: '交通偏好(火车/飞机/自驾)', required: false },
    { id: 'accommodation', label: '住宿偏好(酒店类型/预算)', required: false },
    { id: 'fitness', label: '体力水平(轻松/适中/高强度)', required: false },
    { id: 'gpxFile', label: '如有 GPX/KML 轨迹文件或两步路链接,请提供,可大幅提高路线精度', required: false },
  ];

  if (missing.length > 0) {
    return {
      tripId: trip.tripId,
      status: trip.status,
      collectPrompt: {
        message: `好的!开始规划「${destination || '(待定)'}」的行程。以下信息还需补充:`,
        questions: [...missing, ...optionalQuestions],
      },
    };
  }

  return {
    tripId: trip.tripId,
    status: trip.status,
    summary: {
      destination: trip.destination,
      startDate: trip.dates.start,
      activity: activity,
      interests: trip.preferences.interests,
      fitness: trip.preferences.fitness,
    },
    collectPrompt: {
      message: hasAll
        ? `「${destination} · ${activity}」行程已创建(${startDate})。如需补充细节:`
        : `还需以下信息:`,
      questions: hasAll ? optionalQuestions : [...missing, ...optionalQuestions],
    },
    amapNotice: '🗺️  行程站点名称将通过网络发送给高德地图(Amap)API 以生成地图链接。',
    nextSteps: [
      'search_routes: 搜索徒步路线(两步路 https://www.2bulu.com/track + 小红书 + B站)',
      'search_transport: 查询大交通(12306/flyai)',
      'search_hotels: 查询酒店(flyai/web_search)',
      'search_culture: 收集人文信息(Wikipedia/xiaohongshu)',
      'generate_plan: 生成完整行程计划',
      'render_maps: 渲染行程地图',
    ],
  };
}

/**
 * 旧格式兼容:cmdInit(destination, options)
 */
function _cmdInitLegacy(destination, options) {
  const outputDir = getOutputDir(options);
  let state = loadState(outputDir);

  // ── 目的地必填校验 ──
  // 未提供目的地时不初始化,等待用户明确目的地
  if (!destination || !destination.trim()) {
    return {
      error: '请先明确目的地,例如:hike-init 大觉寺',
      needsDestination: true,
    };
  }

  if (state.activeTripId) {
    const activeTrip = state.trips[state.activeTripId];
    if (activeTrip && activeTrip.status !== STATUS.COMPLETED) {
      return {
        error: `已有进行中的行程「${activeTrip.destination}」(${activeTrip.tripId}),请先完成或取消`,
        activeTripId: activeTrip.tripId,
      };
    }
  }

  // ── 持久化同意确认 ──
  if (!options || !options.confirmed) {
    return {
      needsConsent: true,
      consentType: 'output_dir',
      outputDir: outputDir,
      message: `行程计划将保存到 ${outputDir}。同一服务器的其他用户可能可以查看这些数据。是否继续?`,
    };
  }

  const trip = createTripPlan(destination, options);
  trip.tripId = generateTripId(destination, getToday());
  trip.title = `🥾 ${destination}出行计划`;

  state.trips[trip.tripId] = trip;
  state.activeTripId = trip.tripId;
  saveState(state, outputDir);

  return {
    tripId: trip.tripId,
    status: trip.status,
    collectPrompt: {
      message: `好的!开始规划「${destination}」的徒步行程。请告诉我以下信息:`,
      questions: [
        { id: 'startDate', label: '出发日期(如 2026-05-13)', required: true },
        { id: 'endDate', label: '返回日期(单程可不填)', required: false },
        { id: 'origin', label: '从哪个城市出发?', required: true },
        { id: 'destinationRegion', label: '目的地在哪个省/市/县?(如 北京市延庆区,用于精确地图定位)', required: false },
        { id: 'returnTo', label: '回到哪个城市?(同出发可不填)', required: false },
        { id: 'participants', label: '几个人?', required: false, default: '1' },
        { id: 'transport', label: '交通偏好(火车/飞机/自驾)', required: false },
        { id: 'accommodation', label: '住宿偏好(酒店类型/预算)', required: false },
        { id: 'fitness', label: '体力水平(轻松/适中/高强度)', required: false },
        { id: 'gpxFile', label: '如有 GPX/KML 轨迹文件或两步路链接,请提供,可大幅提高路线精度', required: false },
        { id: 'interests', label: '兴趣方向(历史文化/自然风光/美食等)', required: false },
      ],
    },
  };
}

// ── 命令:设置需求 ────────────────────────────────────

/**
 * 设置收集到的需求。Agent 交互完成后调用。
 * @param {object} requirements - 用户输入的需求数据
 */
function cmdSetRequirements(requirements) {
  const outputDir = getOutputDir(requirements);
  let state = loadState(outputDir);
  const tripId = requirements.tripId || state.activeTripId;
  if (!tripId || !state.trips[tripId]) {
    return { error: '没有活动的行程,请先 hike-init' };
  }

  const trip = state.trips[tripId];
  const r = requirements;

  // 更新日期
  if (r.startDate) trip.dates.start = r.startDate;
  if (r.endDate) trip.dates.end = r.endDate;
  if (r.startDate && !r.endDate) trip.dates.end = r.startDate;
  if (r.title) trip.title = r.title;

  // 更新出发/返回地
  if (r.origin) trip.origin = r.origin;
  if (r.returnTo) trip.returnTo = r.returnTo;
  if (r.destinationRegion) trip.destinationRegion = r.destinationRegion;
  if (!trip.returnTo && trip.origin) trip.returnTo = trip.origin;

  // 更新人数和偏好
  if (r.participants) trip.participants = parseInt(r.participants) || 1;
  if (r.transport) trip.preferences.transport = r.transport;
  if (r.accommodation) trip.preferences.accommodation = r.accommodation;
  if (r.fitness) trip.preferences.fitness = r.fitness;
  if (r.interests) {
    trip.preferences.interests = typeof r.interests === 'string'
      ? r.interests.split(/[,,]/).map(s => s.trim())
      : r.interests;
  }
  // 活动类型(hike-init 新参数兼容)
  if (r.activity) {
    const activityParts = r.activity.split(/[+、/]/).map(s => s.trim()).filter(Boolean);
    trip.preferences.interests = [...new Set([...trip.preferences.interests, ...activityParts])];
  }

  // 重新生成 tripId(用真实日期)
  if (r.startDate) {
    const newTripId = generateTripId(trip.destination, r.startDate);
    if (newTripId !== tripId) {
      delete state.trips[tripId];
      trip.tripId = newTripId;
      state.trips[newTripId] = trip;
      state.activeTripId = newTripId;
    }
  }

  // 自动计算天数并填充 days 数组
  if (trip.dates.start && trip.dates.end) {
    const numDays = dateDiff(trip.dates.start, trip.dates.end) + 1;
    // Day 0 = 抵达日, Day 1..N-1 = 活动日, Day N = 返程日
    // 如果只有1天,就是当天往返
    trip.days = [];
    for (let i = 0; i < numDays; i++) {
      const d = addDays(trip.dates.start, i);
      trip.days.push({
        date: d,
        dayOfWeek: getWeekday(d),
        dayIndex: i,
        theme: i === 0 ? '出发/抵达' : (i === numDays - 1 ? '返程' : '徒步'),
        weather: { condition: '', high: null, low: null },
        nodes: [],
        mapUrl: '',
        dayCost: 0,
      });
    }
  }

  trip.status = STATUS.PLANNING;
  trip.updatedAt = new Date().toISOString();
  saveState(state, outputDir);

  return {
    tripId: trip.tripId,
    status: trip.status,
    summary: {
      destination: trip.destination,
      dates: `${trip.dates.start} ~ ${trip.dates.end}(${trip.days.length}天)`,
      origin: trip.origin,
      returnTo: trip.returnTo,
      participants: trip.participants,
      preferences: trip.preferences,
    },
    amapNotice: '🗺️  行程站点名称将通过网络发送给高德地图(Amap)API 以生成地图链接。',
    nextSteps: [
      'search_routes: 搜索徒步路线(两步路 https://www.2bulu.com/track + 小红书 + B站)',
      'search_transport: 查询大交通(12306/flyai)',
      'search_hotels: 查询酒店(flyai/web_search)',
      'search_culture: 收集人文信息(Wikipedia/xiaohongshu)',
      'generate_plan: 生成完整行程计划',
      'render_maps: 渲染行程地图',
    ],
  };
}

function addDays(dateStr, n) {
  const d = new Date(dateStr + 'T00:00:00+08:00');
  d.setDate(d.getDate() + n);
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

// ── 命令:设置徒步路线 ────────────────────────────────

function cmdSetHikingRoutes(routes, tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };

  trip.hikingRoutes = routes.map(r => ({
    name: r.name || '未命名路线',
    // 从 GPX/KML 提取的 GPS 坐标(最高精度数据源,用于地图渲染)
    waypoints: r.waypoints || [],  // [{name: '起点', lng: 115.xxx, lat: 40.xxx}, ...]
    distance: r.distance || null,
    distanceUnit: r.distanceUnit || 'km',
    ascent: r.ascent || null,
    descent: r.descent || null,
    maxAltitude: r.maxAltitude || null,
    estimatedTime: r.estimatedTime || '',
    type: r.type || '混合',
    routeClass: r.routeClass || '',     // 路线分类: 穿越(起终点不同)/环线(起点=终点,路径不重复)/往返(起点=终点,原路返回)
    keyNodes: r.keyNodes || [],
    gpxSource: r.gpxSource || '',
    gpxFilePath: r.gpxFilePath || '',       // GPX/KML 文件相对路径(gpx/xxx.gpx)
    trackMapPath: r.trackMapPath || '',     // 轨迹地图 HTML 相对路径(gpx/xxx_轨迹地图.html)
    tips: r.tips || '',
    dayIndex: r.dayIndex || 0,
  }));

  // GPX waypoints 自动更新到 day.nodes
  routes.forEach(r => {
    if (r.waypoints && r.waypoints.length >= 2 && r.dayIndex != null) {
      const day = trip.days[r.dayIndex];
      if (day) {
        // 更新起点节点坐标
        const startWP = r.waypoints[0];
        const startNode = day.nodes[0];
        if (startNode && startWP) {
          startNode.gps = { lat: startWP.lat, lng: startWP.lng };
        }
        // 更新终点节点坐标
        const endWP = r.waypoints[r.waypoints.length - 1];
        const endNode = day.nodes[day.nodes.length - 1];
        if (endNode && endWP) {
          endNode.gps = { lat: endWP.lat, lng: endWP.lng };
        }
      }
    }
  });

  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  return { tripId: trip.tripId, hikingRoutes: trip.hikingRoutes };
}

// ── GPX/KML 文件保存 + 轨迹地图生成 ──────────────────

/**
 * 保存 GPX/KML 文件到行程 gpx 目录,并生成轨迹地图 HTML
 * @param {object} trip - 行程对象
 * @param {string} sourcePath - 上传的 GPX/KML 文件路径
 * @returns {{ gpxPath: string, trackMapPath: string, error: string|null }}
 */
function saveGpxFile(trip, sourcePath) {
  // 检查源文件是否存在
  const resolvedPath = path.resolve(sourcePath);
  if (!fs.existsSync(resolvedPath)) {
    // 尝试 webchat inbound 路径
    const inboundCandidate = path.join(os.homedir(), '.openclaw', 'media', 'inbound', path.basename(sourcePath));
    if (fs.existsSync(inboundCandidate)) {
      sourcePath = inboundCandidate;
    } else {
      return { gpxPath: null, trackMapPath: null, error: `文件不存在: ${resolvedPath}。请确认文件路径是否正确。如果文件是通过 webchat 上传的,请使用绝对路径 ~/.openclaw/media/inbound/<文件名>` };
    }
  }

  const gpxDir = path.join(trip.outputDir, 'upcoming', trip.tripId, 'gpx');
  fs.mkdirSync(gpxDir, { recursive: true });

  // 复制 GPX/KML 到 gpx 目录
  const ext = path.extname(sourcePath);
  const baseName = path.basename(sourcePath, ext);
  const destFile = path.join(gpxDir, `${baseName}${ext}`);
  fs.copyFileSync(sourcePath, destFile);

  // 生成轨迹地图 HTML
  const htmlFile = path.join(gpxDir, `${baseName}_轨迹地图.html`);
  const scriptPath = path.join(__dirname, 'generate-track-map.py');
  try {
    execSync(`python3 "${scriptPath}" "${destFile}" --output "${htmlFile}" --tile amap`, { timeout: 30000 });
  } catch (e) {
    return { gpxPath: `gpx/${baseName}${ext}`, trackMapPath: null, error: `轨迹地图生成失败: ${e.message}` };
  }

  // 返回 gpx 目录内的相对路径(用于行程计划链接)
  return { gpxPath: `gpx/${baseName}${ext}`, trackMapPath: `gpx/${baseName}_轨迹地图.html`, error: null };
}

/**
 * 保存截图/图片文件到行程 media 目录
 * @param {object} trip - 行程对象
 * @param {string} sourcePath - 上传的图片/截图文件路径
 * @returns {{ mediaPath: string|null, error: string|null }}
 */
function saveMediaFile(trip, sourcePath) {
  const mediaDir = path.join(trip.outputDir, 'upcoming', trip.tripId, 'media');
  fs.mkdirSync(mediaDir, { recursive: true });

  const resolvedPath = sourcePath.startsWith('~')
    ? path.join(os.homedir(), sourcePath.slice(1))
    : sourcePath;

  if (!fs.existsSync(resolvedPath)) {
    const inboundCandidate = path.join(os.homedir(), '.openclaw', 'media', 'inbound', path.basename(sourcePath));
    if (fs.existsSync(inboundCandidate)) {
      sourcePath = inboundCandidate;
    } else {
      return { mediaPath: null, error: `文件不存在: ${resolvedPath}` };
    }
  }

  const ext = path.extname(resolvedPath);
  const baseName = path.basename(resolvedPath, ext);
  const destFile = path.join(mediaDir, `${baseName}${ext}`);
  fs.copyFileSync(resolvedPath, destFile);

  return { mediaPath: `media/${baseName}${ext}`, error: null };
}

// ── 命令:设置交通 ────────────────────────────────────

function cmdSetDayNode(dayIndex, node, tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };
  if (!trip.days[dayIndex]) return { error: `第 ${dayIndex} 天不存在` };

  trip.days[dayIndex].nodes.push({
    time: node.time || '',
    type: node.type || 'other',
    name: node.name || '',
    detail: node.detail || '',
    cost: node.cost || null,
    remark: node.remark || '',
  });
  trip.days[dayIndex].dayCost = trip.days[dayIndex].nodes.reduce((s, n) => s + (n.cost || 0), 0);
  trip.totalBudget = trip.days.reduce((s, d) => s + d.dayCost, 0);
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  return { tripId: trip.tripId, dayIndex, day: trip.days[dayIndex] };
}

function cmdSetDayWeather(dayIndex, weather, tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };
  if (!trip.days[dayIndex]) return { error: `第 ${dayIndex} 天不存在` };

  trip.days[dayIndex].weather = weather;
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  return { tripId: trip.tripId, dayIndex, weather };
}

// ── 命令:设置文化信息 ────────────────────────────────

function cmdSetCulture(culture, tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };

  trip.culture = culture;
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  return { tripId: trip.tripId, cultureKeys: Object.keys(trip.culture) };
}

// ── 命令:设置装备 + 待办 ──────────────────────────────

function cmdSetEquipment(equipment, tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };

  trip.equipment = equipment;
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  return { tripId: trip.tripId, equipment: trip.equipment };
}

function cmdSetTodos(todos, tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };

  // 兼容旧格式(纯字符串)与新格式({text, done} 对象)
  trip.todos = todos.map(t => typeof t === 'string' ? { text: t, done: false } : t);
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  return { tripId: trip.tripId, todos: trip.todos };
}

// ── 命令:标记待办完成 ──────────────────────────────

/**
 * 通过编号快速标记待办为完成。
 * 用户输入 "TODO 1 done" / "todo 2 done" 即可完成对应编号的待办。
 *
 * @param {number} todoNumber - 待办编号(1-based)
 * @param {string} [tripId] - 行程 ID
 * @returns {object} { tripId, todo, message }
 */
function cmdTodoDone(todoNumber, tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };

  const index = todoNumber - 1;
  if (index < 0 || index >= trip.todos.length) {
    return { error: `待办编号 ${todoNumber} 无效(共 ${trip.todos.length} 项)` };
  }

  const todo = trip.todos[index];
  if (typeof todo === 'string') {
    // 旧格式自动迁移
    trip.todos[index] = { text: todo, done: true };
  } else {
    todo.done = true;
  }
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  const text = typeof todo === 'string' ? todo : todo.text;
  return { tripId: trip.tripId, todoIndex: index + 1, text, message: `✅ TODO ${index + 1} 已完成: ${text}` };
}

// ── 命令:设置地图链接 ────────────────────────────────

function cmdSetMapUrl(dayIndex, mapUrl, tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };
  if (!trip.days[dayIndex]) return { error: `第 ${dayIndex} 天不存在` };

  trip.days[dayIndex].mapUrl = mapUrl;
  if (!trip.mapUrls.includes(mapUrl)) {
    trip.mapUrls.push(mapUrl);
  }
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  return { tripId: trip.tripId, dayIndex, mapUrl };
}

// ── 命令:确认计划 ────────────────────────────────────

function cmdConfirm(tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };

  trip.status = STATUS.CONFIRMED;
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  return { tripId: trip.tripId, status: trip.status };
}

// ── 命令:出发(激活) ────────────────────────────────

function cmdActivate(tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };
  if (trip.status !== STATUS.CONFIRMED) {
    return { error: `行程状态「${trip.status}」无法激活,需要先确认` };
  }

  trip.status = STATUS.ACTIVE;
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  return { tripId: trip.tripId, status: trip.status };
}

// ── 命令:hike-status ─────────────────────────────────

function cmdStatus(tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) {
    return { status: STATUS.IDLE, message: '没有活动的行程。输入 hike-init <目的地> 开始规划。' };
  }

  const totalDays = trip.days.length;
  const completedDays = trip.days.filter(d => d.nodes.length > 0).length;
  const totalCost = trip.totalBudget || trip.days.reduce((s, d) => s + d.dayCost, 0);

  // 统计节点状态
  const allNodes = trip.days.flatMap(d => d.nodes.map(n => ({ ...n, date: d.date })));
  const nodeStats = {
    total: allNodes.length,
    completed: allNodes.filter(n => n.actualStatus === NODE_STATUS.COMPLETED).length,
    changed: allNodes.filter(n => n.actualStatus === NODE_STATUS.CHANGED).length,
    skipped: allNodes.filter(n => n.actualStatus === NODE_STATUS.SKIPPED).length,
    pending: allNodes.filter(n => n.actualStatus === NODE_STATUS.PENDING).length,
    untracked: allNodes.filter(n => !n.actualStatus).length,
  };
  nodeStats.tracked = nodeStats.completed + nodeStats.changed + nodeStats.skipped + nodeStats.pending;

  // 汇总偏差
  const alertDeviations = trip.actuals.deviations.filter(d => d.alert);
  const infoDeviations = trip.actuals.deviations.filter(d => !d.alert);

  return {
    tripId: trip.tripId,
    status: trip.status,
    destination: trip.destination,
    dates: trip.dates,
    origin: trip.origin,
    returnTo: trip.returnTo,
    participants: trip.participants,
    preferences: trip.preferences,
    progress: totalDays > 0 ? `${completedDays}/${totalDays} 天已规划` : '未开始规划',
    hikingRoutes: trip.hikingRoutes.length,
    totalBudget: totalCost,
    logs: trip.logs.length,
    outputDir: trip.outputDir,
    // 订单确认状态
    orderConfirmations: trip.orderConfirmations.length,
    // 节点执行状态
    nodeStatus: nodeStats,
    // 偏差总览
    deviations: {
      alert: alertDeviations.length,
      info: infoDeviations.length,
      alerts: alertDeviations.map(d => ({
        type: d.type,
        node: d.node,
        planned: d.planned,
        actual: d.actual,
        diffText: d.diffText,
      })),
    },
    days: trip.days.map(d => ({
      date: d.date,
      dayOfWeek: d.dayOfWeek,
      theme: d.theme,
      nodes: d.nodes.length,
      weather: d.weather,
      mapUrl: d.mapUrl,
      // 每天节点状态摘要
      nodeSummary: {
        total: d.nodes.length,
        completed: d.nodes.filter(n => n.actualStatus === NODE_STATUS.COMPLETED).length,
        changed: d.nodes.filter(n => n.actualStatus === NODE_STATUS.CHANGED).length,
        skipped: d.nodes.filter(n => n.actualStatus === NODE_STATUS.SKIPPED).length,
        pending: d.nodes.filter(n => n.actualStatus === NODE_STATUS.PENDING).length,
        untracked: d.nodes.filter(n => !n.actualStatus).length,
      },
    })),
  };
}

// ── 命令:hike-today ──────────────────────────────────

function cmdToday(dateStr) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state);
  if (!trip) return { error: '没有活动的行程' };

  const targetDate = dateStr || getToday();
  const day = trip.days.find(d => d.date === targetDate);
  if (!day) {
    return {
      error: `${targetDate} 不在行程范围内(${trip.dates.start} ~ ${trip.dates.end})`,
      availableDays: trip.days.map(d => `${d.date}(${d.dayOfWeek})`),
    };
  }

  // 渲染当天时间线(含计划 vs 实际对比)
  const timeline = day.nodes.map(n => ({
    time: n.time,
    type: n.type,
    name: n.name,
    detail: n.detail,
    cost: n.cost,
    remark: n.remark,
    // 实际数据(如有)
    actualStatus: n.actualStatus || null,
    actualIcon: n.actualStatusIcon || null,
    actualTime: n.actualTime || null,
    actualCost: n.actualCost || null,
    actualRemark: n.actualRemark || null,
  }));

  // 汇总当天偏差
  const dayDeviations = trip.actuals.deviations.filter(d => {
    const nd = trip.days[day.dayIndex];
    return nd && nd.nodes.some(n => n.name === d.node);
  });

  return {
    date: day.date,
    dayOfWeek: day.dayOfWeek,
    theme: day.theme,
    weather: day.weather,
    timeline: timeline,
    mapUrl: day.mapUrl,
    estimatedCost: day.dayCost,
    dayIndex: day.dayIndex,
    totalDays: trip.days.length,
    tips: day.nodes.filter(n => n.type === 'hiking').map(n => n.remark).filter(Boolean),
    // 计划 vs 实际总览
    comparison: {
      hasActual: timeline.some(t => t.actualStatus || t.actualTime || t.actualCost),
      deviations: dayDeviations.length > 0 ? dayDeviations.map(d => ({
        type: d.type,
        node: d.node,
        diffText: d.diffText,
        alert: d.alert,
      })) : [],
    },
  };
}

// ── 订单短信解析 ────────────────────────────────

/**
 * 解析订单确认短信,提取结构化数据
 * @param {string} text - SMS 文本
 * @returns {object|null} { type, data }
 */
function parseOrderSMS(text) {
  // 先检测短信类型
  // 火车票关键词: 车次、列车、二等座/一等座/硬卧、12306
  if (/车次|列车|等座|硬卧|软卧|硬座|无座|\b[GCKDTZYL]\d+\b/.test(text)) {
    for (const pattern of SMS_PATTERNS.train) {
      const m = text.match(pattern);
      if (m) {
        const groups = m.slice(1);
        // 统一提取顺序: carNum, fromSta, fromTime, toSta, toTime, seat, orderId
        let carNum, fromSta, fromTime, toSta, toTime, seat, orderId;
        if (pattern.source.startsWith('订单\\s*')) {
          // 模式1(新): 订单+车次号 直接格式 → carNum, fromSta, fromTime, toSta, toTime, seat, orderId
          [carNum, fromSta, fromTime, toSta, toTime, seat, orderId] = groups;
        } else if (pattern.source.startsWith('车次')) {
          // 模式2: 车次 + 出发站时间-到达站时间 + 座位 + 订单号
          [carNum, fromSta, fromTime, toSta, toTime, seat, orderId] = groups;
        } else {
          // 模式3: 订单号 + 车次 变体
          [orderId, carNum, fromSta, fromTime, toSta, toTime, seat] = groups;
        }
        // 清理站名
        fromSta = fromSta.replace(/站$/, '站').replace(/站站/, '站');
        if (!fromSta.endsWith('站')) fromSta += '站';
        toSta = toSta.replace(/站$/, '站').replace(/站站/, '站');
        // 有些站名本身包含"站"字但不以站结尾(如 剑门关站),规范化
        if (!toSta.endsWith('站') && !/(?:东|南|西|北|关|桥|口|岭)$/.test(toSta)) toSta += '站';
        return {
          type: 'train',
          data: { carNum, fromSta, fromTime, toSta, toTime, seat, orderId },
        };
      }
    }
  }

  // 机票关键词: 航班、舱、登机
  if (/航班|舱|登机|起飞|到达/.test(text)) {
    for (const pattern of SMS_PATTERNS.flight) {
      const m = text.match(pattern);
      if (m) {
        const groups = m.slice(1);
        let flightNum, fromCity, toCity, date, fromTime, toTime, seat, orderId;
        if (pattern.source.startsWith('航班')) {
          [flightNum, fromCity, toCity, date, fromTime, toTime, seat, orderId] = groups;
        } else {
          [orderId, flightNum, fromCity, toCity, date, fromTime, toTime] = groups;
          seat = '';
        }
        return {
          type: 'flight',
          data: { flightNum, fromCity, toCity, date, fromTime, toTime, seat, orderId },
        };
      }
    }
  }

  // 酒店关键词: 酒店/宾馆/客栈 + 入住/退房/预订
  if (/(?:酒店|宾馆|客栈|民宿|饭店|公寓|旅社).*(?:入住|退房|预订|已订)/.test(text) ||
      /(?:入住|退房|预订|已订).*(?:酒店|宾馆|客栈|民宿|饭店|公寓|旅社)/.test(text)) {
    for (const pattern of SMS_PATTERNS.hotel) {
      const m = text.match(pattern);
      if (m) {
        const groups = m.slice(1);
        let hotelName, checkIn, checkOut, roomType, orderId;
        if (groups.length === 5) {
          // 完整模式
          if (/^[A-Za-z0-9]+$/.test(groups[0])) {
            [orderId, hotelName, checkIn, checkOut, roomType] = groups;
          } else {
            [hotelName, checkIn, checkOut, roomType, orderId] = groups;
          }
        } else if (groups.length === 4) {
          // 简化模式
          [hotelName, checkIn, roomType, orderId] = groups;
          checkOut = '';
        }
        // 从原始短信中推断是否含早,不保留 raw 文本
        const hasBreakfast = /含.*[早双]/.test(text);
        return {
          type: 'hotel',
          data: { hotelName, checkIn, checkOut, roomType, orderId, hasBreakfast },
        };
      }
    }
  }

  return null;
}

/**
 * 将解析的订单 SMS 应用到 TripPlan
 * @param {object} trip - TripPlan
 * @param {object} sms - parseOrderSMS 返回值
 * @returns {object} { applied, matchedDayIndex, detail }
 */
function applySMSToTrip(trip, sms) {
  if (!sms || !sms.data) return { applied: false, detail: '无效的 SMS 数据' };

  const { type, data } = sms;
  const result = { applied: false, detail: '', type };

  if (type === 'train') {
    // 匹配日期:根据出发时间和行程日期匹配 day
    const trainDate = guessDateFromTrip(trip, data.fromTime, data.toTime);
    let matchedDay = null;
    if (trainDate) {
      matchedDay = trip.days.find(d => d.date === trainDate);
    }
    if (!matchedDay) {
      // fallback: 查找第一个有 train 类型节点的日期
      matchedDay = trip.days.find(d => d.nodes.some(n => n.type === 'train'));
    }

    // 构建节点数据(不覆盖已有 cost)
    const nodeData = {
      time: `${data.fromTime}-${data.toTime}`,
      type: 'train',
      name: `${data.fromSta}→${data.toSta}`,
      detail: data.carNum,
      remark: `${data.seat},订单${data.orderId}`,
    };

    if (matchedDay) {
      // 查找已存在的同类型节点,支持覆盖
      const existingIdx = matchedDay.nodes.findIndex(
        n => n.type === 'train' && (n.detail === data.carNum || n.name.includes(data.fromSta))
      );
      if (existingIdx >= 0) {
        matchedDay.nodes[existingIdx] = { ...matchedDay.nodes[existingIdx], ...nodeData };
        result.action = 'updated';
        result.nodeIndex = existingIdx;
      } else {
        matchedDay.nodes.push(nodeData);
        result.action = 'added';
        result.nodeIndex = matchedDay.nodes.length - 1;
      }
      result.matchedDayIndex = trip.days.indexOf(matchedDay);
      result.matchedDay = matchedDay.date;
      matchedDay.dayCost = matchedDay.nodes.reduce((s, n) => s + (n.cost || 0), 0);
    } else {
      // 无匹配日,提示用户指定
      result.applied = false;
      result.detail = `无法匹配行程日期,请用 hike-log "交通 D${trip.days[0]?.date || ''}" 指定日期后再试`;
      return result;
    }

    result.applied = true;
    result.detail = `${result.action === 'updated' ? '已更新' : '已添加'}火车票:${data.carNum} ${data.fromSta}${data.fromTime}→${data.toSta}${data.toTime},${data.seat}`;
    result.node = nodeData;

  } else if (type === 'flight') {
    let matchedDay = trip.days.find(d => d.date === data.date);
    if (!matchedDay) {
      matchedDay = trip.days.find(d => d.nodes.some(n => n.type === 'flight'));
    }

    const nodeData = {
      time: `${data.fromTime}-${data.toTime}`,
      type: 'flight',
      name: `${data.fromCity}→${data.toCity}`,
      detail: data.flightNum,
      remark: `${data.seat},订单${data.orderId}`,
    };

    if (matchedDay) {
      const existingIdx = matchedDay.nodes.findIndex(
        n => n.type === 'flight' && (n.detail === data.flightNum || n.name.includes(data.fromCity))
      );
      if (existingIdx >= 0) {
        matchedDay.nodes[existingIdx] = { ...matchedDay.nodes[existingIdx], ...nodeData };
        result.action = 'updated';
      } else {
        matchedDay.nodes.push(nodeData);
        result.action = 'added';
      }
      result.matchedDayIndex = trip.days.indexOf(matchedDay);
      result.matchedDay = matchedDay.date;
    } else {
      result.applied = false;
      result.detail = `无法匹配行程日期 ${data.date},请检查行程日期范围`;
      return result;
    }

    result.applied = true;
    result.detail = `${result.action === 'updated' ? '已更新' : '已添加'}机票:${data.flightNum} ${data.fromCity}→${data.toCity} ${data.date} ${data.fromTime}-${data.toTime},${data.seat}`;
    result.node = nodeData;

  } else if (type === 'hotel') {
    // 酒店匹配:查找入住日期范围内的 day
    const hotelStartDate = data.checkIn;
    let matchedDays = [];
    if (hotelStartDate && data.checkOut) {
      matchedDays = trip.days.filter(d => d.date >= hotelStartDate && d.date < data.checkOut);
    } else if (hotelStartDate) {
      matchedDays = trip.days.filter(d => d.date === hotelStartDate);
    } else {
      matchedDays = trip.days.filter(d => d.nodes.some(n => n.type === 'hotel'));
    }

    if (matchedDays.length === 0) {
      result.applied = false;
      result.detail = `无法匹配行程日期 ${hotelStartDate || '(未识别)'},请检查行程日期范围`;
      return result;
    }

    // 为每个匹配的日期添加/更新酒店节点
    const nights = matchedDays.length;
    matchedDays.forEach((day, i) => {
      const nodeData = {
        time: i === 0 ? '入住' : '',
        type: 'hotel',
        name: data.hotelName,
        detail: `${data.roomType}`,
        remark: `${i === 0 ? `入住${data.checkIn},` : ''}退房${data.checkOut},订单${data.orderId}${i > 0 ? '(续住)' : ''}${data.hasBreakfast ? ',含早' : ''}`,
      };

      const existingIdx = day.nodes.findIndex(
        n => n.type === 'hotel' && n.name === data.hotelName
      );
      if (existingIdx >= 0) {
        day.nodes[existingIdx] = { ...day.nodes[existingIdx], ...nodeData };
      } else {
        day.nodes.push(nodeData);
      }
      day.dayCost = day.nodes.reduce((s, n) => s + (n.cost || 0), 0);
    });

    result.applied = true;
    result.action = 'added';
    result.detail = `已添加酒店:${data.hotelName} ${data.roomType},${data.checkIn} 入住${nights > 1 ? `,共${nights}晚` : ''}`;
    result.matchedDayIndex = trip.days.indexOf(matchedDays[0]);
    result.matchedDay = matchedDays[0].date;
  }

  // 记录订单确认
  trip.orderConfirmations.push({
    type,
    orderId: data.orderId,
    timestamp: new Date().toISOString(),
    data,
  });

  trip.updatedAt = new Date().toISOString();
  return result;
}

function guessDateFromTrip(trip, fromTime, toTime) {
  // 根据时间判断:如果出发时间在上午,通常是行程首日
  const hour = parseInt(fromTime);
  // 找行程范围内第一个日期
  if (hour <= 12) {
    // 上午出发→找第0天
    return trip.days[0]?.date || null;
  } else {
    // 下午/晚上出发→可能是前一天或当天
    return trip.days[0]?.date || null;
  }
}

// ── 计划 vs 实际对比 ─────────────────────────────

/**
 * 比较实际数据与计划,产生偏差记录
 * @param {object} trip - TripPlan
 * @param {object} actual - { dayIndex, nodeIndex, actualTime, actualCost, actualRemark }
 * @returns {object} { alert, deviations }
 */
function compareActualVsPlan(trip, actual) {
  const deviations = [];
  const day = trip.days[actual.dayIndex];
  if (!day || !day.nodes[actual.nodeIndex]) {
    return { alert: false, deviations: [], message: '未找到对应节点' };
  }

  const node = day.nodes[actual.nodeIndex];

  // 1. 时间偏差
  if (actual.actualTime && node.time) {
    const plannedMinutes = parseTimeToMinutes(node.time);
    const actualMinutes = parseTimeToMinutes(actual.actualTime);
    if (plannedMinutes != null && actualMinutes != null) {
      const diff = actualMinutes - plannedMinutes;
      if (Math.abs(diff) > DEVIATION_THRESHOLDS.timeMinutes) {
        deviations.push({
          type: 'time',
          node: node.name,
          planned: node.time,
          actual: actual.actualTime,
          diffMinutes: diff,
          diffText: `${diff > 0 ? '+' : ''}${diff} 分钟(${diff > 0 ? '延迟' : '提前'})`,
          alert: true,
          threshold: DEVIATION_THRESHOLDS.timeMinutes,
        });
      }
    }
  }

  // 2. 费用偏差
  if (actual.actualCost != null && node.cost != null) {
    const diff = actual.actualCost - node.cost;
    if (Math.abs(diff) > DEVIATION_THRESHOLDS.costYuan) {
      deviations.push({
        type: 'cost',
        node: node.name,
        planned: node.cost,
        actual: actual.actualCost,
        diffYuan: diff,
        diffText: `${diff > 0 ? '+' : ''}¥${diff}(${diff > 0 ? '超支' : '节约'})`,
        alert: true,
        threshold: DEVIATION_THRESHOLDS.costYuan,
      });
    }
  }

  // 3. 路线/备注变更
  if (actual.actualRemark) {
    deviations.push({
      type: 'remark',
      node: node.name,
      planned: node.remark || node.detail || '',
      actual: actual.actualRemark,
      alert: false,
    });
  }

  // 存储偏差
  if (deviations.length > 0) {
    trip.actuals.deviations.push(...deviations);
  }

  const hasAlert = deviations.some(d => d.alert);
  return {
    alert: hasAlert,
    deviations,
    message: hasAlert
      ? `⚠️ 偏差提醒:${deviations.filter(d => d.alert).map(d => d.diffText).join(';')}`
      : (deviations.length > 0 ? '已记录差异(未超阈值)' : '无偏差'),
  };
}

function parseTimeToMinutes(timeStr) {
  // 支持 "07:50-09:21" 格式,取出发时间的分钟数
  // 也支持纯时间 "07:50"
  const t = timeStr.split('-')[0].trim();
  const m = t.match(/(\d{1,2}):(\d{2})/);
  if (!m) return null;
  return parseInt(m[1]) * 60 + parseInt(m[2]);
}

// ── 节点状态操作 ─────────────────────────────────

/**
 * 手动标记节点状态
 * @param {string} tripId
 * @param {number} dayIndex
 * @param {number} nodeIndex
 * @param {string} status - completed / changed / skipped / pending
 * @param {object} actual - 可选的实际数据
 */
function cmdSetNodeStatus(tripId, dayIndex, nodeIndex, status, actual) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };

  const day = trip.days[dayIndex];
  if (!day) return { error: `第 ${dayIndex} 天不存在` };

  const node = day.nodes[nodeIndex];
  if (!node) return { error: `第 ${dayIndex} 天第 ${nodeIndex} 个节点不存在` };

  const validStatuses = Object.values(NODE_STATUS);
  if (!validStatuses.includes(status)) {
    return { error: `无效的状态: ${status},支持: ${validStatuses.join(', ')}` };
  }

  node.actualStatus = status;
  node.actualStatusIcon = NODE_STATUS_ICONS[status];

  if (actual) {
    if (actual.actualTime) node.actualTime = actual.actualTime;
    if (actual.actualCost != null) node.actualCost = actual.actualCost;
    if (actual.actualRemark) node.actualRemark = actual.actualRemark;
  }

  // 如果提供了实际数据,触发偏差对比
  let compareResult = null;
  if (actual && (actual.actualTime || actual.actualCost != null || actual.actualRemark)) {
    compareResult = compareActualVsPlan(trip, { dayIndex, nodeIndex, ...actual });
  }

  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  return {
    tripId: trip.tripId,
    dayIndex,
    nodeIndex,
    node: node.name,
    status: node.actualStatus,
    icon: node.actualStatusIcon,
    actual: { actualTime: node.actualTime, actualCost: node.actualCost, actualRemark: node.actualRemark },
    compare: compareResult,
  };
}

// ── 命令:hike-log ────────────────────────────────────

/**
 * hike-log - 记录行程最新信息。
 *
 * 用途:
 * - 🚄 订好车票:粘贴 12306 订单短信自动解析(车次/站点/时间/座位)
 * - ✈️ 订好机票:粘贴航司订单短信自动解析(航班/城市/日期/舱位)
 * - 🏨 订了酒店:粘贴酒店订单短信自动解析(店名/入住/退房/房型)
 * - 💰 支出花销:记录实际花费,自动与预算对比
 * - ⏰ 时间变更:记录实际出发/到达时间,自动计算偏差
 * - 📝 备注信息:任意文本记录
 *
 * 自动能力:
 * - 订单短信智能解析(12306 / 航司 / 酒店 / OTA)
 * - 计划 vs 实际时间/费用偏差对比
 * - 节点状态自动标记(完成/变更/跳过/待定)
 *
 * @param {string} text - 日志文本或订单短信
 * @param {string} [dateStr] - 日期,默认今天
 */
function cmdLog(text, dateStr, options) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state);
  if (!trip) return { error: '没有活动的行程' };

  const opts = (typeof options === 'object' && options !== null) ? options : {};

  const logDate = dateStr || getToday();
  const logEntry = {
    date: logDate,
    timestamp: new Date().toISOString(),
    text: text,
  };

  const result = {
    tripId: trip.tripId,
    logEntry: logEntry,
    totalLogs: trip.logs.length + 1,
    message: '',
  };

  // ── 1. 检测节点状态标记关键字 ──
  const statusMarkers = [
    { pattern: /✅|完成|已完成|搞完/, status: NODE_STATUS.COMPLETED },
    { pattern: /🔄|变更|变了|改成|改为|调整/, status: NODE_STATUS.CHANGED },
    { pattern: /❌|跳过|取消|没去|不去/, status: NODE_STATUS.SKIPPED },
    { pattern: /⏸️|待定|暂缓|推迟/, status: NODE_STATUS.PENDING },
  ];

  let detectedStatus = null;
  for (const marker of statusMarkers) {
    if (marker.pattern.test(text)) {
      detectedStatus = marker.status;
      break;
    }
  }

  // ── 2. 解析实际时间(多种自然语言表达) ──
  const actualTimePatterns = [
    /实际[出发到]*[时间:::]\s*(\d{1,2}:\d{2})/,
    /实[际在][到出发]*(\d{1,2}:\d{2})/,
    /(\d{1,2}:\d{2})[出发到]的/,
    /改到\s*(\d{1,2}:\d{2})/,
    /调整[为到]\s*(\d{1,2}:\d{2})/,
    /实际.*?(\d{1,2}:\d{2}\s*[--~至到]\s*\d{1,2}:\d{2})/,
  ];
  let actualTime = null;
  for (const p of actualTimePatterns) {
    const m = text.match(p);
    if (m) { actualTime = m[1].trim(); break; }
  }

  // ── 3. 解析实际费用 ──
  let actualCost = null;
  // 明确实际费用
  const actualCostMatch = text.match(/实际[花费用]了?\s*(\d+(?:\.\d{1,2})?)\s*(?:块|元|¥)/);
  if (actualCostMatch) {
    actualCost = parseFloat(actualCostMatch[1]);
  } else {
    // 经典超支/多花钱模式
    const costMatch = text.match(/(?:超出了预算|超(?:出)?预?算?了?|多[花用了]了?|额外[花用]?了?|超支了?)\s*(\d+(?:\.\d{1,2})?)\s*(?:块|元|¥)?/);
    if (costMatch) {
      logEntry.costOverrun = parseFloat(costMatch[1]);
    }
    // 新增: "实际多花了 ¥X" 模式 (¥在数字前)
    if (!logEntry.costOverrun) {
      const extraCostMatch = text.match(/实际多[花用了]了?\s*¥\s*(\d+(?:\.\d{1,2})?)/);
      if (extraCostMatch) {
        logEntry.costOverrun = parseFloat(extraCostMatch[1]);
      }
    }
    // 花了 / 用了 ¥XX(排除「多花/额外花」避免与 costOverrun 冲突)
    const spentMatch = text.match(/(?<!多)(?<!额外)(?:[花用]了)\s*(\d+(?:\.\d{1,2})?)\s*(?:块|元|¥)/);
    if (spentMatch && !actualCostMatch) {
      actualCost = parseFloat(spentMatch[1]);
    }
  }

  // ── 4. 解析时间延迟(经典模式) ──
  const delayMatch = text.match(/[晚迟](?:了)?(\d+)\s*(?:分钟|min)/);
  if (delayMatch) {
    logEntry.delayMinutes = parseInt(delayMatch[1]);
  }

  // ── 5. 尝试订单 SMS 解析 ──
  // 先快速检测文本是否包含订单特征关键词,如有则需要用户同意
  const smsKeywords = /订单|车次|航班|预订|入住|退房|12306|携程|航旅|飞猪/i;
  let sms = null;
  if (opts.confirmed || !smsKeywords.test(text)) {
    sms = parseOrderSMS(text);
  } else {
    // 检测到疑似订单短信,要求用户确认
    return {
      needsConsent: true,
      consentType: 'sms_parse',
      tripId: trip.tripId,
      message: '⚠️ 您提供的短信内容(含订单号、日期、车次/航班/酒店名称等出行信息)将被保存在本地服务器上。同一服务器的其他用户可能可以查看这些数据。是否继续?',
    };
  }

  if (sms) {
    logEntry.smsType = sms.type;
    const smsResult = applySMSToTrip(trip, sms);
    result.sms = sms;
    result.smsApply = smsResult;
    logEntry.smsApplied = smsResult.applied;
    logEntry.smsDetail = smsResult.detail;
  }

  // ── 6. 尝试匹配当日节点进行偏差对比 ──
  result.compare = null;
  const todayDay = trip.days.find(d => d.date === logDate);
  if (todayDay && todayDay.nodes.length > 0) {
    // 尝试根据文本内容匹配节点
    let matchedNodeIndex = -1;
    const nodeKeywords = text;
    for (let i = 0; i < todayDay.nodes.length; i++) {
      const node = todayDay.nodes[i];
      const nodeText = `${node.name} ${node.detail} ${node.type}`;
      // 关键词匹配
      if (node.name && node.name.length > 1 && nodeKeywords.includes(node.name.substring(0, 2))) {
        matchedNodeIndex = i;
        break;
      }
      if (node.detail && node.detail.length > 1 && nodeKeywords.includes(node.detail)) {
        matchedNodeIndex = i;
        break;
      }
    }

    // 如果没匹配到但有实际数据或偏差,默认匹配第一个交通/徒步节点
    if (matchedNodeIndex === -1 && (actualTime || actualCost != null || logEntry.delayMinutes || logEntry.costOverrun)) {
      matchedNodeIndex = 0;
    }

    if (matchedNodeIndex >= 0 && (actualTime || actualCost != null || detectedStatus || logEntry.delayMinutes || logEntry.costOverrun)) {
      const node = todayDay.nodes[matchedNodeIndex];

      // 从 delayMinutes 推导 actualTime
      if (!actualTime && logEntry.delayMinutes && node.time) {
        const plannedMinutes = parseTimeToMinutes(node.time);
        if (plannedMinutes != null) {
          const delayedMinutes = plannedMinutes + logEntry.delayMinutes;
          const h = Math.floor(delayedMinutes / 60);
          const m = delayedMinutes % 60;
          actualTime = `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
        }
      }

      // 从 costOverrun 推导 actualCost
      if (actualCost == null && logEntry.costOverrun != null && node.cost != null) {
        actualCost = node.cost + logEntry.costOverrun;
      }

      // 更新 actual 数据
      if (actualTime) {
        node.actualTime = actualTime;
        logEntry.actualTime = actualTime;
      }
      if (actualCost != null) {
        node.actualCost = actualCost;
        logEntry.actualCost = actualCost;
      }

      // 更新节点状态
      if (detectedStatus) {
        node.actualStatus = detectedStatus;
        node.actualStatusIcon = NODE_STATUS_ICONS[detectedStatus];
        logEntry.nodeStatus = detectedStatus;
      }

      // 触发偏差对比
      const compare = compareActualVsPlan(trip, {
        dayIndex: trip.days.indexOf(todayDay),
        nodeIndex: matchedNodeIndex,
        actualTime: actualTime,
        actualCost: actualCost,
        actualRemark: text,
      });
      result.compare = compare;
      logEntry.deviations = compare.deviations;
    }
  }

  // 最终记录
  trip.logs.push(logEntry);
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  // 构建返回消息
  const parts = [`已记录 ${logDate}:${text}`];
  if (sms && sms.type) {
    const icon = sms.type === 'train' ? '🚄' : sms.type === 'flight' ? '✈️' : '🏨';
    const action = result.smsApply?.applied ? (result.smsApply.action === 'updated' ? '更新' : '添加') : '检测到但未';
    parts.push(`${icon} ${action}订单:${result.smsApply?.detail || sms.data.orderId}`);
  }
  if (result.compare && result.compare.alert) {
    parts.push(`⚠️ ${result.compare.message}`);
  }
  if (detectedStatus) {
    parts.push(`${NODE_STATUS_ICONS[detectedStatus]} 节点状态已标记为:${detectedStatus}`);
  }
  result.message = parts.join('\n');

  return result;
}

// ── 命令:hike-list ───────────────────────────────────

const INCOMPLETE_STATUSES = [STATUS.PLANNING, STATUS.CONFIRMED, STATUS.ACTIVE];

/**
 * 列出所有未完成的行程(status 为 PLANNING/CONFIRMED/ACTIVE)。
 * 传入 tripId 则对该行程做完整汇总+归档(原 hike-summary 逻辑)。
 * @param {string} [tripId] - 可选,归档指定行程
 */
function cmdList(tripId) {
  const { state } = loadStateWithFallback();

  // ── 指定 tripId:完整汇总 + 归档(原 hike-summary 逻辑) ──
  if (tripId) {
    return cmdListArchive(state, tripId);
  }

  // ── 无参数:列出所有未完成的行程 ──
  const incompleteTrips = Object.entries(state.trips)
    .filter(([, trip]) => INCOMPLETE_STATUSES.includes(trip.status))
    .map(([id, trip]) => {
      const totalDays = trip.days.length;
      const plannedDays = trip.days.filter(d => d.nodes.length > 0).length;
      const totalCost = trip.totalBudget || trip.days.reduce((s, d) => s + d.dayCost, 0);
      const isActive = trip.tripId === state.activeTripId;

      return {
        tripId: id,
        isActive,
        destination: trip.destination,
        status: trip.status,
        dates: trip.dates,
        progress: totalDays > 0 ? `${plannedDays}/${totalDays} 天已规划` : '未开始规划',
        budget: totalCost,
        hikingRoutes: trip.hikingRoutes.length,
        logs: trip.logs.length,
        createdAt: trip.createdAt,
        updatedAt: trip.updatedAt,
      };
    });

  if (incompleteTrips.length === 0) {
    return {
      trips: [],
      total: 0,
      message: '没有未完成的行程。输入 hike-init <目的地> 开始规划。',
    };
  }

  // 统计
  const totalTrips = Object.keys(state.trips).length;
  const completedCount = totalTrips - incompleteTrips.length;

  return {
    trips: incompleteTrips,
    total: incompleteTrips.length,
    stats: {
      totalTrips,
      incomplete: incompleteTrips.length,
      completed: completedCount,
    },
    activeTripId: state.activeTripId,
    message: `共 ${incompleteTrips.length} 个未完成行程(总计 ${totalTrips} 个,已完成 ${completedCount} 个)`,
  };
}

/**
 * 对指定 tripId 做完整汇总+归档(原 hike-summary 逻辑,hike-list <tripId> 时调用)
 */
function cmdListArchive(state, tripId) {
  const trip = state.trips[tripId];
  if (!trip) return { error: `未找到行程「${tripId}」` };

  // 汇总 logs
  const costOverruns = trip.logs.filter(l => l.costOverrun).reduce((s, l) => s + l.costOverrun, 0);
  const totalDelayMins = trip.logs.filter(l => l.delayMinutes).reduce((s, l) => s + l.delayMinutes, 0);
  const routeChanges = trip.logs.filter(l => l.text.includes('路线变更') || l.text.includes('绕路'));
  const allNotes = trip.logs.map(l => `- ${l.date} ${l.text}`);

  // 节点状态统计
  const allNodes = trip.days.flatMap(d => d.nodes);
  const nodeStats = {
    total: allNodes.length,
    completed: allNodes.filter(n => n.actualStatus === NODE_STATUS.COMPLETED).length,
    changed: allNodes.filter(n => n.actualStatus === NODE_STATUS.CHANGED).length,
    skipped: allNodes.filter(n => n.actualStatus === NODE_STATUS.SKIPPED).length,
    pending: allNodes.filter(n => n.actualStatus === NODE_STATUS.PENDING).length,
  };

  // 订单确认汇总
  const orderSummary = trip.orderConfirmations.map(o => ({
    type: o.type,
    orderId: o.orderId,
    timestamp: o.timestamp,
  }));

  // 更新状态为完成
  trip.status = STATUS.COMPLETED;
  trip.updatedAt = new Date().toISOString();
  if (state.activeTripId === tripId) {
    state.activeTripId = null;
  }

  // 汇总实际数据
  const summary = {
    tripId: trip.tripId,
    destination: trip.destination,
    dates: trip.dates,
    status: trip.status,
    budget: {
      planned: trip.totalBudget || trip.days.reduce((s, d) => s + d.dayCost, 0),
      overrun: costOverruns,
      message: costOverruns > 0
        ? `超出预算 ¥${costOverruns}`
        : (costOverruns < 0 ? `节约 ¥${Math.abs(costOverruns)}` : '未记录费用偏差'),
    },
    timekeeping: {
      totalDelayMinutes: totalDelayMins,
      message: totalDelayMins > 0
        ? `累计延迟 ${totalDelayMins} 分钟`
        : '未记录时间偏差',
    },
    hiking: {
      plannedRoutes: trip.hikingRoutes.length,
      plannedDistance: trip.hikingRoutes.reduce((s, r) => s + (r.distance || 0), 0),
    },
    nodes: nodeStats,
    orderConfirmations: orderSummary,
    deviations: {
      total: trip.actuals.deviations.length,
      alerts: trip.actuals.deviations.filter(d => d.alert),
    },
    logs: {
      total: trip.logs.length,
      routeChanges: routeChanges.length,
      notes: allNotes,
    },
    outputPath: path.join(trip.outputDir, 'upcoming', trip.tripId, getPlanFilename(trip)),
    archivePath: path.join(trip.outputDir, 'completed', trip.tripId, getPlanFilename(trip)),
  };

  saveState(state, trip.outputDir);

  return summary;
}

// ── 命令:hike-select(取代 hike-set) ────────────────

/**
 * hike-select - 选择/切换默认输出目录或激活行程。
 *
 * 用法 1:hike-select output <path>
 *   设置/切换默认输出目录,持久化到 config.json
 *
 * 用法 2:hike-select <planname>
 *   激活/选择某个行程进行管理。<planname> 可以是 tripId 或目的地关键词,支持模糊匹配。
 *   选择后,hike-status / hike-today / hike-log 等命令都作用于被选中的行程。
 *
 * @param {string} arg1 - 'output' 或 planname
 * @param {string} [arg2] - output 路径(仅 arg1='output' 时有效)
 */
function cmdSelect(arg1, arg2) {
  if (!arg1) {
    return { error: '用法:hike-select output <路径> | baseurl <URL> | <行程名>' };
  }

  // ── 用法 1:hike-select output <path> ──
  if (arg1 === 'output') {
    if (!arg2) {
      return { error: '请提供输出目录路径,例如:hike-select output /path/to/planner' };
    }
    const resolved = path.resolve(arg2);
    const parent = path.dirname(resolved);
    if (!fs.existsSync(parent)) {
      return { error: `父目录不存在:${parent}` };
    }
    const config = loadConfig();
    config.outputDir = resolved;
    saveConfig(config);
    return {
      key: 'outputDir',
      value: resolved,
      configPath: CONFIG_FILE,
      message: `默认输出目录已设置为:${resolved}`,
    };
  }

  // ── 用法 2:hike-select baseurl <url> ──
  if (arg1 === 'baseurl') {
    if (!arg2) {
      const config = loadConfig();
      return {
        current: config.webBaseUrl,
        message: `当前 webBaseUrl: ${config.webBaseUrl}`,
      };
    }
    const url = arg2.replace(/\/+$/, ''); // 去除尾部斜杠
    const config = loadConfig();
    config.webBaseUrl = url;
    saveConfig(config);
    return {
      key: 'webBaseUrl',
      value: url,
      configPath: CONFIG_FILE,
      message: `Web 基础 URL 已设置为:${url}`,
    };
  }

  // ── 用法 2:hike-select <planname> ──
  const query = arg1.toLowerCase();
  const configuredDir = getOutputDir();
  let state = loadState(configuredDir);

  // 如果在已配置的目录中没有行程,也检查默认目录并合并
  let effectiveDir = configuredDir;
  if (configuredDir !== DEFAULT_OUTPUT_DIR) {
    const defaultState = loadState(DEFAULT_OUTPUT_DIR);
    const defaultTrips = Object.entries(defaultState.trips);
    if (defaultTrips.length > 0) {
      // 合并两个目录的行程
      for (const [id, trip] of Object.entries(state.trips)) {
        if (!defaultState.trips[id]) defaultState.trips[id] = trip;
      }
      defaultState.activeTripId = defaultState.activeTripId || state.activeTripId;
      state = defaultState;
      effectiveDir = DEFAULT_OUTPUT_DIR;
    }
  }

  const allTrips = Object.entries(state.trips);
  if (allTrips.length === 0) {
    return { error: '没有任何行程。请先 hike-init 创建行程。' };
  }

  // 模糊匹配:精确 tripId > 部分 tripId > 目的地关键词
  let matches = [];

  // 1. 精确 tripId 匹配
  const exact = allTrips.find(([id]) => id.toLowerCase() === query);
  if (exact) {
    matches = [exact];
  }

  // 2. tripId 包含查询
  if (matches.length === 0) {
    matches = allTrips.filter(([id]) => id.toLowerCase().includes(query));
  }

  // 3. 目的地关键词匹配
  if (matches.length === 0) {
    matches = allTrips.filter(([, trip]) =>
      trip.destination && trip.destination.toLowerCase().includes(query)
    );
  }

  if (matches.length === 0) {
    return {
      error: `未找到匹配「${arg1}」的行程`,
      availableTrips: allTrips.map(([id, t]) => ({
        tripId: id,
        destination: t.destination,
        status: t.status,
        dates: t.dates,
        isActive: t.tripId === state.activeTripId,
      })),
    };
  }

  if (matches.length > 1) {
    return {
      error: `找到 ${matches.length} 个匹配的行程,请更精确地指定:`,
      candidates: matches.map(([id, t]) => ({
        tripId: id,
        destination: t.destination,
        status: t.status,
        dates: t.dates,
        isActive: t.tripId === state.activeTripId,
      })),
    };
  }

  // 唯一匹配 → 激活该行程
  const [matchedId, matchedTrip] = matches[0];
  const wasActive = state.activeTripId === matchedId;
  state.activeTripId = matchedId;
  saveState(state, effectiveDir);

  const statusLabel = { IDLE: '空闲', COLLECTING: '收集中', PLANNING: '规划中', CONFIRMED: '已确认', ACTIVE: '进行中', COMPLETED: '已完成' };

  return {
    tripId: matchedId,
    destination: matchedTrip.destination,
    status: matchedTrip.status,
    statusLabel: statusLabel[matchedTrip.status] || matchedTrip.status,
    dates: matchedTrip.dates,
    message: wasActive
      ? `已在管理「${matchedTrip.destination}」(${matchedId})`
      : `✅ 已切换到「${matchedTrip.destination}」(${matchedId}),后续 hike-status/today/log 将作用于该行程。`,
  };
}

// ── 命令:生成行程计划文件 ───────────────────────────

/**
 * 按 PLAN_TEMPLATE 格式渲染完整行程计划
 * @param {string} tripId
 * @returns {object} { content, filePath }
 */
function cmdGeneratePlan(tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };

  let md = renderPlan(trip);

  const dir = path.join(trip.outputDir, 'upcoming', trip.tripId);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const filePath = path.join(dir, getPlanFilename(trip));
  fs.writeFileSync(filePath, md, 'utf8');

  trip.status = STATUS.CONFIRMED;
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  return {
    tripId: trip.tripId,
    filePath: filePath,
    content: md,
    message: `行程计划已生成:${filePath}`,
  };
}

// ── Day 编号解析工具 ────────────────────────────────

/**
 * 解析 Day 编号字符串(day1-dayN)为 0-indexed 数组索引
 * 也兼容纯数字格式(1-N)
 */
function parseDayIndex(dayStr) {
  if (!dayStr) return -1;
  const match = dayStr.toLowerCase().match(/^day(\d+)$/);
  if (match) return parseInt(match[1], 10) - 1;
  // 兼容纯数字
  const num = parseInt(dayStr, 10);
  if (!isNaN(num) && num >= 1) return num - 1;
  return -1;
}

// ── 命令:hike-add(Day 级新增行程段) ─────────────────────

/**
 * 在指定 Day 末尾新增行程段节点
 * 用法:hike-add day3 A-B
 */
function cmdAddDay(dayStr, routeStr, tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };

  const dayIndex = parseDayIndex(dayStr);
  if (dayIndex < 0 || dayIndex >= trip.days.length) {
    return { error: `DAY 参数无效。有效范围:day1-day${trip.days.length}` };
  }
  if (!routeStr || !routeStr.trim()) {
    return { error: '缺少行程段描述。用法:hike-add <DAY> <行程段>' };
  }

  const day = trip.days[dayIndex];
  const newNode = {
    time: '-',
    name: routeStr.trim(),
    type: 'activity',
    cost: null,
    remark: '',
    detail: '',
  };

  day.nodes.push(newNode);
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  let md = renderPlan(trip);
  const dir = path.join(trip.outputDir, 'upcoming', trip.tripId);
  const filePath = path.join(dir, getPlanFilename(trip));
  fs.writeFileSync(filePath, md, 'utf8');

  return {
    ok: true,
    tripId: trip.tripId,
    message: `已添加行程段「${newNode.name}」到 DAY ${dayIndex + 1}`,
  };
}

// ── 命令:hike-del(Day 级删除日程) ────────────────────────

/**
 * 删除指定 Day
 * 用法:hike-del day3
 */
function cmdDelDay(dayStr, tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };

  const dayIndex = parseDayIndex(dayStr);
  if (dayIndex < 0 || dayIndex >= trip.days.length) {
    return { error: `DAY 参数无效。有效范围:day1-day${trip.days.length}` };
  }

  const removed = trip.days.splice(dayIndex, 1)[0];
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  let md = renderPlan(trip);
  const dir = path.join(trip.outputDir, 'upcoming', trip.tripId);
  const filePath = path.join(dir, getPlanFilename(trip));
  fs.writeFileSync(filePath, md, 'utf8');

  return {
    ok: true,
    tripId: trip.tripId,
    message: `已删除 Day ${dayIndex + 1}`,
  };
}

// ── 命令:hike-reorder(Day 级重排) ──────────────────

/**
 * 调整 Day 顺序
 * 用法:hike-reorder day5 after day2
 *       hike-reorder day5 before day2
 *       hike-reorder day5 to day2
 */
function cmdReorderDay(dayStr, action, targetDay, tripId) {
  const { state } = loadStateWithFallback();
  const trip = getTrip(state, tripId);
  if (!trip) return { error: '没有活动的行程' };

  const srcIdx = parseDayIndex(dayStr);
  if (srcIdx < 0 || srcIdx >= trip.days.length) {
    return { error: `DAY 参数无效。有效范围:day1-day${trip.days.length}` };
  }

  if (!action || !['after', 'before', 'to'].includes(action)) {
    return { error: `无效操作:${action}。支持 after/before/to` };
  }

  if (!targetDay || !targetDay.trim()) {
    return { error: '缺少目标 Day。用法:hike-reorder <DAY> after|before|to <目标DAY>' };
  }

  let tgtIdx = parseDayIndex(targetDay);
  if (tgtIdx < 0 || tgtIdx >= trip.days.length) {
    return { error: `目标 DAY 参数无效。有效范围:day1-day${trip.days.length}` };
  }

  let destIdx;
  if (action === 'after') {
    destIdx = tgtIdx + 1;
  } else if (action === 'before') {
    destIdx = tgtIdx;
  } else { // to
    // swap src and tgt elements
    const src = trip.days[srcIdx];
    trip.days[srcIdx] = trip.days[tgtIdx];
    trip.days[tgtIdx] = src;
    trip.updatedAt = new Date().toISOString();
    saveState(state, trip.outputDir);

    let md = renderPlan(trip);
    const dir = path.join(trip.outputDir, 'upcoming', trip.tripId);
    const filePath = path.join(dir, getPlanFilename(trip));
    fs.writeFileSync(filePath, md, 'utf8');

    return { ok: true, tripId: trip.tripId, message: `已交换 Day${srcIdx + 1} 和 Day${tgtIdx + 1}` };
  }

  if (destIdx === srcIdx) {
    return { ok: true, tripId: trip.tripId, message: '已在目标位置,无需移动。' };
  }

  const [moved] = trip.days.splice(srcIdx, 1);
  // splice 之后如果 srcIdx < destIdx,destIdx 需要 -1
  if (srcIdx < destIdx) destIdx--;
  trip.days.splice(destIdx, 0, moved);
  trip.updatedAt = new Date().toISOString();
  saveState(state, trip.outputDir);

  let md = renderPlan(trip);
  const dir = path.join(trip.outputDir, 'upcoming', trip.tripId);
  const filePath = path.join(dir, getPlanFilename(trip));
  fs.writeFileSync(filePath, md, 'utf8');

  return {
    ok: true,
    tripId: trip.tripId,
    message: `已将 Day${srcIdx + 1} 移动到位置 ${destIdx + 1}`,
  };
}

// ── 默认装备生成 ────────────────────────────────

/**
 * 根据目的地类型和活动生成默认装备清单
 */
function getDefaultEquipment(trip) {
  const fitness = (trip.preferences.fitness || '').toLowerCase();
  const interests = (trip.preferences.interests || []).map(s => s.toLowerCase());
  const isWinter = isWinterTrip(trip);
  const isHighAlpine = /高山|雪山|高原|海拔/.test(fitness) || /高山|雪山/.test(interests.join(' '));
  const isHeavy = /高强度|重装|穿越/.test(fitness);

  const eq = {
    '鞋': '徒步鞋/越野跑鞋(建议中帮,防水)',
    '衣': '速干衣裤、冲锋衣/雨衣' + (isWinter ? '、保暖内衣、羽绒服' : '') + '、换洗衣物',
    '包': (isHeavy ? '重装背包50-70L' : '徒步背包20-35L') + '、防水罩',
    '导航': '手机+两步路/六只脚离线地图、充电宝',
    '水': '水袋/保温杯 1-2L,沿途补给点补水',
    '食物': '路餐(能量棒/坚果/面包)、电解质冲剂',
    '防晒': '防晒霜SPF50+、遮阳帽、太阳镜、头巾',
    '药品': '创可贴、云南白药、肠胃药、感冒药' + (isHighAlpine ? '、高原安/红景天' : ''),
    '证件': '身份证、学生证/老年证(如有优惠)',
    '电子': '充电宝、数据线、相机(如需)',
    '其他': '登山杖×2、头灯/手电、急救毯、现金若干',
  };

  return eq;
}

// ── 默认待办事项生成 ────────────────────────────

/**
 * 根据行程上下文生成默认待办清单
 */
function getDefaultTodos(trip) {
  const todos = [
    { text: '订火车票/机票(确认出发日期和班次)', done: false },
    { text: '订酒店(确认入住日期和房型)', done: false },
    { text: '检查装备清单并补齐缺失物品', done: false },
    { text: '购买户外保险(推荐:慧择/平安户外险)', done: false },
    { text: '下载离线地图和GPX/KML轨迹(两步路/六只脚)', done: false },
  ];

  // 如果有徒步路线,加上轨迹相关
  if (trip.hikingRoutes && trip.hikingRoutes.length > 0) {
    todos.push('熟悉徒步路线的关键节点和补给点');
  }

  return todos;
}

// ── 路线详情提取 ────────────────────────────────

/**
 * 从 hikingRoutes 中匹配路线并返回格式化摘要
 * @returns {string} 如 "距离10km 爬升286m 预计3.5h 难度★★★/★★★★★"
 */
function getHikeRouteSummary(nodeName, hikingRoutes) {
  if (!hikingRoutes || hikingRoutes.length === 0) return '';

  // 尝试精确匹配路线名
  let route = hikingRoutes.find(r => r.name === nodeName);
  // 模糊匹配:节点名包含路线名或路线名包含节点名
  if (!route) {
    route = hikingRoutes.find(r =>
      (nodeName && nodeName.includes(r.name)) || (r.name && r.name.includes(nodeName))
    );
  }
  if (!route) return '';

  const parts = [];
  if (route.distance) parts.push(`距离${route.distance}${route.distanceUnit || 'km'}`);
  if (route.ascent) parts.push(`爬升${route.ascent}m`);
  if (route.estimatedTime) parts.push(`预计${route.estimatedTime}`);
  if (route.difficulty) {
    parts.push(`难度${route.difficulty}`);
  } else if (route.distance) {
    // 根据距离估算难度
    const dist = parseFloat(route.distance);
    if (dist <= 5) parts.push('难度★★/★★★★★');
    else if (dist <= 10) parts.push('难度★★★/★★★★★');
    else if (dist <= 20) parts.push('难度★★★★/★★★★★');
    else parts.push('难度★★★★★/★★★★★');
  }

  return parts.join(' ');
}

/**
 * 判断行程是否在冬季(11月-3月)
 */
function isWinterTrip(trip) {
  if (!trip.dates || !trip.dates.start) return false;
  const m = parseInt((trip.dates.start || '').substring(5, 7));
  return m >= 11 || m <= 3;
}

// ── 出行建议渲染 ────────────────────────────────

/**
 * 渲染出行建议节
 */
function renderTravelAdvice(trip, lines) {
  lines.push('### 出行建议');
  lines.push('');

  // 交通建议
  lines.push('#### 交通建议');
  lines.push('');
  lines.push('| 交通方式 | 建议 |');
  lines.push('|---------|------|');
  // 到达交通
  const arrivalNodes = trip.days.flatMap(d => d.nodes.filter(n =>
    ['train', 'flight', 'bus'].includes(n.type) &&
    n.name && n.name.includes('→')
  ));
  const arrivalTransport = arrivalNodes.length > 0
    ? arrivalNodes.map(n => `${n.name}(${n.detail || ''})`).join(';')
    : '待确认';
  lines.push(`| 到达交通 | ${arrivalTransport} |`);

  // 离开交通
  const departureNodes = trip.days.flatMap(d => d.nodes.filter(n =>
    ['train', 'flight', 'bus'].includes(n.type) &&
    n.name && n.name.includes('→')
  ));
  const lastDayNodes = trip.days.length > 0
    ? trip.days[trip.days.length - 1].nodes.filter(n =>
        ['train', 'flight'].includes(n.type) && n.name && n.name.includes('→')
      )
    : [];
  const departureTransport = lastDayNodes.length > 0
    ? lastDayNodes.map(n => `${n.name}(${n.detail || ''})`).join(';')
    : '待确认';
  lines.push(`| 离开交通 | ${departureTransport} |`);

  // 当地交通
  const localTransports = trip.days.flatMap(d => d.nodes.filter(n =>
    ['taxi', 'car', 'selfdrive', 'bus', 'metro'].includes(n.type)
  ));
  const localTransport = localTransports.length > 0
    ? [...new Set(localTransports.map(n => n.remark || n.name))].filter(Boolean).join(';') || '包车/打车/公共交通'
    : '建议提前联系当地包车司机或使用打车软件';
  lines.push(`| 当地交通 | ${localTransport} |`);
  lines.push('');

  // 网红推荐
  if (trip.culture && trip.culture.recommendations) {
    const rec = trip.culture.recommendations;

    if (rec.hotels && rec.hotels.length > 0) {
      lines.push('#### 网红酒店推荐');
      lines.push('');
      lines.push('| 名称 | 特色 | 参考价格 |');
      lines.push('|------|------|---------|');
      for (const h of rec.hotels) {
        lines.push(`| ${h.name || ''} | ${h.feature || ''} | ${h.price || ''} |`);
      }
      lines.push('');
    }

    if (rec.spots && rec.spots.length > 0) {
      lines.push('#### 网红景点推荐');
      lines.push('');
      lines.push('| 名称 | 亮点 | 建议时长 |');
      lines.push('|------|------|---------|');
      for (const s of rec.spots) {
        lines.push(`| ${s.name || ''} | ${s.highlight || ''} | ${s.duration || ''} |`);
      }
      lines.push('');
    }

    if (rec.activities && rec.activities.length > 0) {
      lines.push('#### 网红活动推荐');
      lines.push('');
      lines.push('| 活动 | 特色 | 适合人群 |');
      lines.push('|------|------|---------|');
      for (const a of rec.activities) {
        lines.push(`| ${a.name || ''} | ${a.feature || ''} | ${a.crowd || ''} |`);
      }
      lines.push('');
    }
  } else {
    // 占位:提示用户可搜索推荐
    lines.push('#### 网红推荐');
    lines.push('');
    lines.push(`> 💡 使用 \`xiaohongshu__search_feeds\` 搜索「${trip.destination} 徒步 攻略」获取最新网红推荐。`);
    lines.push('');
  }
}

// ── 地图链接自动生成 ─────────────────────────────

/**
 * 根据节点类型推导路线类型(高德地图 routeType 参数)
 * @param {string} nodeType - 节点类型
 * @returns {string} driving | walking | transfer | straight
 */
function getNodeRouteType(nodeType) {
  switch (nodeType) {
    case 'hiking': case 'walk': return 'walking';
    case 'metro': case 'bus': return 'transfer';
    case 'taxi': case 'selfdrive': case 'car': return 'driving';
    case 'train': case 'flight': return 'straight';
    default: return 'driving';
  }
}

/**
 * 为指定 day 自动生成高德地图可视化路线链接
 * @param {number} dayIndex - day 索引
 * @param {string[]} stops - 节点名称列表
 * @param {string} [region] - 省市区县范围,用于地理编码消歧义(如 "北京市延庆区")
 * @param {Array<{lat:number,lng:number}>} [coords] - GPX/KML 提取的 GPS 坐标
 * @param {string[]} [routeTypes] - 逐段路线类型数组(长度 = stops.length - 1),默认全为 driving
 * @returns {{ link: string|null, error: string|null }}
 */
function renderDayMap(dayIndex, stops, region, coords, routeTypes) {
  const key = process.env.AMAP_WEBSERVICE_KEY;
  if (!key) {
    return { link: null, error: '未设置 AMAP_WEBSERVICE_KEY 环境变量,无法生成地图链接' };
  }

  if (!stops || stops.length < 2) {
    return { link: null, error: '节点数量不足(至少需要2个节点)' };
  }

  const scriptPath = path.join(__dirname, 'render-itinerary-map.js');

  try {
    // 构建逐段路线类型参数(逗号分隔)
    const rtypes = (routeTypes && routeTypes.length > 0) ? routeTypes : stops.slice(0, -1).map(() => 'driving');
    const routeTypeArg = rtypes.join(',');

    // 优先使用 GPX/KML 提取的 GPS 坐标(无需地理编码,精度最高)
    if (coords && coords.length >= 2) {
      const coordsStr = coords.map(c => `${c.lng},${c.lat}`).join('|');
      // 使用 waypoints 的名称作为 POI 标签,确保起点/终点与坐标一致
      const waypointNames = coords.map(c => (c.name || '').replace(/,/g, ' '));
      const namesStr = waypointNames.join('|');
      const env = { ...process.env, AMAP_WEBSERVICE_KEY: key };
      const result = execSync(
        `node "${scriptPath}" --coords="${coordsStr}" --names="${namesStr}" --routeType=${routeTypeArg}`,
        { timeout: 30000, encoding: 'utf8', env }
      );
      const match = result.match(/https:\/\/a\.amap\.com\/[^\s\n]+/);
      if (match) return { link: match[0], error: null };
    }

    // 兜底:通过地名地理编码(带省市区县前缀消歧义)
    const stopsStr = stops.map(s => s.replace(/,/g, ' ')).join(',');
    const regionArg = region ? ` --region="${region.replace(/"/g, '')}"` : '';
    const env = { ...process.env, AMAP_WEBSERVICE_KEY: key };
    const result = execSync(
      `node "${scriptPath}" --stops="${stopsStr}" --routeType=${routeTypeArg}${regionArg}`,
      { timeout: 30000, encoding: 'utf8', env }
    );
    const match = result.match(/https:\/\/a\.amap\.com\/[^\s\n]+/);
    if (match) {
      return { link: match[0], error: null };
    }
    return { link: null, error: '无法从地图渲染脚本输出中提取链接' };
  } catch (e) {
    return { link: null, error: `地图链接生成失败: ${e.message}` };
  }
}
// ── Markdown 渲染器 ────────────────────────────────────

function renderPlan(trip) {
  const lines = [];

  // 标题(优先 trip.title,空则 fallback)
  const h1 = trip.title
    ? `# ${trip.title}`
    : `# 🥾 ${trip.destination || '旅行'} 出行计划`;
  lines.push(h1);
  lines.push('');
  lines.push(`**出行日期**:${formatFullDate(trip.dates.start)} - ${formatFullDate(trip.dates.end)}`);
  lines.push(`**目的地**:${trip.destination}`);
  lines.push(`**人员**:${trip.participants}人`);
  lines.push('');

  // 总览表
  lines.push('## 总览');
  lines.push('');
  lines.push('| 日期 | 星期 | 行程概要 | 出行方式 | 班次/车牌 | 住宿酒店 | 含早 | 天气 |');
  lines.push('|------|------|---------|---------|---------|---------|------|------|');
  for (const day of trip.days) {
    const transportNodes = day.nodes.filter(n => ['train', 'flight', 'bus', 'taxi', 'car', 'selfdrive', 'metro', 'hiking'].includes(n.type));
    const transport = transportNodes.map(n => getNodeTransportLabel(n)).join(' ') || '';
    const schedule = day.nodes.filter(n => ['train', 'flight', 'bus'].includes(n.type)).map(n => n.detail).join(', ') || '';
    const hotel = day.nodes.find(n => n.type === 'hotel');
    const hotelName = hotel ? hotel.name : '';
    const hasBreakfast = hotel ? (hotel.remark && /含(早|双早|早餐|二?早)/.test(hotel.remark) ? '是' : '否') : '';
    const weather = day.weather.condition ? `${day.weather.condition}${day.weather.high ? ` ${day.weather.high}°C/${day.weather.low}°C` : ''}` : '';
    lines.push(`| ${formatDate(day.date)} | ${day.dayOfWeek} | ${day.theme} | ${transport} | ${schedule} | ${hotelName} | ${hasBreakfast} | ${weather} |`);
  }
  lines.push('');

  // 每日安排
  lines.push('## 每日安排');
  lines.push('');
  for (const day of trip.days) {
    lines.push(`### DAY ${day.dayIndex} - ${formatDate(day.date)}(${day.dayOfWeek}):${day.theme}`);
    lines.push('');
    if (day.nodes.length === 0) {
      lines.push('| 时间 | 区间 | 节点详情 | 费用 | 备注 |');
      lines.push('|------|------|---------|------|------|');
      lines.push('| | | 待规划 | | |');
    } else {
      lines.push('| 时间 | 区间 | 节点详情 | 费用 | 备注 |');
      lines.push('|------|------|---------|------|------|');
      // 合并连续徒步节点为紧凑行
      const mergedNodes = [];
      let hikingGroup = null;

      for (const node of day.nodes) {
        if (node.type === 'hiking') {
          if (!hikingGroup) {
            hikingGroup = {
              type: 'hiking',
              time: node.time,
              endTime: node.time,
              nodes: [node],
              cost: node.cost || 0,
            };
          } else {
            hikingGroup.endTime = node.time;
            hikingGroup.nodes.push(node);
            hikingGroup.cost += node.cost || 0;
          }
        } else {
          if (hikingGroup) {
            mergedNodes.push(hikingGroup);
            hikingGroup = null;
          }
          mergedNodes.push(node);
        }
      }
      if (hikingGroup) mergedNodes.push(hikingGroup);

      for (const node of mergedNodes) {
        if (node.type === 'hiking' && node.nodes) {
          // 徒步合并行
          const names = node.nodes.map(n => n.name);
          const keyNodesStr = names.length > 2
            ? `${names[0]}→...→${names[names.length - 1]}`
            : names.join('→');
          const timeStr = node.nodes.length > 1
            ? `${node.time}-${node.endTime}`
            : node.time;
          // 尝试从 hikingRoutes 获取路线摘要
          const route = trip.hikingRoutes.find(r =>
            r.name === node.nodes[0].name ||
            node.nodes.some(n => n.name === r.name)
          );
          let detail = keyNodesStr;
          if (route) {
            const parts = [];
            if (route.distance) parts.push(`${route.distance}${route.distanceUnit || 'km'}`);
            if (route.ascent) parts.push(`爬升${route.ascent}m`);
            if (route.estimatedTime) parts.push(`预计${route.estimatedTime}`);
            detail = `${keyNodesStr}(${parts.join(',')})`;
          }
          lines.push(`| ${timeStr} | 🥾 徒步 | ${detail} | ${node.cost ? `¥${node.cost}` : ''} | |`);
        } else {
          const costStr = node.cost != null ? `¥${node.cost}` : '';
          const transportLabel = getNodeTransportLabel(node);
          lines.push(`| ${node.time} | ${transportLabel} | ${node.name} | ${costStr} | ${node.remark || ''} |`);
        }
      }
    }
    lines.push('');
    if (day.mapUrl) {
      lines.push(`> 🗺️ [查看地图](${day.mapUrl})`);
    } else if (day.nodes.length >= 2) {
      // 自动生成地图链接
      const stopNames = day.nodes.map(n => n.name).filter(Boolean);
      if (stopNames.length >= 2) {
        // 尝试从当天的徒步路线中提取 GPS 坐标(GPX/KML 直接解析,精度最高)
        const dayHikeRoute = trip.hikingRoutes.find(r => r.dayIndex === day.dayIndex || r.name === (day.nodes.find(n => n.type === 'hiking') || {}).name);
        const gpsCoords = (dayHikeRoute && dayHikeRoute.waypoints && dayHikeRoute.waypoints.length >= 2) ? dayHikeRoute.waypoints : null;
        // 逐段推导路线类型(根据节点类型自动映射)
        const { routeTypes } = getRouteTypesForDay(day);
        const segTypes = routeTypes ? routeTypes.split(',') : [];
        const { link, error } = renderDayMap(day.dayIndex, stopNames, trip.destinationRegion, gpsCoords, segTypes);
        if (link) {
          day.mapUrl = link;
          if (!trip.mapUrls.includes(link)) trip.mapUrls.push(link);
          lines.push(`> 🗺️ [查看地图](${link})`);
        } else if (error) {
          lines.push(`> 🗺️ *${error}*`);
        }
      }
    }
    if (day.dayCost > 0) {
      lines.push(`> 💰 本日费用:约¥${day.dayCost}`);
    }
    lines.push('');
  }

  // 行程详情
  lines.push('## 行程详情');
  lines.push('');
  lines.push(`### ${trip.destination}`);
  lines.push('');

  // 文化信息 - 3-5 个最相关分类
  const cultureOrder = ['geography', 'history', 'poetry', 'relics', 'worldHeritage', 'food', 'religion', 'festivals'];
  const cultureTitles = {
    geography: '地理风貌',
    history: '历史渊源',
    poetry: '人文与诗词',
    relics: '遗存遗迹',
    worldHeritage: '世界遗产',
    food: '美食特产',
    religion: '宗教文化',
    festivals: '民俗节庆',
  };

  if (trip.culture && Object.keys(trip.culture).filter(k => k !== 'recommendations').length > 0) {
    const cultureKeys = Object.keys(trip.culture).filter(k => k !== 'recommendations');
    // 先输出已有的
    const renderedKeys = new Set();
    for (const key of cultureOrder) {
      if (trip.culture[key]) {
        lines.push(`### ${cultureTitles[key] || key}`);
        lines.push('');
        lines.push(trip.culture[key]);
        lines.push('');
        renderedKeys.add(key);
      }
    }
    // 输出不在标准顺序中的自定义 key
    for (const key of cultureKeys) {
      if (!renderedKeys.has(key)) {
        lines.push(`### ${key}`);
        lines.push('');
        lines.push(trip.culture[key]);
        lines.push('');
      }
    }
    // 强制补齐:如果少于3个已有分类,生成占位节
    if (renderedKeys.size < 3) {
      const remaining = cultureOrder.filter(k => !renderedKeys.has(k));
      const toAdd = remaining.slice(0, 3 - renderedKeys.size);
      for (const key of toAdd) {
        lines.push(`### ${cultureTitles[key] || key}`);
        lines.push('');
        lines.push(`> 💡 使用 \`web_search\` 或 \`xiaohongshu__search_feeds\` 搜索「${trip.destination} ${cultureTitles[key]}」填充此节。`);
        lines.push('');
      }
    }
  } else {
    // 完全没有文化信息:输出最少3个占位节
    const defaultCategories = cultureOrder.slice(0, 3);
    for (const key of defaultCategories) {
      lines.push(`### ${cultureTitles[key] || key}`);
      lines.push('');
      lines.push(`> 💡 使用 \`web_search\` 搜索「${trip.destination} ${cultureTitles[key]}」获取信息填充此节。`);
      lines.push('');
    }
  }

  // ── 徒步路线详情(独立顶级章节,与总览/每日安排/行程详情同级) ──
  if (trip.hikingRoutes.length > 0) {
    lines.push('## 徒步路线详情');
    lines.push('');
    for (const route of trip.hikingRoutes) {
      lines.push(`### ${route.name}`);
      lines.push('');
      lines.push('| 项目 | 数据 |');
      lines.push('|------|------|');
      if (route.distance) lines.push(`| 距离 | ${route.distance}${route.distanceUnit} |`);
      if (route.ascent) lines.push(`| 爬升 | ${route.ascent}m |`);
      if (route.descent) lines.push(`| 下降 | ${route.descent}m |`);
      if (route.maxAltitude) lines.push(`| 最高海拔 | ${route.maxAltitude}m |`);
      if (route.estimatedTime) lines.push(`| 预计用时 | ${route.estimatedTime} |`);
      if (route.type) lines.push(`| 路线类型 | ${route.type} |`);
      if (route.routeClass) lines.push(`| 路线分类 | ${route.routeClass} |`);
      if (route.keyNodes.length > 0) lines.push(`| 关键节点 | ${route.keyNodes.join('→')} |`);
      if (route.gpxSource) lines.push(`| 轨迹来源 | ${route.gpxSource} |`);
      if (route.trackMapPath) {
        const config = loadConfig();
        const webBase = config.webBaseUrl;
        if (webBase) {
          const encodedPath = encodeURIComponent(`upcoming/${trip.tripId}/${route.trackMapPath}`);
          const webUrl = `${webBase}/api/openmedia/raw?root=trip&path=${encodedPath}`;
          lines.push(`| 🗺️ 轨迹地图 | [查看](${webUrl}) |`);
        } else {
          lines.push(`| 🗺️ 轨迹地图 | [查看](${route.trackMapPath}) |`);
        }
      }
      if (route.tips) lines.push(`| ⚠️ 提示 | ${route.tips} |`);
      lines.push('');
    }
  }

  // 装备清单
  lines.push('## 装备清单');
  lines.push('');
  if (trip.equipment && Object.keys(trip.equipment).length > 0) {
    lines.push('| 类型 | 物品 |');
    lines.push('|------|------|');
    for (const [type, items] of Object.entries(trip.equipment)) {
      lines.push(`| ${type} | ${Array.isArray(items) ? items.join('、') : items} |`);
    }
    // 媒体文件列表
    const mediaDir = path.join(trip.outputDir, 'upcoming', trip.tripId, 'media');
    try {
      if (fs.existsSync(mediaDir)) {
        const mediaFiles = fs.readdirSync(mediaDir).filter(f => /\.(png|jpg|jpeg|gif|webp|bmp|svg|mp4|mov|avi|webm)$/i.test(f));
        if (mediaFiles.length > 0) {
          lines.push('');
          lines.push('### 📸 截图/媒体文件');
          lines.push('');
          for (const file of mediaFiles) {
            lines.push(`- [${file}](media/${encodeURIComponent(file)})`);
          }
          lines.push('');
        }
      }
    } catch (e) {
      // ignore media directory errors
    }
  } else {
    lines.push('| 类型 | 物品 |');
    lines.push('|------|------|');
    const eqDefaults = ['鞋', '衣', '包', '导航', '水', '食物', '防晒', '药品', '证件', '电子', '其他'];
    for (const t of eqDefaults) {
      lines.push(`| ${t} | |`);
    }
  }
  lines.push('');

  // 待办事项
  lines.push('## 待办事项');
  lines.push('');
  if (trip.todos.length > 0) {
    for (let i = 0; i < trip.todos.length; i++) {
      const todo = trip.todos[i];
      const text = typeof todo === 'string' ? todo : todo.text;
      const done = typeof todo === 'string' ? false : todo.done;
      const check = done ? 'x' : ' ';
      const suffix = done ? ' ✅' : '';
      lines.push(`${i + 1}. [${check}] ${text}${suffix}`);
    }
  } else {
    lines.push('1. [ ] 待补充');
  }
  lines.push('');

  lines.push(`*创建日期:${formatDate(trip.createdAt.split('T')[0])}*`);

  return lines.join('\n');
}

// ── 模板完整性检查 ──────────────────────────────────

/**
 * 对照 PLAN_TEMPLATE 检查生成的行程计划内容是否包含所有必需板块。
 * 在计划生成完成后调用,确保输出质量。
 *
 * @param {string} content - renderPlan 的输出
 * @returns {{ complete: boolean, missing: string[], warnings: string[] }}
 */
function validatePlan(content, trip) {
  const missing = [];
  const warnings = [];

  // ── 顶级章节检查(必须包含) ──
  const requiredHeadings = [
    { pattern: /^## 总览/m, name: '总览' },
    { pattern: /^## 每日安排/m, name: '每日安排' },
    { pattern: /^## 行程详情/m, name: '行程详情' },
    { pattern: /^## 徒步路线详情/m, name: '徒步路线详情' },
    { pattern: /^## 装备清单/m, name: '装备清单' },
    { pattern: /^## 待办事项/m, name: '待办事项' },
  ];

  for (const { pattern, name } of requiredHeadings) {
    if (!pattern.test(content)) {
      missing.push(name);
    }
  }

  // ── 总览表检查 ──
  if (/^## 总览/m.test(content)) {
    if (!/^\| 日期 \|/m.test(content)) {
      warnings.push('总览 - 缺少日期表头');
    }
    // 每个 day 应该有对应行
    if (trip && trip.days) {
      const overviewLines = (content.match(/^\| \d{1,2}\/\d{1,2} \|/gm) || []).length;
      if (overviewLines < trip.days.length) {
        warnings.push(`总览表 - 期望 ${trip.days.length} 行,实际 ${overviewLines} 行`);
      }
    }
  }

  // ── 每日安排检查 ──
  if (/^## 每日安排/m.test(content)) {
    if (trip && trip.days) {
      for (const day of trip.days) {
        const dayHeader = `DAY ${day.dayIndex}`;
        if (!content.includes(dayHeader)) {
          warnings.push(`每日安排 - 缺少 ${dayHeader}`);
        }
        // 地图链接检查
        if (day.nodes.length >= 2 && !content.includes(`[查看地图]`)) {
          warnings.push(`${dayHeader} - 缺少地图链接`);
        }
      }
    }
  }

  // ── 行程详情检查(至少 3 个文化分类) ──
  if (/^## 行程详情/m.test(content)) {
    const cultureHeadings = (content.match(/^### (?!DAY )(?!.*路线)(?!.*建议)(?!.*推荐)[^\n]+/gm) || []);
    if (cultureHeadings.length < 3) {
      warnings.push(`行程详情 - 仅 ${cultureHeadings.length} 个文化分类(建议 ≥3)`);
    }
    // 出行建议检查
    if (!/出行建议/i.test(content)) {
      warnings.push('行程详情 - 缺少「出行建议」节(交通/网红酒店/网红景点/网红活动)');
    }
  }

  // ── 徒步路线详情检查 ──
  if (/^## 徒步路线详情/m.test(content) && trip && trip.hikingRoutes && trip.hikingRoutes.length > 0) {
    for (const route of trip.hikingRoutes) {
      if (!content.includes(route.name)) {
        warnings.push(`徒步路线详情 - 缺少路线「${route.name}」`);
      }
    }
    // 必须有徒步路线表格字段
    if (!/\| 距离 \|/m.test(content)) {
      warnings.push('徒步路线详情 - 缺少徒步路线数据表格');
    }
  }

  // ── 装备清单检查 ──
  if (/^## 装备清单/m.test(content)) {
    if (!/\| 类型 \|/m.test(content)) {
      warnings.push('装备清单 - 缺少表格');
    }
  }

  // ── 待办事项检查 ──
  if (/^## 待办事项/m.test(content)) {
    if (!/\d+\. \[.\]/m.test(content)) {
      warnings.push('待办事项 - 无编号清单项');
    }
  }

  return {
    complete: missing.length === 0,
    missing,
    warnings,
  };
}

// ── 导出 ──────────────────────────────────────────────

module.exports = {
  // 常量
  STATUS,
  NODE_STATUS,
  INCOMPLETE_STATUSES,
  DEFAULT_OUTPUT_DIR,
  CONFIG_FILE,

  // 8 条主命令
  cmdHike,
  cmdInit,
  cmdStatus,
  cmdToday,
  cmdLog,
  cmdList,
  cmdSelect,
  // 汇总归档(hike-list <tripId>)
  cmdListArchive,

  // 辅助命令(Agent 逐步填充)
  cmdSetRequirements,
  cmdSetHikingRoutes,
  cmdSetDayNode,
  cmdSetDayWeather,
  cmdSetCulture,
  cmdSetEquipment,
  cmdSetTodos,
  cmdTodoDone,
  cmdSetMapUrl,
  cmdConfirm,
  cmdActivate,
  cmdGeneratePlan,
  cmdAddDay,
  cmdDelDay,
  cmdReorderDay,
  // 旧别名(向后兼容)
  cmdAddNode: cmdAddDay,
  cmdRemoveNode: cmdDelDay,
  cmdReorderNode: cmdReorderDay,

  // 新增:订单短信解析 + 实时行程修订
  cmdSetNodeStatus,
  parseOrderSMS,
  applySMSToTrip,
  compareActualVsPlan,

  // 节点类型 → 路线类型映射(地图渲染)
  getNodeRouteType,
  getNodeTransportLabel,
  getRouteTypesForDay,

  // GPX/KML 工具
  saveGpxFile,
  saveMediaFile,

  // 工具函数
  loadConfig,
  saveConfig,
  getOutputDir,
  generateTripId,
  getPlanFilename,
  formatDate,
  formatFullDate,
  getWeekday,
  getToday,
  addDays,
  renderPlan,
  renderDayMap,
  validatePlan,
};
