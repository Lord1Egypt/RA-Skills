import { fileURLToPath } from "node:url";

const DEFAULT_OPERATION_BASE_URL = "https://mesh.if.iqiyi.com/ai/zhipu";

const INSTALL_LINKS = {
  mac: "https://app.iqiyi.com/mac/player/index.html",
  windows: "https://dl-static.iqiyi.com/hz/IQIYIsetup_skill01.exe",
  uwp: "https://dl-static.iqiyi.com/hz/IQIYIsetup_skill01.exe",
};

const operationDefs = [
  {
    id: "video.search",
    endpoint: "/video/search",
    name: "视频搜索",
    source: "smart-assistant-operation",
    noLogin: true,
    inputs: ["q", "pageNum"],
    output: "message,prompt,col",
    intent: { type: "interact", action: "search", args: "q" },
    description: "通过指定关键词和页码搜索电影、电视剧、综艺、动漫、纪录片和各种视频。",
  },
  {
    id: "video.recommend",
    endpoint: "/video/recommend",
    name: "视频推荐",
    source: "smart-assistant-operation",
    noLogin: true,
    inputs: ["type", "style", "kind"],
    output: "message,prompt,col",
    intent: { type: "reference", action: "recommendation", args: "type;kind" },
    authOnlyKinds: ["history", "favor"],
    noLoginFallback: { kind: "hot" },
    description: "按视频类型、筛选词和来源返回推荐、热播、飙升、必看、新片、豆瓣或片库结果。",
  },
  {
    id: "video.details",
    endpoint: "/video/details",
    name: "视频详情",
    source: "smart-assistant-operation",
    noLogin: true,
    inputs: ["title", "season", "year"],
    output: "data,bloopers",
    intent: { type: "reference", action: "video", args: "Album/TV ID" },
    description: "按标题、季数和年份查询视频详情、演职员、周边视频和角色关系。",
  },
  {
    id: "star.search",
    endpoint: "/star/search",
    name: "明星详情和作品集",
    source: "smart-assistant-operation",
    noLogin: true,
    inputs: ["q"],
    output: "data",
    intent: { type: "reference", action: "star", args: "Star ID" },
    description: "按明星姓名查询基本介绍和参演视频。",
  },
  {
    id: "video.related",
    endpoint: "/video/related",
    name: "相关视频",
    source: "smart-assistant-operation",
    noLogin: true,
    inputs: ["title", "season", "year"],
    output: "col",
    intent: { type: "reference", action: "related", args: "TV ID" },
    description: "查询指定视频或节目的关联视频内容。",
  },
  {
    id: "video.episode",
    endpoint: "/video/episode",
    name: "选集",
    source: "smart-assistant-operation",
    noLogin: true,
    inputs: ["title", "season", "year"],
    output: "col",
    intent: { type: "reference", action: "episodes", args: "Album ID" },
    description: "查询电视剧、动漫、纪录片、课程或综艺的集/期信息。",
  },
  {
    id: "video.play",
    endpoint: "/video/play",
    name: "视频播放",
    source: "smart-assistant-operation",
    noLogin: true,
    inputs: ["title", "season", "year", "episode"],
    output: "data",
    intent: { type: "command", action: "play", args: "qips" },
    description: "明确播放意图默认由本地 qips action=play 承接；仅在 H5 降级、候选确认或强制后端解析时查询播放详情。",
  },
  {
    id: "playback.qips_open_or_control",
    name: "qips 播放与播控",
    source: "iqiyi-skill.qips",
    noLogin: true,
    inputs: ["qipsIntent"],
    output: "validated qips string or launch command",
    description: "使用 iqiyi-skill 内置 qips 拼接并校验 deeplink；用户表达播放、打开、跳转或播控意图时，可拉起客户端或交付系统 deeplink 命令。",
  },
  {
    id: "client.install_check",
    name: "客户端安装检测",
    source: "host_probe",
    noLogin: true,
    inputs: ["platform"],
    output: "installed boolean or unknown",
    description: "检测本机是否可拉起 qips 协议处理器。",
  },
  {
    id: "client.download_link",
    name: "客户端下载链接",
    source: "product_confirmed_url",
    noLogin: true,
    inputs: ["platform"],
    output: "install URL",
    description: "返回产品确认后的 Mac 或 PCA/Windows/UWP 客户端安装地址。",
  },
  {
    id: "fallback.h5_play_url",
    name: "H5 播放降级",
    source: "web_fallback",
    noLogin: true,
    inputs: ["url"],
    output: "H5 URL plus install tip",
    description: "无客户端时返回 H5 播放地址，并提示安装客户端可获得更完整体验。",
  },
];

