
/* Cron Tab — Cron Jobs, Run History, Cost Analysis */
var escHtml = window.escHtml || function(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\"/g, '&quot;')
    .replace(/'/g, '&#39;');
};

// Cron Jobs list removed — data shown in cost table instead
async function loadCronEnhanced() {
  // No-op: cron jobs are displayed in loadCronCosts() table
}

// ─── Ops Channel Usage Panel ───
const MODEL_COLORS = {};

// Normalize model string: lowercase + dots and hyphens unified → '-'
// Allows "claude-opus-4-6" to match key "opus-4.6", and "Qwen3.5-35B" to match "qwen3-5-35b"
function normModelStr(s) { return (s || '').toLowerCase().replace(/[.\-]/g, '-'); }

function _hashColor(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = ((h << 5) - h) + str.charCodeAt(i);
  const hue = Math.abs(h) % 360;
  return `hsl(${hue} 72% 58%)`;
}

function getModelColor(model) {
  const mNorm = normModelStr(model);
  const key = Object.keys(MODEL_COLORS).find(k => mNorm.includes(normModelStr(k)));
  if (key) return MODEL_COLORS[key];
  if (!mNorm) return '#6b7280';
  return _hashColor(mNorm);
}

function shortModel(m) {
  const raw = (m || '').replace(/-preview$/, '');
  if (!raw || raw === 'unknown') return 'unknown';
  const rawNorm = normModelStr(raw);
  const pair = MODEL_DISPLAY_NAMES.find(([pattern]) => rawNorm.includes(normModelStr(pattern)));
  return pair ? pair[1] : raw.replace(/^[^/]+\//, '').replace(/[-_]/g, ' ').replace(/\.gguf$/i, '').trim();
}

function fmtTokens(n) {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
  if (n >= 1_000) return (n / 1_000).toFixed(0) + 'k';
  return String(n);
}

function fmtUsd(n, digits = 2) {
  return '$' + (Number(n || 0)).toFixed(digits);
}


async function loadCronRuns() {
  const body = document.getElementById('cronRunsBody');
  const count = document.getElementById('cronRunsCount');
  if (!body) return;

  try {
    const data = await apiFetch('/cron/today');
    const runs = data.todayJobs || [];
    count.textContent = runs.length;

    if (runs.length === 0) {
      body.innerHTML = `<div style="padding:12px 18px;font-size:.8rem;color:var(--text2)">${tt('No Cron runs today', '今日暂无 Cron 执行记录')}</div>`;
      return;
    }

    // Sort by last run time descending (timeline newest first)
    runs.sort((a, b) => {
      const ta = Date.parse(a?.last?.endedAt || a?.last?.startedAt || '');
      const tb = Date.parse(b?.last?.endedAt || b?.last?.startedAt || '');
      return (Number.isFinite(tb) ? tb : 0) - (Number.isFinite(ta) ? ta : 0);
    });

    body.innerHTML = runs.map(r => {
      const last = r.last || {};
      const name = r.name || r.id?.slice(0, 8) || '—';
      const status = last.status === 'ok' ? '✅' : last.status === 'error' ? '❌' : '⏳';
      const time = last.endedAt ? new Date(last.endedAt).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'America/Los_Angeles' }) : (last.startedAt ? new Date(last.startedAt).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'America/Los_Angeles' }) : '—');
      const startMs = Date.parse(last.startedAt || '');
      const endMs = Date.parse(last.endedAt || '');
      const dur = (Number.isFinite(startMs) && Number.isFinite(endMs) && endMs >= startMs)
        ? ((endMs - startMs) / 1000).toFixed(1) + 's'
        : (Number.isFinite(Number(last.durationMs)) ? (Number(last.durationMs) / 1000).toFixed(1) + 's' : '');
      const modelRaw = last.model || r.model || '';
      const model = modelRaw ? shortModel(modelRaw) : '';
      const isLocalModel = /local-|qwen|gguf|local-dgx-spark/i.test(String(modelRaw));
      const tokens = (isLocalModel && Number.isFinite(Number(last.tokens))) ? (fmtTokens(Number(last.tokens)) + ' tok') : '';
      const cost = Number.isFinite(last.costUsd) ? fmtUsd(last.costUsd, 3) : '';
      const detail = [model, tokens, cost, dur].filter(Boolean).join(' · ');

      return `<div class="agent-session-row">
        <span style="font-size:.9rem">${status}</span>
        <span class="agent-session-key" style="flex:1;font-family:inherit;font-size:.78rem">${escHtml(name)}</span>
        <span class="agent-session-tokens">${escHtml(detail)}</span>
        <span class="agent-session-age">${time}</span>
      </div>`;
    }).join('');
  } catch (e) {
    body.innerHTML = `<div style="padding:12px 18px;font-size:.8rem;color:var(--text2)">${escHtml(e.message)}</div>`;
  }
}

