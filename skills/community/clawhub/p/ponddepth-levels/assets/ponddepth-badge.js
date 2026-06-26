// PondDepth badge in Control UI topbar-left (MVP)
// - Hover shows: progress + level description + recommended skills status + OpenClaw news
// - Data sources:
//   - Level: localStorage ponddepth.level (manual for now)
//   - Skills status: /ui/assets/skills-status.json (generated from `openclaw skills list --json`)

const LEVELS = {
  B1: {
    titleZh: "开坑学徒",
    titleEn: "Pond Digger",
    descZh: "你已经成功把 OpenClaw 跑起来了。下一步：把它接到一个常用入口（IM/渠道），让它随叫随到。",
    descEn: "OpenClaw is running. Next: connect it to a daily entry (IM/channel) so it’s always reachable.",
  },
  B2: {
    titleZh: "打桩工",
    titleEn: "Foundation Setter",
    descZh: "基础打牢：你开始把 OpenClaw 接入日常沟通链路。下一步：装一批新手必备 skills，让它能做具体活。",
    descEn: "Your foundation is set: OpenClaw is in your daily chat flow. Next: install a starter set of skills to do real work.",
  },
  B3: {
    titleZh: "通水匠",
    titleEn: "Water Router",
    descZh: "你已经把能力‘通水’到技能层。下一步：做一个真实需求交付（不是 demo），让它替你省时间。",
    descEn: "Capabilities are flowing through skills. Next: ship one real deliverable (not a demo) that saves you time.",
  },
  B4: {
    titleZh: "修塘监工",
    titleEn: "Pond Foreman",
    descZh: "你已经完成一个真实需求。下一步：把流程固化（模板/定时/监控），让它稳定长期运行。",
    descEn: "You’ve shipped a real need. Next: harden it into a stable system (templates/schedules/monitoring).",
  },
  B5: {
    titleZh: "塘主",
    titleEn: "Pond Owner",
    descZh: "你已完成与主人对齐：目标/边界/偏好清晰。下一步：进入投喂阶段，让自动化持续产出。",
    descEn: "You’re aligned: goals, boundaries, and preferences are clear. Next: move to automation that produces daily.",
  },

  F1: {
    titleZh: "撒料新手",
    titleEn: "First Feeder",
    descZh: "你开始用自动化喂虾：有了第一个稳定的省时动作。下一步：扩大到 2-3 个高频场景。",
    descEn: "Your first automation is live. Next: expand to 2–3 high-frequency scenarios.",
  },
  F2: {
    titleZh: "配方员",
    titleEn: "Feed Mixer",
    descZh: "你能组合多个 skills 形成配方。下一步：把配方参数化，形成可复用 workflow。",
    descEn: "You can combine skills into a ‘recipe’. Next: parameterize it into a reusable workflow.",
  },
  F3: {
    titleZh: "训虾师",
    titleEn: "Lobster Trainer",
    descZh: "你能让 OpenClaw 按规则跑流程。下一步：加入失败告警/重试/对账，提升可靠性。",
    descEn: "Your workflows follow rules. Next: add alerts/retries/reconciliation to improve reliability.",
  },
  F4: {
    titleZh: "增殖官",
    titleEn: "Growth Manager",
    descZh: "你开始关注规模与稳定性。下一步：把成果沉淀成模板/文档/可迁移方案。",
    descEn: "You’re thinking scale and stability. Next: package results into templates/docs that others can reuse.",
  },
  F5: {
    titleZh: "养殖大师",
    titleEn: "Aqua Master",
    descZh: "你有可复用的个人自动化体系。下一步：进入售卖阶段，把价值交付做成闭环。",
    descEn: "You have a reusable automation system. Next: move to delivery loops that create measurable value.",
  },

  S1: {
    titleZh: "摆摊小贩",
    titleEn: "Market Starter",
    descZh: "你能把成果打包输出（模板/清单/脚本）。下一步：让 1 个朋友能复现使用。",
    descEn: "You can package outputs (templates/checklists/scripts). Next: help one friend reproduce it end-to-end.",
  },
  S2: {
    titleZh: "订单管家",
    titleEn: "Order Keeper",
    descZh: "你能持续交付并收集反馈。下一步：量化节省时间/成本，形成 ROI。",
    descEn: "You deliver repeatedly and learn from feedback. Next: quantify time/cost saved to prove ROI.",
  },
  S3: {
    titleZh: "利润操盘手",
    titleEn: "Margin Operator",
    descZh: "你开始做效率/成本的优化。下一步：把方法论写成案例复盘。",
    descEn: "You’re optimizing efficiency and cost. Next: write a short case study with the playbook.",
  },
  S4: {
    titleZh: "品牌老板",
    titleEn: "Brand Builder",
    descZh: "你有稳定口碑与案例。下一步：把作品发布到社区/仓库，形成传播。",
    descEn: "You have strong cases and reputation. Next: publish to a community/repo to build distribution.",
  },
  S5: {
    titleZh: "虾王",
    titleEn: "Lobster King",
    descZh: "你已经形成持续产出的高手工作流。下一步：扩展到团队/社群规模。",
    descEn: "You run an elite, repeatable workflow. Next: scale it to a team or community.",
  },
};