const operationById = new Map(operationDefs.map((item) => [item.id, item]));
const RECOMMEND_KIND_ALIASES = new Map([
  ["推荐", "suggest"],
  ["热播", "hot"],
  ["飙升", "soar"],
  ["必看", "top"],
  ["新片", "new"],
  ["豆瓣", "douban"],
  ["历史", "history"],
  ["收藏", "favor"],
]);

const RECOMMEND_STYLE_CATALOG = {
  TvSeries: [
    "古装",
    "战争",
    "谍战",
    "爱情",
    "罪案",
    "悬疑",
    "家庭",
    "军旅",
    "喜剧",
    "都市",
    "武侠",
    "言情",
    "偶像",
    "青春",
    "农村",
    "穿越",
    "奇幻",
    "历史",
    "年代",
    "科幻",
    "生活",
    "剧情",
    "励志",
    "婚姻",
    "警匪",
    "犯罪",
    "推理",
    "商战",
    "宫廷",
    "仙侠",
    "神话",
    "动作",
    "复仇",
    "惊悚",
    "其他",
  ],
  ShortDrama: [
    "穿越",
    "逆袭",
    "重生",
    "爱情",
    "玄幻",
    "现代言情",
    "总裁",
    "虐恋",
    "甜宠",
    "神豪",
    "女性成长",
    "古风权谋",
    "家庭伦理",
    "复仇",
    "悬疑推理",
    "古风言情",
    "生活",
    "刑侦",
    "恐怖",
  ],
  Movie: [
    "喜剧",
    "动画",
    "动作",
    "爱情",
    "恐怖",
    "战争",
    "惊悚",
    "枪战",
    "科幻",
    "犯罪",
    "悬疑",
    "奇幻",
    "剧情",
    "青春",
    "冒险",
    "家庭",
    "少儿",
    "警匪",
    "历史",
    "武侠",
    "伦理",
    "灾难",
    "传记",
    "运动",
    "音乐",
    "魔幻",
    "歌舞",
    "戏曲",
    "玄幻",
    "悲剧",
    "史诗",
    "西部",
    "纪录片",
    "其他",
  ],
  Variety: ["喜剧", "真人秀", "音乐", "脱口秀", "观察", "访谈", "游戏", "晚会", "曲艺", "竞技", "竞演", "文化", "其他"],
  Comic: ["玄幻", "奇幻", "武侠", "恋爱", "搞笑", "冒险", "热血", "治愈", "科幻", "推理", "竞技", "励志", "机战", "偶像", "其他"],
  Manga: [
    "逆袭",
    "穿越",
    "大女主",
    "系统",
    "玄幻",
    "搞笑",
    "废柴",
    "悬疑",
    "恋爱",
    "末日",
    "战神",
    "扮猪吃老虎",
    "修仙",
    "觉醒",
    "无敌",
    "科幻",
    "开局",
    "异能",
  ],
  Documentary: ["自然", "历史", "人文", "美食", "医疗", "萌宠", "财经", "罪案", "竞技", "灾难", "军事", "探险", "社会", "科技", "旅游", "其他"],
};

const RECOMMEND_TYPE_ALIASES = new Map([
  ["电视剧", "TvSeries"],
  ["剧集", "TvSeries"],
  ["短剧", "ShortDrama"],
  ["电影", "Movie"],
  ["影片", "Movie"],
  ["综艺", "Variety"],
  ["动漫", "Comic"],
  ["动画", "Comic"],
  ["漫剧", "Manga"],
  ["纪录片", "Documentary"],
]);

const GLOBAL_STYLE_ALIASES = [
  { patterns: ["全家", "合家欢", "一家人", "老少皆宜", "亲子", "阖家"], style: "家庭" },
  { patterns: ["小朋友", "小孩", "儿童", "孩子"], style: "少儿" },
  { patterns: ["轻松", "搞笑", "逗乐", "开心", "爆笑"], style: "喜剧" },
  { patterns: ["温馨", "治愈", "暖心"], style: "治愈" },
  { patterns: ["热血", "燃"], style: "热血" },
  { patterns: ["烧脑", "推理", "破案"], style: "悬疑" },
  { patterns: ["刑侦", "警察", "案件"], style: "警匪" },
  { patterns: ["宇宙", "未来", "科技感"], style: "科幻" },
  { patterns: ["古代", "古风"], style: "古装" },
  { patterns: ["职场", "城市"], style: "都市" },
  { patterns: ["恋爱", "甜甜", "甜蜜"], style: "爱情" },
];