function formatAge(minutes) {
  if (minutes < 1) return 'just now';
  if (minutes < 60) return `${minutes}m ago`;
  if (minutes < 1440) return `${Math.floor(minutes / 60)}h ago`;
  return `${Math.floor(minutes / 1440)}d ago`;
}

function toggleSessionsPanel() {
  // Panel toggle handled by CSS via collapsed class
}

function spawnSingleTask(_taskId) {
  // Dashboard is read-only. Spawn tasks via Discord or CLI.
  toast('Dashboard is read-only. Use Discord or CLI to spawn tasks.', 'info');
}

// ─── Sessions Panel ───
// ─── Model names (single source of truth for display) ───
const MODEL_DISPLAY_NAMES = [
  // [match-pattern (normModelStr applied), display name]
  // Anthropic
  ['opus-4-6',            'Claude Opus 4.6'],
  ['sonnet-4-6',          'Claude Sonnet 4.6'],
  ['haiku-4-5',           'Claude Haiku 4.5'],
  ['haiku-3-5',           'Claude Haiku 3.5'],
  // Google
  ['gemini-3-flash',      'Gemini 3 Flash'],
  ['gemini-3-1-pro',      'Gemini 3.1 Pro'],
  ['gemini-3-1-flash',    'Gemini 3.1 Flash Lite'],
  ['gemini-2-5-pro',      'Gemini 2.5 Pro'],
  ['gemini-2-5-flash',    'Gemini 2.5 Flash'],
  // OpenAI
  ['gpt-5-4',             'GPT-5.4'],
  ['gpt-5-3-codex',       'GPT-5.3 Codex'],
  ['gpt-5-3-instant',     'GPT-5.3 Instant'],
  ['gpt-5-3-chat',        'GPT-5.3 Chat'],
  ['gpt-5-2',             'GPT-5.2'],
  ['gpt-5-1',             'GPT-5.1'],
  ['gpt-5',               'GPT-5'],
  ['gpt-5-mini',          'GPT-5 Mini'],
  ['gpt-5-nano',          'GPT-5 Nano'],
  // Moonshot
  ['kimi-k2',             'Kimi-K2.5'],
  // Volcengine
  ['doubao',              'Doubao Seed'],
  // Qwen models - unified naming
  ['qwen3-5-27b-claude',  'Qwen-27B'],
  ['qwen3-5-27b',         'Qwen-27B'],
  ['qwen3-5-35b',         'Qwen-35B'],
  ['qwen-mac',            'Qwen-MacBook'],
  ['qwen-spark-35b',      'Qwen-35B'],
  ['qwen-spark-27b',      'Qwen-27B'],
  ['local-dgx-spark-qwen-35b', 'Qwen-35B'],
  ['local-dgx-spark-qwen-27b', 'Qwen-27B'],
  ['local-macbook-pro-qwen',   'Qwen-MacBook'],
];

// ─── Model Selector ───
let globalDefaultModel = 'claude-sonnet-4-6'; // updated dynamically from /ops/system

// Starts with hardcoded defaults; refreshed from /ops/models on load.
// To update model names/ids: edit models-registry.json on the server — no code change needed.
let MODEL_OPTIONS = [
  { value: 'default', label: '', full: null, isDefault: true },
  { value: 'opus',   label: 'Claude Opus 4',   full: 'claude-opus-4-6' },
  { value: 'sonnet', label: 'Claude Sonnet 4', full: 'claude-sonnet-4-6' },
  { value: 'flash',  label: 'Gemini 3 Flash',  full: 'gemini-3-flash-preview' },
  { value: 'pro',    label: 'Gemini 3 Pro',     full: 'gemini-3-pro-preview' },
  { value: 'codex',  label: 'GPT-5.3 Codex',   full: 'gpt-5.3-codex' },
];