const RECOMMENDED_SKILLS = [
  { name: "skill-vetter", whyZh: "装新技能先过安全门", whyEn: "Safety gate before installing new skills" },
  { name: "proactive-agent", whyZh: "让 Agent 主动推进 + 可复盘", whyEn: "Make the agent proactive and reviewable" },
  { name: "summarize", whyZh: "链接/视频/文章快速提炼", whyEn: "Fast summaries for links, videos, and articles" },
  { name: "find-skills", whyZh: "按需求找合适的技能", whyEn: "Find the right skill for a job" },

  { name: "openai-image-gen", whyZh: "批量生成图标/海报等图片", whyEn: "Batch-generate images" },
  { name: "openai-whisper", whyZh: "本地语音转文字（无需 key）", whyEn: "Local speech-to-text" },
  { name: "nano-pdf", whyZh: "用自然语言批量改 PDF", whyEn: "Edit PDFs with natural language" },

  { name: "github", whyZh: "工程协作（PR/CI/issue）", whyEn: "Engineering workflow (PR/CI/issues)" },
  { name: "feishu-doc", whyZh: "飞书文档读写", whyEn: "Read/write Feishu docs" },
  { name: "feishu-drive", whyZh: "云盘文件/文件夹管理", whyEn: "Manage drive files/folders" },
  { name: "imsg", whyZh: "iMessage/SMS 发消息", whyEn: "Send iMessage/SMS" },
  { name: "weather", whyZh: "查天气与预报", whyEn: "Weather and forecasts" },
];

// Extra discovery pool: we will prioritize NOT installed skills from this list.
const DISCOVERY_SKILLS = [
  // From ClawHub "Popular skills" + common productivity picks
  { name: "self-improving-agent", whyZh: "自动复盘+持续改进", whyEn: "Continuous improvement memory" },
  { name: "tavily-search", whyZh: "更准的网页搜索", whyEn: "AI-optimized web search" },
  { name: "caldav-calendar", whyZh: "同步/查询 CalDAV 日历", whyEn: "Sync/query CalDAV calendars" },
  { name: "answeroverflow", whyZh: "搜 Discord 讨论答案", whyEn: "Search Discord discussions" },

  "find-skills",
  "gog",
  "summarize",
  "github",
  "weather",
  "proactive-agent",
  "sonoscli",
  "notion",
  "nano-pdf",

  // Extra variety
  { name: "trello", whyZh: "管理 Trello 看板", whyEn: "Manage Trello boards" },
  { name: "slack", whyZh: "在 Slack 里执行动作", whyEn: "Control Slack" },
  "himalaya",
  "obsidian",
  "things-mac",
  "mcporter",
  "peekaboo",
  "video-frames",
  "openhue",
  "eightctl",
  "openai-whisper-api",
  "openai-image-gen",
  "healthcheck",
  "skill-creator",
  "clawhub",
];

const NEWS = [
  { title: "OpenClaw Docs", url: "https://docs.openclaw.ai" },
  { title: "OpenClaw GitHub", url: "https://github.com/openclaw/openclaw" },
  { title: "Join Community Discord", url: "https://discord.com/invite/clawd" },
];

const LOCALE = (localStorage.getItem("ponddepth.locale") || ((typeof navigator !== "undefined" && (navigator.language || "").toLowerCase().startsWith("zh")) ? "zh" : "en"));
const t = (zh, en) => (LOCALE === "zh" ? zh : en);

// Best-effort zh translations for skill descriptions (names stay English)
const ZH_SKILL_DESC = {
  "skill-vetter": "装新技能先过安全门（风险扫描/权限核对）",
  "proactive-agent": "让 Agent 主动推进：WAL 记忆、复盘、自动跟进",
  "summarize": "把链接/视频/文章快速提炼成要点",
  "find-skills": "按需求帮你找合适的技能并给安装建议",
  "github": "用 gh 管 PR/CI/Issue（工程协作）",
  "gh-issues": "批量拉取 GitHub issues 并自动修复/提 PR",
  "gog": "Google Workspace：Gmail/日历/Drive/Docs 的 CLI",
  "himalaya": "邮件客户端（IMAP/SMTP）：收发/搜索/整理",
  "imsg": "iMessage/SMS：查历史/发消息",
  "weather": "查天气与预报（wttr.in/Open-Meteo）",
  "apple-notes": "Apple 备忘录：创建/搜索/编辑/导出",
  "apple-reminders": "Apple 提醒事项：添加/修改/完成/删除",
  "bear-notes": "Bear 笔记：创建/搜索/管理",
  "blogwatcher": "监控博客与 RSS/Atom 更新",
  "blucli": "控制 BluOS（发现/播放/分组/音量）",
  "camsnap": "从 RTSP/ONVIF 摄像头抓图/录片段",
  "obsidian": "Obsidian 笔记库：读写 Markdown/自动化",
  "openai-whisper": "本地 Whisper 语音转文字（无需 API key）",
  "openai-whisper-api": "用 OpenAI Whisper API 做转写",
  "nano-pdf": "用自然语言批量编辑 PDF",
  "video-frames": "用 ffmpeg 抽帧/截短片",
  "sonoscli": "控制 Sonos 音箱（播放/分组/音量）",
  "openhue": "控制 Philips Hue 灯光/场景",
  "feishu-doc": "飞书文档：读写/追加/插入/表格",
  "feishu-drive": "飞书云盘：列目录/新建文件夹/移动/删除",
  "feishu-wiki": "飞书知识库：导航/搜索/创建/移动",
  "feishu-perm": "飞书权限：共享/协作者/权限排查",
};