function pickKnownInput(operation, input) {
  return operation.inputs.reduce((body, key) => {
    if (input[key] !== undefined && input[key] !== null && input[key] !== "") {
      body[key] = input[key];
    }
    return body;
  }, {});
}

function hasAuthorization(options) {
  return typeof options.authorization === "string" && options.authorization.trim() !== "";
}

function normalizeRecommendKind(body) {
  if (typeof body.kind !== "string") return;
  body.kind = RECOMMEND_KIND_ALIASES.get(body.kind.trim()) || body.kind.trim();
}

function normalizeRecommendType(type) {
  if (typeof type !== "string") return type;
  const trimmed = type.trim();
  return RECOMMEND_TYPE_ALIASES.get(trimmed) || trimmed;
}

function getSupportedStylesForType(type) {
  const normalizedType = normalizeRecommendType(type);
  if (RECOMMEND_STYLE_CATALOG[normalizedType]) return RECOMMEND_STYLE_CATALOG[normalizedType];
  return [...new Set(Object.values(RECOMMEND_STYLE_CATALOG).flat())];
}

function findSupportedStyle(style, supportedStyles) {
  if (typeof style !== "string") return style;
  const trimmed = style.trim();
  if (supportedStyles.includes(trimmed)) return trimmed;

  const directContained = supportedStyles.find((supported) => trimmed.includes(supported));
  if (directContained) return directContained;

  const alias = GLOBAL_STYLE_ALIASES.find(({ patterns, style: aliasStyle }) => {
    return supportedStyles.includes(aliasStyle) && patterns.some((pattern) => trimmed.includes(pattern));
  });

  return alias ? alias.style : trimmed;
}

export function getRecommendStyleCatalog() {
  return Object.fromEntries(
    Object.entries(RECOMMEND_STYLE_CATALOG).map(([type, styles]) => [type, [...styles]]),
  );
}

export function normalizeRecommendStyles(style, type) {
  const styleList = Array.isArray(style) ? style : [style];
  const supportedStyles = getSupportedStylesForType(type);
  const warnings = [];
  const styles = [];

  for (const item of styleList) {
    if (item === undefined || item === null || item === "") continue;
    const normalized = findSupportedStyle(item, supportedStyles);
    if (!styles.includes(normalized)) styles.push(normalized);
    if (typeof item === "string" && item.trim() !== normalized) {
      warnings.push(`style=${item} normalized to ${normalized}`);
    }
  }

  return { styles, warnings };
}

export function getClientInstallLink(platform = "windows") {
  const normalized = String(platform).trim().toLowerCase();
  if (normalized === "macos" || normalized === "darwin") return INSTALL_LINKS.mac;
  if (normalized === "win" || normalized === "windows-uwp") return INSTALL_LINKS.windows;
  if (!INSTALL_LINKS[normalized]) {
    throw new Error(`Unsupported install platform: ${platform}`);
  }
  return INSTALL_LINKS[normalized];
}

export function buildOperationRequest(operationId, input = {}, options = {}) {
  const operation = operationById.get(operationId);
  if (!operation || !operation.endpoint) {
    throw new Error(`Unsupported Web API operation: ${operationId}`);
  }

  const body = pickKnownInput(operation, input);
  const headers = { "content-type": "application/json" };
  const warnings = [];

  if (operationId === "video.recommend") {
    body.type = normalizeRecommendType(body.type);
    normalizeRecommendKind(body);
    if (body.style !== undefined) {
      const normalizedStyle = normalizeRecommendStyles(body.style, body.type);
      body.style = normalizedStyle.styles;
      warnings.push(...normalizedStyle.warnings);
    }
  }

  if (hasAuthorization(options)) {
    headers.Authorization = options.authorization;
  }

  if (
    operation.authOnlyKinds &&
    operation.authOnlyKinds.includes(body.kind) &&
    !hasAuthorization(options)
  ) {
    const originalKind = body.kind;
    body.kind = operation.noLoginFallback.kind;
    warnings.push(`kind=${originalKind} requires Authorization; downgraded to ${body.kind}`);
  }

  return {
    method: "POST",
    endpoint: operation.endpoint,
    url: `${options.baseUrl || DEFAULT_OPERATION_BASE_URL}${operation.endpoint}`,
    headers,
    body,
    warnings,
  };
}