function refreshModelOptions(registry) {
  if (!registry || typeof registry !== 'object') return;
  const opts = [{ value: 'default', label: '', full: null, isDefault: true }];
  for (const [alias, entry] of Object.entries(registry)) {
    const id = typeof entry === 'string' ? entry : entry?.id;
    const label = (typeof entry === 'object' && entry?.label) ? entry.label : alias;
    if (id) opts.push({ value: alias, label, full: id.includes('/') ? id.split('/').pop() : id });
  }
  MODEL_OPTIONS = opts;
}

function getDefaultModelLabel() {
  // Show actual model name instead of "默认"
  const m = globalDefaultModel || '';
  return shortModel(m) + ' ★';
}

function buildModelSelect(currentModel, id, type) {
  // type: 'session' (channelId) or 'cron' (jobId)
  const opts = MODEL_OPTIONS.map(o => {
    let label = o.isDefault ? getDefaultModelLabel() : o.label;
    const isCurrent = o.full ? currentModel.includes(o.full) : (!currentModel || currentModel === 'unknown');
    return `<option value="${o.value}" ${isCurrent ? 'selected' : ''}>${label}</option>`;
  }).join('');
  const color = getModelColor(currentModel);
  return `<select class="model-select" style="border-color:${color};color:${color}"
    ${DASHBOARD_CAPS.mutatingOpsEnabled ? '' : 'disabled title="Model changes are available in OpenClaw Control UI or CLI"'}
    onchange="changeModel('${type}','${id}',this.value,this)">${opts}</select>`;
}

function changeModel(_type, _id, _model, el) {
  // Dashboard is read-only. Change models via Discord (/status) or CLI.
  if (el) { el.disabled = false; el.style.opacity = '1'; }
  toast('Dashboard is read-only. Change models via Discord or CLI.', 'info');
}

const SESSION_SORT_DEFAULT_DIR = {
  model: 'asc',
  messages: 'desc',
  tokens: 'desc',
  cost: 'desc',
  costPerMsg: 'desc',
  fit: 'desc',
};

const sessionSortState = {
  key: null,
  dir: 'desc',
};

function toggleSessionSort(key) {
  if (sessionSortState.key === key) {
    sessionSortState.dir = sessionSortState.dir === 'asc' ? 'desc' : 'asc';
  } else {
    sessionSortState.key = key;
    sessionSortState.dir = SESSION_SORT_DEFAULT_DIR[key] || 'desc';
  }
  loadSessions();
}

function sessionSortIndicator(key) {
  if (sessionSortState.key !== key) return '&harr;';
  return sessionSortState.dir === 'asc' ? '&uarr;' : '&darr;';
}

function normalizeTaskTag(tag) {
  if (!tag) return '';
  if (isZh()) return tag;
  const map = {
    '🔧 深度开发': '🔧 Deep build',
    '🧠 架构讨论': '🧠 Architecture',
    '📊 汇报转发': '📊 Reporting',
    '💬 闲聊': '💬 Chat',
    '🔍 监控播报': '🔍 Monitoring',
    '💼 搜索整理': '💼 Job research',
    '🐦 内容创作': '🐦 Content',
    '📰 摘要生成': '📰 Summary',
    '📝 内容摘要': '📝 Summary',
    '👁️ 图片路由': '👁️ Image routing',
    '🎯 活动搜索': '🎯 Event search',
    '📅 规划': '📅 Planning',
    '👤 信息录入': '👤 Data entry',
    '🍷 品鉴记录': '🍷 Tasting log',
    '🚬 品鉴记录': '🚬 Tasting log',
    '🍵 品鉴记录': '🍵 Tasting log',
    '🌱 记录': '🌱 Logging',
    '📖 灵修提醒': '📖 Reflection reminder',
  };
  return map[tag] || tag.replace(/[\u4E00-\u9FFF]/g, '').replace(/\s+/g, ' ').trim();
}

let _sessionsHideStale = false; // global toggle: hide sessions with no activity for 7+ days
let _sessionsHideInactive = false; // global toggle: hide sessions with no activity today