function localizeSkillWhy(name, why) {
  if (LOCALE !== "zh") return String(why || "");
  const k = String(name || "").trim();
  // Prefer model-generated zh map if available
  try {
    const m = window.__ponddepthSkillsZh;
    if (m && typeof m === "object" && typeof m[k] === "string" && m[k].trim()) return m[k].trim();
  } catch {}

  const hit = ZH_SKILL_DESC[k];
  return hit || String(why || "");
}

let SKILLS_ZH_LOADING = null;
async function loadSkillsZhMap() {
  if (LOCALE !== "zh") return null;
  try {
    if (window.__ponddepthSkillsZh && typeof window.__ponddepthSkillsZh === "object") return window.__ponddepthSkillsZh;
  } catch {}

  if (SKILLS_ZH_LOADING) return SKILLS_ZH_LOADING;
  SKILLS_ZH_LOADING = (async () => {
    try {
      const res = await fetch(`/ui/assets/skills-zh.json?_=${Date.now()}`, { cache: "no-store" });
      if (!res.ok) return null;
      const j = await res.json();
      const items = j && j.items && typeof j.items === "object" ? j.items : null;
      if (items) {
        try { window.__ponddepthSkillsZh = items; } catch {}
      }
      return items;
    } catch {
      return null;
    }
  })();
  return SKILLS_ZH_LOADING;
}

// Make bilingual titles display cleanly per locale
function cleanTitle(s) {
  const str = String(s || "");
  if (LOCALE === "zh") {
    // Keep leading Chinese part (strip trailing English)
    return str.replace(/\s+[A-Za-z][\s\S]*$/, "").trim() || str.trim();
  }
  // Keep trailing English part (strip leading Chinese)
  const en = str.replace(/^[\u4e00-\u9fff\s]+/, "").trim();
  return en || str.trim();
}

function iconUrlForLevel(levelId) {
  const id = String(levelId || "B1").toUpperCase();
  const base = "/ui/assets/ponddepth-icons";
  // We ship: B1..B5, F1..F5, S1..S5 as PNG (transparent)
  if (/^[BFS][1-5]$/.test(id)) return `${base}/${id}.png`;
  return `${base}/B1.png`;
}


function getLevelId() {
  return (localStorage.getItem("ponddepth.level.auto") || localStorage.getItem("ponddepth.level") || "B1").toUpperCase();
}

function setLevelId(v) {
  localStorage.setItem("ponddepth.level", (v || "B1").toUpperCase());
  localStorage.setItem("ponddepth.level.auto", (v || "B1").toUpperCase());
  renderBadge();
}

function clamp(n, a, b) {
  return Math.max(a, Math.min(b, n));
}