function normalizeItem(item) {
  if (!item || typeof item !== "object") return item;
  const normalized = {};

  for (const key of ["id", "title", "name", "desc", "description", "url"]) {
    if (item[key] !== undefined) normalized[key] = item[key];
  }

  return { ...item, ...normalized };
}

function formatItemLine(item, index) {
  if (!item || typeof item !== "object") return `${index + 1}. ${String(item)}`;

  const title = item.title || item.name || item.id || `结果 ${index + 1}`;
  const desc = item.desc || item.description;
  const url = item.url;
  const titleLine = desc ? `${index + 1}. ${title} - ${desc}` : `${index + 1}. ${title}`;

  return url ? `${titleLine}\n${url}` : titleLine;
}

function formatDataText(data) {
  if (!data || typeof data !== "object") return String(data ?? "");

  const title = data.title || data.name || data.id;
  const desc = data.desc || data.description || data.intro;
  const url = data.url || data.playUrl || data.h5Url;
  const parts = [];

  if (title && desc) parts.push(`${title} - ${desc}`);
  else if (title) parts.push(String(title));
  else if (desc) parts.push(String(desc));

  if (url) parts.push(String(url));

  return parts.length > 0 ? parts.join("\n") : JSON.stringify(data, null, 2);
}

export function formatOperationResponse(payload = {}) {
  const base = {
    message: payload.message,
    prompt: payload.prompt,
    intent: payload.intent,
  };

  if (Array.isArray(payload.col)) {
    const items = payload.col.map(normalizeItem);
    return {
      kind: "collection",
      ...base,
      items,
      text: items.map(formatItemLine).join("\n"),
    };
  }

  if (payload.data !== undefined) {
    return {
      kind: "data",
      ...base,
      data: payload.data,
      text: formatDataText(payload.data),
    };
  }

  return {
    kind: "message",
    ...base,
    text: payload.message || payload.prompt || JSON.stringify(payload, null, 2),
  };
}

export async function executeOperation(operationId, input = {}, options = {}) {
  const request = buildOperationRequest(operationId, input, options);
  const fetchImpl = options.fetchImpl || globalThis.fetch;

  if (typeof fetchImpl !== "function") {
    throw new Error("No fetch implementation available for executing iqiyi-skill operation");
  }

  const response = await fetchImpl(request.url, {
    method: request.method,
    headers: request.headers,
    body: JSON.stringify(request.body),
  });

  if (!response.ok) {
    throw new Error(`iqiyi-skill operation failed: ${response.status}`);
  }

  const raw = await response.json();

  return {
    request,
    raw,
    formatted: formatOperationResponse(raw),
  };
}

export function getIqiyiSkillCatalog() {
  return {
    name: "iqiyi-skill",
    version: "0.2.0",
    scope: "no-login-mvp",
    dataSource: {
      title: "智能助理",
      url: "https://iq.feishu.cn/wiki/WRmFw6W6bildBJkGTBnc1gtRnad",
      operationBaseUrl: DEFAULT_OPERATION_BASE_URL,
      transport: "POST JSON",
      authorization: "Authorization header is passed through when supplied; no-login MVP downgrades auth-only sources.",
    },
    reusedSkills: [],
    embeddedCapabilities: ["qips"],
    client: {
      installLinks: INSTALL_LINKS,
    },
    fallback: {
      noClient: {
        strategy: "return_h5_play_url_and_download_tip",
      },
    },
    mvpBoundary: {
      excluded: [
        "account.login_binding",
        "account.qr_or_password_login",
        "membership.status_real_auth",
        "recommend.personalized_login_required",
        "native.new_command",
        "backend.new_api",
      ],
    },
    operations: operationDefs,
  };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const [, , operationId, inputJson] = process.argv;

  if (operationId) {
    const input = inputJson ? JSON.parse(inputJson) : {};
    const result = await executeOperation(operationId, input);
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(JSON.stringify(getIqiyiSkillCatalog(), null, 2));
  }
}