async function loadCronCosts() {
  const summaryEl = document.getElementById('cronCostSummary');
  const contentEl = document.getElementById('cronCostContent');
  const canvas = document.getElementById('cronTrendChart');
  const legendEl = document.getElementById('cronTrendLegend');
  if (!contentEl) return;

  try {
    const [summaryData, trendData, dailyData] = await Promise.all([
      apiFetch('/dashboard/usage/cron/summary?days=7'),
      apiFetch('/dashboard/usage/cron/trend?days=7'),
      apiFetch('/dashboard/usage/cron/daily?days=7'),
    ]);

    const s = summaryData.summary || {};
    const jobs = summaryData.jobs || summaryData.rows || [];
    const trendRows = trendData.dailyTrend || trendData.rows || [];
    const dailyRows = dailyData.rows || [];
    const totalRuns = Number(s.totalRuns || s.calls || 0);
    const totalCronCost = Number(s.totalCronCost || s.costUsd || 0);
    const totalCronTokens = Number(s.totalCronTokens || s.totalTokens || 0);
    const todayKey = new Date().toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' });
    const todayRows = dailyRows.filter(r => (r.day || r.date) === todayKey);
    const todayCost = todayRows.reduce((sum, r) => sum + Number(r.costUsd || 0), 0);
    const todayTokens = todayRows.reduce((sum, r) => sum + Number(r.totalTokens || 0), 0);

    summaryEl.textContent = tt(
      `${totalRuns} calls · total cron ${fmtUsd(totalCronCost, 2)} (${fmtTokens(totalCronTokens)} tokens) · today ${fmtUsd(todayCost, 2)} (${fmtTokens(todayTokens)} tokens) · 7 days`,
      `累计 ${totalRuns} 次调用 · 总 cron 成本 ${fmtUsd(totalCronCost, 2)}（${fmtTokens(totalCronTokens)} tokens） · 今日 ${fmtUsd(todayCost, 2)}（${fmtTokens(todayTokens)}） · 7 天`
    );

    const modelAgg = new Map();
    for (const j of jobs) {
      const key = `${j.provider || 'unknown'}|${j.model || 'unknown'}`;
      const prev = modelAgg.get(key) || { model: j.model, runs: 0, totalTokens: 0, jobs: [] };
      prev.runs += Number(j.calls || 0);
      prev.totalTokens += Number(j.totalTokens || 0);
      prev.jobs.push({ name: j.jobName || j.cronJobId || 'unknown', runs: Number(j.calls || 0) });
      modelAgg.set(key, prev);
    }
    const modelStats = Array.from(modelAgg.values()).sort((a, b) => b.totalTokens - a.totalTokens);

    let modelStatsHtml = '';
    if (modelStats.length > 0) {
      modelStatsHtml = `<div class="glass-card" style="padding:10px;margin-bottom:10px">
        <div style="font-size:.8rem;font-weight:600;margin-bottom:6px">📊 ${tt('Cost by Model', '按模型聚合成本')}</div>
        <table class="sessions-table">
          <thead>
            <tr>
              <th>${tt('Model', '模型')}</th>
              <th>${tt('Total Runs', '总次数')}</th>
              <th>Tokens/${tt('run', '次')}</th>
              <th>${tt('Total Tokens', '总 Tokens')}</th>
              <th>${tt('Jobs', '任务数')}</th>
            </tr>
          </thead>
          <tbody>`;
      for (const m of modelStats) {
        modelStatsHtml += `<tr>
          <td style="font-weight:600;font-size:.78rem">
            <span class="sess-model" style="border-color:${getModelColor(m.model)};color:${getModelColor(m.model)}">${shortModel(m.model)}</span>
          </td>
          <td>${m.runs}</td>
          <td>${fmtTokens(m.runs > 0 ? Math.round(m.totalTokens / m.runs) : 0)}</td>
          <td style="font-weight:600">${fmtTokens(m.totalTokens)}</td>
          <td style="font-size:.72rem;color:var(--text2)">${m.jobs.slice(0,5).map(j => `<div>${escHtml(j.name)} (${j.runs}x)</div>`).join('')}${m.jobs.length > 5 ? `<div style="color:var(--text3)">+${m.jobs.length - 5} more</div>` : ''}</td>
        </tr>`;
      }
      modelStatsHtml += '</tbody></table></div>';
    }

    const todayMap = new Map();
    for (const r of dailyRows) {
      if ((r.day || r.date) !== todayKey) continue;
      const key = `${r.cronJobId || 'unknown'}|${r.provider || 'unknown'}|${r.model || 'unknown'}`;
      todayMap.set(key, {
        totalTokens: Number(r.totalTokens || 0),
        costUsd: Number(r.costUsd || 0),
        calls: Number(r.calls || 0),
      });
    }

    let html = modelStatsHtml;
    html += `<table class="sessions-table"><thead><tr><th>${tt('Cron job', 'Cron 任务')}</th><th>${tt('Runs', '总次数')}</th><th>${tt('Active days', '活跃天数')}</th><th>Tokens/${tt('run', '次')}</th><th>$/ ${tt('run', '次')}</th><th>${tt('Today (tokens / $)', '今日（tokens / $）')}</th><th>${tt('Total tokens', '总 Tokens')}</th><th>${tt('Total cost', '总花费')}</th></tr></thead><tbody>`;
    for (const j of jobs) {
      const tokensPerRun = Number(j.calls || 0) > 0 ? Number(j.totalTokens || 0) / Number(j.calls || 0) : 0;
      const costPerRun = Number(j.calls || 0) > 0 ? Number(j.costUsd || 0) / Number(j.calls || 0) : 0;
      const today = todayMap.get(`${j.cronJobId || 'unknown'}|${j.provider || 'unknown'}|${j.model || 'unknown'}`) || { totalTokens: 0, costUsd: 0, calls: 0 };
      html += `<tr>
        <td style="font-weight:600;font-size:.78rem">
          ${escHtml(j.jobName || j.cronJobId || 'unknown')}
          <div style="margin-top:4px"><span class="sess-model" style="border-color:${getModelColor(j.model)};color:${getModelColor(j.model)}">${shortModel(j.model)}</span></div>
        </td>
        <td>${j.calls}</td>
        <td>${j.activeDays || '—'}</td>
        <td>${fmtTokens(tokensPerRun)}</td>
        <td style="color:${costPerRun > 0.2 ? '#fbbf24' : 'var(--green)'}">${fmtUsd(costPerRun, 3)}</td>
        <td>${fmtTokens(today.totalTokens)} / ${fmtUsd(today.costUsd, 2)}</td>
        <td style="font-weight:600">${fmtTokens(j.totalTokens || 0)}</td>
        <td style="font-weight:600">${fmtUsd(j.costUsd || 0, 2)}</td>
      </tr>`;
    }
    html += '</tbody></table>';
    contentEl.innerHTML = html;

    const trend = [...trendRows].map(r => ({ date: r.day || r.date, cronCost: Number(r.cronCost ?? r.costUsd ?? 0), cronTokens: Number(r.cronTokens ?? r.totalTokens ?? 0) })).filter(r => r.date).sort((a, b) => a.date < b.date ? -1 : 1);
    if (canvas && trend.length > 1) {
      const ctx = canvas.getContext('2d');
      const W = canvas.parentElement.clientWidth - 32;
      const H = 160;
      canvas.width = W * 2; canvas.height = H * 2;
      canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
      ctx.scale(2, 2);
      const maxCost = Math.max(...trend.map(d => d.cronCost), 1);
      const barW = Math.min(40, (W - 40) / trend.length - 4);
      const startX = 36;
      const chartH = H - 30;
      const theme = getChartThemeColors();
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = theme.muted; ctx.font = '10px sans-serif'; ctx.textAlign = 'right';
      for (let i = 0; i <= 4; i++) {
        const y = 10 + chartH - (i / 4) * chartH;
        ctx.fillText('$' + (maxCost * i / 4).toFixed(0), 30, y + 3);
        ctx.strokeStyle = theme.border; ctx.beginPath(); ctx.moveTo(startX, y); ctx.lineTo(W, y); ctx.stroke();
      }
      trend.forEach((d, i) => {
        const x = startX + i * ((W - startX) / trend.length) + 2;
        const h = ((d.cronCost || 0) / maxCost) * chartH;
        const baseY = 10 + chartH;
        ctx.fillStyle = theme.green;
        ctx.fillRect(x, baseY - h, barW, h);
        ctx.fillStyle = theme.muted; ctx.font = '9px sans-serif'; ctx.textAlign = 'center';
        ctx.fillText(d.date.slice(5), x + barW / 2, baseY + 12);
        ctx.fillStyle = theme.text; ctx.font = 'bold 9px sans-serif';
        ctx.fillText('$' + d.cronCost.toFixed(2), x + barW / 2, baseY - h - 3);
      });
      if (legendEl) legendEl.innerHTML = `<span style="color:var(--green)">■ ${tt('Cron daily cost', 'Cron 每日成本')}</span><span style="color:var(--text2)">${tt('7-day usage trend', '7 天趋势')}</span>`;
    } else if (legendEl) {
      legendEl.textContent = tt('Not enough trend data (need at least 2 days)', '趋势数据不足（至少需要 2 天）');
    }
  } catch (e) {
    contentEl.innerHTML = `<p>${escHtml(e.message)}</p>`;
  }
}