function normSkillKey(s) {
  return String(s || "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^a-z0-9\-]/g, "")
    .replace(/\-+/g, "-");
}

const SKILL_KEY_ALIASES = {
  // ClawHub slug -> local installed skill name
  "tavily-search": "tavily",
};

function resolveSkillKey(name) {
  const k = normSkillKey(name);
  return SKILL_KEY_ALIASES[k] || k;
}

async function loadSkillsStatus() {
  // Prefer live gateway RPC for accurate install/enable/ready states
  try {
    const app = getOpenClawApp && getOpenClawApp();
    const client = app && app.client ? app.client : null;
    if (client) {
      const res = await client.request("skills.status", {});
      if (res) {
        try { res.__ponddepthSource = "rpc"; } catch {}
        return res;
      }
    }
  } catch {}

  // Fallback: local snapshot file (may be stale)
  try {
    const res = await fetch(`/ui/assets/skills-status.json?_=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) return null;
    const j = await res.json();
    try { j.__ponddepthSource = "snapshot"; } catch {}
    return j;
  } catch {
    return null;
  }
}


// Companion day count (distinct message days)
// Source: gateway chat.history for current sessionKey; computed in user's local timezone
const COMPANION_CACHE_KEY = "ponddepth.companion.cache.v1";


let PONDDEPTH_METRICS_CACHE = null;
const PONDDEPTH_METRICS_URL = "/ui/assets/companion-metrics.json";

const OPENCLAW_NEWS_URL = "/ui/assets/openclaw-news.json";
const OPENCLAW_TIP_URL = "/ui/assets/openclaw-tip.json";
const CLAWHUB_STATUS_URL = "/ui/assets/clawhub-status.json";

let __PONDDEPTH_CLAWHUB_STATUS = null;
async function loadClawhubStatus() {
  try {
    if (__PONDDEPTH_CLAWHUB_STATUS) return __PONDDEPTH_CLAWHUB_STATUS;
    const res = await fetch(`${CLAWHUB_STATUS_URL}?_=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) return null;
    const j = await res.json();
    __PONDDEPTH_CLAWHUB_STATUS = j;
    return j;
  } catch {
    return null;
  }
}

async function loadOpenClawTip() {
  try {
    const res = await fetch(`${OPENCLAW_TIP_URL}?_=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) return null;
    const j = await res.json();
    if (!j) return null;
    const tip = t(j.tipZh || "", j.tipEn || "");
    return String(tip || "").trim();
  } catch {
    return null;
  }
}

async function loadOpenClawNews() {
  try {
    const res = await fetch(`${OPENCLAW_NEWS_URL}?_=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) return null;
    const j = await res.json();
    const items = j && Array.isArray(j.items) ? j.items : null;
    return items;
  } catch {
    return null;
  }
}

async function loadPondDepthMetrics() {
  try {
    const res = await fetch(`${PONDDEPTH_METRICS_URL}?_=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) return null;
    const j = await res.json();
    PONDDEPTH_METRICS_CACHE = j;
    // also persist a tiny cache for badge render
    if (j && typeof j.level === "string") {
      localStorage.setItem("ponddepth.level.auto", j.level);
    }
    if (j && typeof j.levelProgressPct === "number") {
      localStorage.setItem("ponddepth.level.pct", String(j.levelProgressPct));
    }
    if (j && typeof j.companionDays === "number") {
      localStorage.setItem("ponddepth.days", String(j.companionDays));
    }
    return j;
  } catch {
    return null;
  }
}

function formatDateKey(tsMs, timeZone) {
  try {
    const dtf = new Intl.DateTimeFormat("en-CA", {
      timeZone,
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
    return dtf.format(new Date(tsMs));
  } catch {
    // fallback: local
    const d = new Date(tsMs);
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return `${y}-${m}-${day}`;
  }
}

function resolveUserTimeZone() {
  try {
    return Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC";
  } catch {
    return "UTC";
  }
}

function getOpenClawApp() {
  try {
    return document.querySelector("openclaw-app") || null;
  } catch {
    return null;
  }
}

async function loadCompanionDayCount() {
  // Preferred source: precomputed companion-metrics.json (derived from local session logs).
  // Fallback: session chat logs via gateway RPC (when sessionKey is available).

  try {
    if (PONDDEPTH_METRICS_CACHE && typeof PONDDEPTH_METRICS_CACHE.companionDays === "number") {
      return Math.max(1, PONDDEPTH_METRICS_CACHE.companionDays);
    }
    const j = await loadPondDepthMetrics();
    if (j && typeof j.companionDays === "number") return Math.max(1, j.companionDays);
  } catch {}

  // Cache for 60 seconds from chat.history

  try {
    const cachedRaw = localStorage.getItem(COMPANION_CACHE_KEY);
    if (cachedRaw) {
      const cached = JSON.parse(cachedRaw);
      if (cached && typeof cached.ts === "number" && Date.now() - cached.ts < 60 * 1000) {
        if (typeof cached.count === "number") return cached.count;
      }
    }
  } catch {}

  const tz = resolveUserTimeZone();
  const app = getOpenClawApp();
  const client = app && app.client ? app.client : null;
  const sessionKey = app && app.sessionKey ? app.sessionKey : null;
  if (!client || !sessionKey) {
    return 1;
  }

  try {
    const res = await client.request("chat.history", { sessionKey, limit: 2000 });
    const msgs = Array.isArray(res && res.messages) ? res.messages : [];
    const days = new Set();
    for (const m of msgs) {
      const ts = typeof m.timestamp === "number" ? m.timestamp : typeof m.ts === "number" ? m.ts : null;
      if (!ts) continue;
      days.add(formatDateKey(ts, tz));
    }
    const count = Math.max(1, days.size);
    try {
      localStorage.setItem(COMPANION_CACHE_KEY, JSON.stringify({ ts: Date.now(), count }));
    } catch {}
    return count;
  } catch {
    return 1;
  }
}

function skillMapFromStatus(statusJson) {
  const map = new Map();
  const skills = statusJson?.skills || [];
  for (const s of skills) {
    const entry = {
      eligible: !!s.eligible,
      disabled: !!s.disabled,
      ready: !!s.eligible && !s.disabled && !s.blockedByAllowlist,
      blockedByAllowlist: !!s.blockedByAllowlist,
      description: s.description || "",
    };
    map.set(s.name, entry);
    map.set(normSkillKey(s.name), entry);
  }
  return map;
}

let pill, label, mono, pop, iconImg;

function* walkNodes(root) {
  if (!root) return;
  const stack = [root];
  while (stack.length) {
    const node = stack.pop();
    if (!node) continue;
    if (node.nodeType === 1) {
      yield node;
      if (node.shadowRoot) stack.push(node.shadowRoot);
      const kids = node.children ? Array.from(node.children) : [];
      for (let i = kids.length - 1; i >= 0; i--) stack.push(kids[i]);
    } else if (node instanceof ShadowRoot || node instanceof DocumentFragment) {
      const kids = node.children ? Array.from(node.children) : [];
      for (let i = kids.length - 1; i >= 0; i--) stack.push(kids[i]);
    }
  }
}

function findTopbarLeft() {
  for (const el of walkNodes(document.documentElement)) {
    if (el.classList && el.classList.contains("topbar-left")) return el;
  }
  return null;
}

function ensureStyle() {
  const STYLE_ID = "ponddepth-style-v3";
  const existing = document.getElementById(STYLE_ID);
  if (existing) {
    try {
      const cur = existing.getAttribute("data-locale");
      if (cur === LOCALE) return;
      existing.remove();
    } catch {
      // fall through
    }
  }
  // remove legacy style ids if present
  try { document.getElementById("ponddepth-style")?.remove?.(); } catch {}

  const style = document.createElement("style");
  style.id = STYLE_ID;
  style.setAttribute("data-locale", LOCALE);
  style.textContent = `
    .pill.ponddepth { cursor: pointer; user-select:none; }
    .ponddepth-pop {
      position: fixed;
      z-index: 9999;
      width: 360px;
      max-width: calc(100vw - 24px);
      background: rgba(18,27,46,0.96);
      border: 1px solid rgba(110,231,255,0.18);
      border-radius: 14px;
      box-shadow: 0 18px 60px rgba(0,0,0,0.35);
      padding: 10px 10px;
      color: #e8eefc;
      font: 12px/1.35 ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "PingFang SC", "Noto Sans CJK SC", "Microsoft YaHei", Arial;
    }
    .ponddepth-pop h4 { margin: 0 0 6px 0; font-size: 12px; color: rgba(232,238,252,0.95); }
    .ponddepth-pop .muted { color: rgba(232,238,252,0.68); }
    .ponddepth-level-cur { color: rgba(232,238,252,0.95); font-weight: 900; }
    .ponddepth-level-icon { width: 18px; height: 18px; vertical-align: -3px; margin-right: 4px; }
    .ponddepth-pill-icon { width: 16px; height: 16px; margin-right: 2px; }
    .ponddepth-help {
      display:inline-flex;
      align-items:center;
      justify-content:center;
      width: 16px;
      height: 16px;
      margin-left: 6px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,0.22);
      background: rgba(255,255,255,0.06);
      color: rgba(232,238,252,0.85);
      font-size: 11px;
      cursor: default;
      user-select: none;
    }
    .ponddepth-levels-panel {
      display:none;
      position: absolute;
      left: 10px;
      right: 10px;
      top: 36px; /* below the level row */
      z-index: 20;
      padding: 8px 8px;
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,0.14);
      background: rgba(10,16,28,0.96);
      box-shadow: 0 18px 50px rgba(0,0,0,0.45);
    }
    .ponddepth-levels-panel .row2 { display:flex; align-items:center; justify-content:space-between; gap:10px; }
    .ponddepth-levels-panel .it { padding: 3px 0; }
    .ponddepth-levels-panel .it.cur { color: rgba(110,231,255,0.98); font-weight: 900; }
    .ponddepth-tip { color: rgba(232,238,252,0.86); padding: 6px 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.10); border-radius: 10px; }
    .ponddepth-note { font-style: italic; color: rgba(232,238,252,0.72); }
    .ponddepth-refresh-btn { margin-left: 8px; font-size: 11px; padding: 2px 6px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.18); background: rgba(255,255,255,0.06); color: rgba(232,238,252,0.82); cursor: pointer; }
    .ponddepth-refresh-btn:hover { background: rgba(255,255,255,0.10); }
    .ponddepth-pop .row { display:flex; align-items:center; justify-content:space-between; gap:10px; }
    .ponddepth-pop .bar { height: 10px; background: rgba(255,255,255,0.10); border-radius: 999px; overflow:hidden; }
    .ponddepth-pop .bar > div { height:100%; background: linear-gradient(90deg, rgba(110,231,255,0.95), rgba(167,139,250,0.95)); width: 0%; }
    .ponddepth-pop ul { margin: 6px 0 0 8px; padding:0; }
    .ponddepth-pop li { margin: 4px 0; }
    .ponddepth-skill { display:flex; align-items:flex-start; gap:5px; }

    /* Two-line clamp for the skill description */
    .ponddepth-skill > span { flex: 1 1 auto; min-width: 0; }
    .ponddepth-skill-why {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: normal;
    }

    /* Fix tag height to match two lines of text */
    .ponddepth-tag {
      font-size: 11px;
      padding: 0;
      border-radius: 999px;
      box-sizing: border-box;
      border: 1px solid rgba(255,255,255,0.18);
      color: rgba(232,238,252,0.78);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      height: 22px;
      width: ${LOCALE === "zh" ? "44px" : "62px"};
      min-width: ${LOCALE === "zh" ? "44px" : "62px"};
      max-width: ${LOCALE === "zh" ? "44px" : "62px"};
      white-space: nowrap;
      flex: 0 0 auto;
      margin-top: 1px;
    }
    button.ponddepth-tag { appearance: none; -webkit-appearance: none; background: rgba(255,255,255,0.06); cursor: pointer; }
    button.ponddepth-tag:hover { background: rgba(255,255,255,0.10); }
    .ponddepth-tag.ok { border-color: rgba(52,211,153,0.45); color: rgba(52,211,153,0.95); }
    .ponddepth-tag.warn { border-color: rgba(251,191,36,0.45); color: rgba(251,191,36,0.95); }
    .ponddepth-pop a { color: rgba(110,231,255,0.95); text-decoration: none; }
    .ponddepth-pop a:hover { text-decoration: underline; }
  `;
  document.head.appendChild(style);
}

function buildBadge() {
  ensureStyle();
  pill = document.createElement("div");
  pill.className = "pill ponddepth";
  pill.title = t("PondDepth（悬停查看详情，点击修改等级）", "PondDepth (hover for details, click to set level)");

  const dot = document.createElement("span");
  dot.className = "statusDot ok";

  label = document.createElement("span");
  mono = document.createElement("span");
  mono.className = "mono";

  iconImg = document.createElement("img");
  iconImg.className = "ponddepth-pill-icon";
  iconImg.alt = "🦞";
  iconImg.src = iconUrlForLevel(getLevelId());

  pill.appendChild(dot);
  pill.appendChild(iconImg);
  pill.appendChild(label);
  pill.appendChild(mono);

  pill.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    const cur = getLevelId();
    const next = prompt(t("设置 PondDepth 等级（B1~B5/F1~F5/S1~S5）", "Set PondDepth level (B1~B5 / F1~F5 / S1~S5)"), cur);
    if (next) setLevelId(next);
  });

  pill.addEventListener("mouseenter", () => showPopover());
  pill.addEventListener("mouseleave", () => scheduleHide());
}

function levelIndex(id) {
  const keys = Object.keys(LEVELS);
  const idx = keys.indexOf(id);
  return idx >= 0 ? idx : 0;
}

let hideTimer = null;
function scheduleHide() {
  if (hideTimer) clearTimeout(hideTimer);
  hideTimer = setTimeout(() => {
    if (pop) pop.style.display = "none";
  }, 180);
}

function cancelHide() {
  if (hideTimer) clearTimeout(hideTimer);
  hideTimer = null;
}

async function showPopover() {
  // debug hook
  try { window.__ponddepth_showPopover = showPopover; } catch {}

  cancelHide();
  if (!pop) {
    pop = document.createElement("div");
    pop.className = "ponddepth-pop";
    pop.style.display = "none";
    pop.addEventListener("mouseenter", () => cancelHide());
    pop.addEventListener("mouseleave", () => scheduleHide());
    document.body.appendChild(pop);
  }

  // Position near badge
  const r = pill.getBoundingClientRect();
  const left = clamp(Math.round(r.left), 12, window.innerWidth - 380);
  const top = Math.round(r.bottom + 10);
  pop.style.left = left + "px";
  pop.style.top = top + "px";

  // Load skills status snapshot
  const status = await loadSkillsStatus();
  await loadSkillsZhMap();
  const smap = status ? skillMapFromStatus(status) : new Map();
  const readyCount = Array.from(smap.values()).filter((s) => s && s.ready).length;
  const totalCount = status && Array.isArray(status.skills) ? status.skills.length : Array.from(smap.values()).length;

  const lvlId = getLevelId();
  const idx = levelIndex(lvlId);

  // Load latest metrics for auto level/progress
  const metrics = await loadPondDepthMetrics();
  const autoLevel = metrics && typeof metrics.level === "string" ? String(metrics.level).toUpperCase() : null;
  const autoPct = metrics && typeof metrics.levelProgressPct === "number" ? Math.round(metrics.levelProgressPct) : null;
  const lvlIdFinal = autoLevel || lvlId;
  const lvl = LEVELS[lvlIdFinal] || LEVELS.B1;
  const pct = autoPct != null ? clamp(autoPct, 0, 100) : Math.round(((idx + 1) / Object.keys(LEVELS).length) * 100);

  const xpVal = metrics && typeof metrics.xp === "number" ? metrics.xp : null;
  const xpStr = xpVal != null ? String(Math.round(xpVal * 100) / 100) : "—";
  const B_THRESH = [
    ["B1", 0, 80],
    ["B2", 80, 160],
    ["B3", 160, 260],
    ["B4", 260, 380],
    ["B5", 380, null],
  ];
  const levelsListHtml = B_THRESH.map(([id, lo, hi]) => {
    const it = LEVELS[id] || {};
    const name = cleanTitle(t(it.titleZh || id, it.titleEn || id));
    const range = hi == null ? `XP ≥ ${lo}` : `XP ${lo}–${hi}`;
    const cls = id === lvlIdFinal ? "it cur" : "it";
    return `<div class="${cls}"><div class="row2"><div><b>${id}</b>｜${name}</div><div class="muted" style="font-weight:700;">${range}</div></div></div>`;
  }).join("");

  const companionDays = await loadCompanionDayCount();

  const skillsPoolAllRaw = ([]
    .concat(RECOMMENDED_SKILLS)
    .concat(DISCOVERY_SKILLS.map((n) => (typeof n === "string" ? { name: n, why: "" } : n))))
    .map((x) => {
      if (!x) return null;
      if (typeof x === "string") return { name: x, why: "" };
      const rawWhy = x.description || x.why || t(x.whyZh || "", x.whyEn || "");
      const why = localizeSkillWhy(x.name, rawWhy);
      return { name: x.name, why };
    })
    .filter((x) => x && x.name);

  // Dedup + prioritize NOT installed skills
  const seenSkill = new Set();
  const dedup = [];
  for (const s of skillsPoolAllRaw) {
    const k = String(s.name || "").trim();
    if (!k || seenSkill.has(k)) continue;
    seenSkill.add(k);
    dedup.push(s);
  }
  const skillsPoolAll = dedup;
  const getSt = (n) => smap.get(n) || smap.get(normSkillKey(n)) || smap.get(resolveSkillKey(n));
  const notInstalledFirst = skillsPoolAll.filter((s) => !getSt(s.name)).concat(skillsPoolAll.filter((s) => !!getSt(s.name)));

  const skillsPageSize = 5;
  let skillsPage = 0;
  try { skillsPage = Math.max(0, parseInt(localStorage.getItem('ponddepth.skills.page') || '0', 10) || 0); } catch {}
  const skillsTotalPages = Math.max(1, Math.ceil(notInstalledFirst.length / skillsPageSize));
  skillsPage = skillsPage % skillsTotalPages;
  const skillsStart = skillsPage * skillsPageSize;
  const skillsPool = notInstalledFirst.slice(skillsStart, skillsStart + skillsPageSize);

  const skillsHtml = skillsPool.map((s) => {
    const st = smap.get(s.name) || smap.get(normSkillKey(s.name)) || smap.get(resolveSkillKey(s.name));
    const installed = !!st;
    const ready = installed && st.ready;
    const tag = !installed
      ? `<button class="ponddepth-tag ponddepth-skill-action warn" data-action="install" data-skill="${s.name}">${t("安装", "Install")}</button>`
      : ready
      ? `<span class="ponddepth-tag ok">${t("生效中", "Active")}</span>`
      : `<button class="ponddepth-tag ponddepth-skill-action warn" data-action="enable" data-skill="${s.name}">${t("启用", "Enable")}</button>`;
    const why = (s.why || "").trim();
    return `<li class="ponddepth-skill">${tag}<span><b>${s.name}</b>${why ? ` <span class="muted ponddepth-skill-why">— ${why}</span>` : ``}</span></li>`;
  }).join("");

  const newsItemsAll = (await loadOpenClawNews()) || NEWS;
  const pageSize = 5;
  let page = 0;
  try { page = Math.max(0, parseInt(localStorage.getItem('ponddepth.news.page') || '0', 10) || 0); } catch {}
  const totalPages = Math.max(1, Math.ceil(newsItemsAll.length / pageSize));
  page = page % totalPages;
  const start = page * pageSize;
  const newsItems = newsItemsAll.slice(start, start + pageSize);

  const newsHtml = newsItems.map((n) => `<li><a href="${n.url}" target="_blank" rel="noreferrer">${n.title}</a></li>`).join("");

  pop.innerHTML = `
    <h4 style="font-size:13px; font-weight:800; margin:0;">${t("陪伴第", "Day")} <b>${companionDays}</b> ${t("天", "")}</h4>

    <div class="row" style="margin-top:8px; align-items:center;">
      <div class="ponddepth-level-cur"><img class="ponddepth-level-icon" src="${iconUrlForLevel(lvlIdFinal)}" alt="🦞"/>${lvlIdFinal}｜${cleanTitle(t(lvl.titleZh, lvl.titleEn))}<span class="ponddepth-help" title="${t("查看所有等级","View all levels")}">?</span></div>
      <div class="muted" style="font-weight:700;">${pct}%</div>
    </div>
    <div class="ponddepth-levels-panel">
      <div class="muted" style="font-weight:700; margin-bottom:6px;">${t("当前 XP：","Current XP: ")}${xpStr}<span class="muted" style="font-weight:500; opacity:0.75; margin-left:6px;">${t("（陪伴天数/消息互动/skills 安装都会加 XP）","(Days, messages, and installed skills all add XP)")}</span></div>
      ${levelsListHtml}
    </div>
    <div class="bar" style="margin-top:8px"><div style="width:${pct}%"></div></div>

    <div style="height:10px"></div>
    <div class="ponddepth-tip">💡 ${await loadOpenClawTip() || t("今日一句暂未生成","Today’s tip is not ready yet")}</div>

    <div style="height:10px"></div>

    <div style="height:10px"></div>
    <h4 style="font-size:13px; font-weight:800;">${t("Skills 推荐", "Recommended Skills")}<button class="ponddepth-refresh-btn ponddepth-skills-refresh" type="button" title="${t("换一批", "Refresh")}">${t("刷新", "Refresh")}</button></h4>
    ${status ? `<div class="muted">${t("启用", "Enabled")} ${readyCount} / ${t("总计", "Total")} ${totalCount}（${status && status.__ponddepthSource === "rpc" ? t("实时","Live") : t("快照","Snapshot")}）</div>` : `<div class="muted">（暂未读取到 skills 快照，稍后再试）</div>`}
    <ul>${skillsHtml}</ul>

    <div style="height:12px"></div>
    <h4 style="font-size:13px; font-weight:800;">${t("OpenClaw 资讯", "OpenClaw News")}<button class="ponddepth-refresh-btn" type="button" title="${t("换一批", "Refresh")}">${t("刷新", "Refresh")}</button></h4>
    <ul>${newsHtml}</ul>
  `;

  // bind refresh button (rotate next 5 items)
  try {
    const btn = pop.querySelector(".ponddepth-refresh-btn:not(.ponddepth-skills-refresh)");
    if (btn) {
      btn.onclick = (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        try {
          const cur = parseInt(localStorage.getItem("ponddepth.news.page") || "0", 10) || 0;
          localStorage.setItem("ponddepth.news.page", String(cur + 1));
        } catch {}
        showPopover();
      };
    }
    const btn2 = pop.querySelector(".ponddepth-skills-refresh");
    if (btn2) {
      btn2.onclick = (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        try {
          const cur = parseInt(localStorage.getItem("ponddepth.skills.page") || "0", 10) || 0;
          localStorage.setItem("ponddepth.skills.page", String(cur + 1));
        } catch {}
        showPopover();
      };
    }

    // skill action buttons (install)
    const actionBtns = pop.querySelectorAll?.(".ponddepth-skill-action") || [];
    for (const b of actionBtns) {
      b.onclick = async (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        const name = b.getAttribute("data-skill") || "";
        const action = b.getAttribute("data-action") || "";
        if (!name || !action) return;
        const prev = b.textContent;
        b.textContent = action === "enable" ? t("启用中", "Enabling") : t("安装中", "Installing");
        b.disabled = true;
        try {
          const app = getOpenClawApp && getOpenClawApp();
          const client = app && app.client ? app.client : null;
          if (!client) throw new Error("no rpc client");

          if (action === "install") {
            // B2 UX: if user hasn't authorized ClawHub, guide them to login first.
            const st = await loadClawhubStatus();
            if (st && st.loggedIn === false) {
              try {
                await navigator.clipboard.writeText(`clawhub login`);
                alert(t("未授权 ClawHub：已复制 \"clawhub login\"，先授权再装。", "ClawHub not authorized: copied \"clawhub login\". Authorize first."));
              } catch {}
              return;
            }

            // Default (safe) install behavior: copy the recommended command.
            try {
              await navigator.clipboard.writeText(`clawhub install ${name}`);
              alert(t("已复制安装命令：", "Copied install command: ") + `clawhub install ${name}`);
            } catch {}
            return;
          } else if (action === "enable") {
            await client.request("skills.update", { skillKey: name, enabled: true });
            try {
              alert(t("已提交启用，请稍等片刻后刷新。", "Enable submitted. Refresh in a moment."));
            } catch {}
          }
        } catch (e) {
          console.warn("skill action failed", action, name, e);
          try {
            await navigator.clipboard.writeText(`clawhub install ${name}`);
            alert(t("安装失败，已复制命令：", "Failed. Copied command: ") + `clawhub install ${name}`);
          } catch {}
        } finally {
          b.disabled = false;
          b.textContent = prev;
          showPopover();
        }
      };
    }

    // levels help panel
    const help = pop.querySelector(".ponddepth-help");
    const panel = pop.querySelector(".ponddepth-levels-panel");
    if (help && panel) {
      let hideT = null;
      const show = () => {
        try { if (hideT) clearTimeout(hideT); } catch {}
        panel.style.display = "block";
      };
      const hide = () => {
        try { if (hideT) clearTimeout(hideT); } catch {}
        hideT = setTimeout(() => { panel.style.display = "none"; }, 120);
      };
      help.addEventListener("mouseenter", show);
      help.addEventListener("mouseleave", hide);
      panel.addEventListener("mouseenter", show);
      panel.addEventListener("mouseleave", hide);
    }
  } catch {}

  pop.style.display = "block";
}

function renderBadge() {
  if (!pill) return;
  const id = getLevelId();
  const lvl = LEVELS[id] || LEVELS.B1;
  label.textContent = `${id}`;
  try { if (iconImg) iconImg.src = iconUrlForLevel(id); } catch {}
  mono.textContent = cleanTitle(t(lvl.titleZh, lvl.titleEn));
}

function mount() {
  const host = findTopbarLeft();
  if (!host) return false;
  if (!pill) buildBadge();
  renderBadge();

  // Ensure ordering inside .topbar-left: collapse toggle, PondDepth badge, brand
  const collapse = host.querySelector?.(".nav-collapse-toggle") || null;
  if (!host.contains(pill)) {
    // First mount
    if (collapse && collapse.parentNode === host && collapse.nextSibling) {
      host.insertBefore(pill, collapse.nextSibling);
    } else if (collapse && collapse.parentNode === host) {
      host.appendChild(pill);
    } else {
      host.prepend(pill);
    }
  } else if (collapse && collapse.parentNode === host) {
    // Reorder if needed (e.g., collapse button mounted after our first insert)
    const shouldBeAfterCollapse = pill.previousSibling !== collapse;
    if (shouldBeAfterCollapse) {
      // Detach + insert after collapse
      pill.remove();
      if (collapse.nextSibling) {
        host.insertBefore(pill, collapse.nextSibling);
      } else {
        host.appendChild(pill);
      }
    }
  }

  return true;
}

// initial mount
const t0 = Date.now();
const timer = setInterval(() => {
  const ok = mount();
  if (ok || Date.now() - t0 > 15000) clearInterval(timer);
}, 300);

window.addEventListener("storage", (e) => {
  if (e.key === "ponddepth.level") {
    mount();
  }
});

// debug: expose popover for evaluation
try {
  window.__ponddepth_showPopover = showPopover;
} catch {
}
