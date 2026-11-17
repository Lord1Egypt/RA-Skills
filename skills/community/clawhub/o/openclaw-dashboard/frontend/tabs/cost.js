
/* Cost Tab — All-Time Usage, Provider Audit, Usage by Source */
var escHtml = window.escHtml || function(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\"/g, '&quot;')
    .replace(/'/g, '&#39;');
};

// ─── Unified Analytics State ──────────────────────────────────────────
window.ANALYTICS_STATE = window.ANALYTICS_STATE || {
  rangeDays: 7,
  windowOffset: 0,
  selectedDay: null,
  expandedDay: null,
  windowModels: [],
  allDaily: [],
  sourceDaily: [],
};

function canonicalModelProvider(provider, model) {
  const p = String(provider || '').toLowerCase();
  const m = String(model || '').toLowerCase();
  if (p.includes('openai')) return 'openai';
  if (p.includes('anthropic')) return 'anthropic';
  if (p.includes('google')) return 'google';
  if (p.includes('moonshot') || m.includes('kimi')) return 'moonshot';
  if (p.includes('qwen') || p.includes('local') || p.includes('ollama') || m.includes('qwen') || m.includes('gguf')) return 'local-qwen';
  if (p.includes('openrouter')) return 'openrouter';
  return 'other';
}

function getProviderBaseColor(providerKey) {
  return {
    openai: '#f97316',
    anthropic: '#a855f7',
    google: '#22c55e',
    moonshot: '#06b6d4',
    'local-qwen': '#6366f1',
    openrouter: '#64748b',
    other: '#94a3b8',
  }[providerKey] || '#94a3b8';
}

function getModelVisual(model, provider) {
  const providerKey = canonicalModelProvider(provider, model);
  const color = getModelColor(model || providerKey || 'unknown');
  const providerColor = getProviderBaseColor(providerKey);
  return {
    model,
    provider: providerKey,
    color,
    providerColor,
    softBg: `${providerColor}22`,
    borderColor: `${providerColor}66`,
    textColor: color,
  };
}

function buildUnifiedDailyModel(historyRows, sourceDaily) {
  const byDay = new Map();
  const modelTotals = new Map();

  for (const r of (historyRows || [])) {
    const day = r.day;
    if (!byDay.has(day)) {
      byDay.set(day, {
        day,
        totalTokens: 0,
        totalCost: 0,
        totalCalls: 0,
        models: {},
        modelCosts: {},
        modelProviders: {},
        sources: { channel: { tokens: 0, costUsd: 0, calls: 0 }, thread: { tokens: 0, costUsd: 0, calls: 0 }, cron: { tokens: 0, costUsd: 0, calls: 0 } },
      });
    }
    const d = byDay.get(day);
    const modelKey = canonicalKey(r.provider, r.model);
    d.totalTokens += Number(r.totalTokens || 0);
    d.totalCost += Number(r.costUsd || 0);
    d.totalCalls += Number(r.calls || 0);
    d.models[modelKey] = (d.models[modelKey] || 0) + Number(r.totalTokens || 0);
    d.modelCosts[modelKey] = (d.modelCosts[modelKey] || 0) + Number(r.costUsd || 0);
    d.modelProviders[modelKey] = r.provider || d.modelProviders[modelKey] || 'unknown';
    modelTotals.set(modelKey, (modelTotals.get(modelKey) || 0) + Number(r.totalTokens || 0));
  }

  for (const s of (sourceDaily || [])) {
    const day = s.day;
    if (!byDay.has(day)) {
      byDay.set(day, {
        day,
        totalTokens: 0,
        totalCost: 0,
        totalCalls: 0,
        models: {},
        modelCosts: {},
        modelProviders: {},
        sources: { channel: { tokens: 0, costUsd: 0, calls: 0 }, thread: { tokens: 0, costUsd: 0, calls: 0 }, cron: { tokens: 0, costUsd: 0, calls: 0 } },
      });
    }
    const d = byDay.get(day);
    d.sources = {
      channel: s.channel || { tokens: 0, costUsd: 0, calls: 0 },
      thread: s.thread || { tokens: 0, costUsd: 0, calls: 0 },
      cron: s.cron || { tokens: 0, costUsd: 0, calls: 0 },
    };
  }

  const allDaily = Array.from(byDay.values()).sort((a, b) => a.day.localeCompare(b.day));
  const windowModels = Array.from(modelTotals.entries())
    .sort((a, b) => b[1] - a[1])
    .map(([k]) => k);

  return { allDaily, windowModels };
}

let _costRangeDays = 30;

function _pstDateKey(v) {
  if (!v) return '';
  if (typeof v === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(v)) return v;
  return new Date(v).toLocaleDateString('en-CA', { timeZone: 'America/Los_Angeles' });
}

function _getAnalyticsWindow(daysList) {
  const all = [...(daysList || [])].sort((a, b) => _pstDateKey(a.day).localeCompare(_pstDateKey(b.day)));
  const range = ANALYTICS_STATE.rangeDays || 7;
  const endExclusive = Math.max(0, all.length - (ANALYTICS_STATE.windowOffset * range));
  const start = Math.max(0, endExclusive - range);
  return all.slice(start, endExclusive);
}

function _getAnalyticsWindowLabel(windowDays, range) {
  if (!windowDays || !windowDays.length) return `Last ${range} Days`;
  return `${windowDays[0].day.slice(5)} – ${windowDays[windowDays.length - 1].day.slice(5)} · ${range}d`;
}

function _renderAnalyticsToolbar() {
  const wrap = document.getElementById('analyticsRangeFilter');
  const label = document.getElementById('weekLabel');
  const prevBtn = document.getElementById('weekPrev');
  const nextBtn = document.getElementById('weekNext');
  if (!wrap) return;
  wrap.querySelectorAll('button[data-days]').forEach(btn => {
    const days = Number(btn.dataset.days || 7);
    const active = days === ANALYTICS_STATE.rangeDays;
    btn.style.background = active ? 'var(--accent)' : 'var(--surface)';
    btn.style.color = active ? '#fff' : 'var(--text2)';
    btn.style.border = '1px solid var(--border)';
    btn.style.borderRadius = '10px';
    btn.style.padding = '3px 10px';
    btn.onclick = () => {
      ANALYTICS_STATE.rangeDays = days;
      ANALYTICS_STATE.windowOffset = 0;
      _renderAnalyticsToolbar();
      if (ANALYTICS_STATE.allDaily?.length) initWeekNav(ANALYTICS_STATE.allDaily.map(d => ({ date: d.day, tokens: d.totalTokens, cost: d.totalCost, models: d.models, modelCosts: d.modelCosts })));
      if (typeof loadOpsBySource === 'function') loadOpsBySource(days);
      if (typeof renderAnalyticsDailyDetails === 'function') renderAnalyticsDailyDetails();
    };
  });
  const all = ANALYTICS_STATE.allDaily || [];
  const range = ANALYTICS_STATE.rangeDays || 7;
  const maxOffset = Math.max(0, Math.ceil(all.length / range) - 1);
  if (label) {
    const windowDays = _getAnalyticsWindow(all);
    label.textContent = _getAnalyticsWindowLabel(windowDays, range);
  }
  if (prevBtn) prevBtn.onclick = () => {
    ANALYTICS_STATE.windowOffset = Math.min(maxOffset, ANALYTICS_STATE.windowOffset + 1);
    _renderAnalyticsToolbar();
    if (ANALYTICS_STATE.allDaily?.length) initWeekNav(ANALYTICS_STATE.allDaily.map(d => ({ date: d.day, tokens: d.totalTokens, cost: d.totalCost, models: d.models, modelCosts: d.modelCosts })));
  };
  if (nextBtn) nextBtn.onclick = () => {
    ANALYTICS_STATE.windowOffset = Math.max(0, ANALYTICS_STATE.windowOffset - 1);
    _renderAnalyticsToolbar();
    if (ANALYTICS_STATE.allDaily?.length) initWeekNav(ANALYTICS_STATE.allDaily.map(d => ({ date: d.day, tokens: d.totalTokens, cost: d.totalCost, models: d.models, modelCosts: d.modelCosts })));
  };
}

function _ensureCostRangeFilter() {
  const existing = document.getElementById('costRangeFilter');
  if (existing) existing.remove();
}


async function loadOpsAlltime(days) {
  if (days === undefined) days = ANALYTICS_STATE.rangeDays || _costRangeDays || 7;
  ANALYTICS_STATE.rangeDays = days;
  _costRangeDays = days;

  const modelsEl = document.getElementById('alltimeModels');
  const subEl    = document.getElementById('alltimeSub');
  const opsTotalSub = document.getElementById('opsTotalSub');
  const opsTotalPills = document.getElementById('opsTotalPills');
  const opsModelBar = document.getElementById('opsModelBar');
  if (!modelsEl) return;

  _ensureCostRangeFilter();

  try {
    const apiDays = days >= 9999 ? 9999 : days;
    const hist = await apiFetch(`/dashboard/usage/models/history?days=${apiDays}`);
    const dayRows = hist.rows || [];

    // ── Totals ────────────────────────────────────────────────────────
    let totalCost   = Number(hist.summary?.costUsd || 0);
    let totalTokens = Number(hist.summary?.totalTokens || 0);

    const rangeLabel = days >= 9999 ? 'all time' : `last ${hist.days || days} days`;
    if (subEl) subEl.textContent = `${fmtTokens(totalTokens)} tokens · $${totalCost.toFixed(2)} · ${rangeLabel}`;

    // Today's Usage (PST) card uses today's dashboard-friendly usage endpoint
    try {
      const today = await apiFetch('/dashboard/usage/models/today');
      const todaySummary = today.summary || {};
      const todayRows = today.rows || [];
      if (opsTotalSub) {
        opsTotalSub.textContent = `${fmtTokens(todaySummary.totalTokens || 0)} tokens · $${Number(todaySummary.costUsd || 0).toFixed(2)} · ${todaySummary.calls || 0} calls today`;
      }
      if (opsTotalPills) {
        opsTotalPills.innerHTML = todayRows.slice(0, 4).map(r => `<span class="pill" style="border-color:${getModelColor(r.model)};color:${getModelColor(r.model)}">${shortModel(r.model)} ${fmtTokens(r.totalTokens || 0)}</span>`).join('');
      }
      if (opsModelBar) {
        const total = Number(todaySummary.totalTokens || 0) || 1;
        opsModelBar.innerHTML = '<div class="ops-bar-track">' + todayRows.map(r => `<div style="width:${((Number(r.totalTokens || 0)/total)*100).toFixed(2)}%;background:${getModelColor(r.model)}" title="${shortModel(r.model)}: ${fmtTokens(r.totalTokens || 0)}"></div>`).join('') + '</div>';
      }
    } catch {}

    // ── Model aggregation from HISTORY (not just today) ───────────────
    // Normalise local-model name variants so Qwen gguf rows don't appear
    // as separate entries for each filename/provider variant.
    // Map raw (provider, model) from ledger → stable display key + metadata
    // Must match the LEDGER_ALIAS_MAP in backend/providers/ground-truth.js
    function canonicalKey(provider, model) {
      const p = (provider || '').toLowerCase();
      const m = (model || '').toLowerCase().replace(/\.gguf$/i, '');
      // All local Qwen3.5 35B variants (dgx-spark + macbook + ollama-remote) → single key
      if (m.includes('qwen') && m.includes('35b') &&
          (p.includes('local') || p.includes('ollama'))) {
        // Distinguish mac vs spark
        if (p.includes('macbook') || p.includes('mac-pro') || p.includes('mac pro')) return 'local/qwen-mac';
        return 'local/qwen-spark';
      }
      // Qwen 27B variants
      if (m.includes('qwen') && m.includes('27b') &&
          (p.includes('local') || p.includes('ollama'))) {
        return 'local/qwen-27b';
      }
      if (m.includes('qwen') && m.includes('30b') &&
          (p.includes('local') || p.includes('ollama'))) return 'local/qwen3.5-30b';
      // anthropic/anthropic/... double prefix artifact → clean
      if (p.startsWith('anthropic/')) return `anthropic/${model || 'unknown'}`;
      return `${p}/${model || 'unknown'}`;
    }

    // Display name for the canonical key
    function canonicalDisplayName(key, rawModel) {
      if (key === 'local/qwen-spark') return 'Qwen-35B';
      if (key === 'local/qwen-27b')   return 'Qwen-27B';
      if (key === 'local/qwen-mac')   return 'Qwen-MacBook';
      if (key === 'local/qwen3.5-30b') return 'Qwen-30B';
      return shortModel(rawModel || key);
    }

    // Color lookup key for getModelColor(): prefer full "provider/model" id
    function colorKey(key, rawModel) {
      if (key === 'local/qwen-spark') return 'local-dgx-spark/Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf';
      if (key === 'local/qwen-mac')   return 'local-macbook-pro/qwen3.5:35b-a3b';
      return rawModel || key;
    }

    const modelAgg = new Map(); // key → { key, displayName, provider, rawModel, tokens, cost, messages, isLocal }

    for (const r of dayRows) {
      const key   = canonicalKey(r.provider, r.model);
      const toks  = Number(r.totalTokens || 0);
      const cost  = Number(r.costUsd || 0);
      const calls = Number(r.calls || 0);
      const prev  = modelAgg.get(key);
      const prov  = (r.provider || '').toLowerCase();
      const isLocal = prov.includes('local') || prov.includes('ollama') ||
                      (r.model || '').toLowerCase().includes('gguf');
      if (prev) {
        prev.tokens   += toks;
        prev.cost     += cost;
        prev.messages += calls;
      } else {
        modelAgg.set(key, {
          key,
          displayName: canonicalDisplayName(key, r.model),
          colorRef:    colorKey(key, r.model),
          provider:    r.provider || 'unknown',
          rawModel:    r.model || key,
          tokens:      toks,
          cost,
          messages:    calls,
          isLocal,
        });
      }
    }

    // Sort: local models by token desc, cloud models by cost desc, then interleave
    const cloudModels = [...modelAgg.values()].filter(m => !m.isLocal)
      .sort((a, b) => b.cost - a.cost);
    const localModels = [...modelAgg.values()].filter(m => m.isLocal)
      .sort((a, b) => b.tokens - a.tokens);
    const sortedModels = [...cloudModels, ...localModels];

    const grandTokens = sortedModels.reduce((s, m) => s + m.tokens, 0);

    modelsEl.innerHTML = sortedModels.length
      ? sortedModels.map(m => {
          const pct = grandTokens > 0 ? ((m.tokens / grandTokens) * 100).toFixed(1) : '0';
          const costStr = m.isLocal
            ? `<span style="color:var(--green);font-size:.7rem">local $0</span>`
            : `$${m.cost.toFixed(2)}`;
          return `<div class="ops-channel-card">
            <div class="ops-ch-left">
              <div class="ops-ch-name" style="font-size:.85rem">
                <span class="ops-model-dot" style="background:${getModelColor(m.colorRef || m.rawModel)};display:inline-block;margin-right:6px"></span>
                ${escHtml(m.displayName)}
                ${m.isLocal ? '<span style="font-size:.65rem;margin-left:4px;padding:1px 6px;border-radius:8px;background:rgba(63,185,80,.15);color:var(--green)">local</span>' : ''}
              </div>
              <div class="ops-ch-meta">
                <span>${m.messages.toLocaleString()} msgs</span>
                <span>${pct}% of tokens</span>
              </div>
            </div>
            <div class="ops-ch-right">
              <div class="ops-ch-tokens">${fmtTokens(m.tokens)}</div>
              <div class="ops-ch-cost">${costStr}</div>
            </div>
          </div>`;
        }).join('')
      : '<div class="ops-ch-meta" style="padding:8px 0">No usage data in this range.</div>';

    // ── Daily chart data ──────────────────────────────────────────────
    // Use daily_totals from API (pre-split local vs paid) when available,
    // fall back to building from rows for per-model color breakdown.
    const dailyMap = {};
    for (const r of dayRows) {
      const d = r.day;
      if (!dailyMap[d]) dailyMap[d] = { date: d, tokens: 0, cost: 0, localTokens: 0, paidTokens: 0, models: {}, modelCosts: {}, localModels: {} };
      const toks = Number(r.totalTokens || 0);
      const cost = Number(r.costUsd || 0);
      const alias = canonicalKey(r.provider, r.model);
      dailyMap[d].tokens           += toks;
      dailyMap[d].cost             += cost;
      dailyMap[d].models[alias]     = (dailyMap[d].models[alias]    || 0) + toks;
      dailyMap[d].modelCosts[alias] = (dailyMap[d].modelCosts[alias]|| 0) + cost;
      const provider = String(r.provider || '').toLowerCase();
      const modelRaw = String(r.model || '').toLowerCase();
      const isLocal = provider.includes('local') || provider.includes('ollama') || modelRaw.includes('gguf');
      if (isLocal) {
        dailyMap[d].localTokens += toks;
        dailyMap[d].localModels[alias] = (dailyMap[d].localModels[alias] || 0) + toks;
      } else {
        dailyMap[d].paidTokens += toks;
      }
    }
    const allDaily = Object.values(dailyMap).sort((a, b) => a.date < b.date ? -1 : 1);
    ANALYTICS_STATE.allDaily = allDaily.map(d => ({
      day: d.date,
      totalTokens: d.tokens,
      totalCost: d.cost,
      totalCalls: 0,
      models: d.models || {},
      modelCosts: d.modelCosts || {},
      modelProviders: Object.fromEntries(Object.keys(d.models || {}).map(k => [k, 'unknown'])),
      sources: { channel: { tokens: 0, costUsd: 0, calls: 0 }, thread: { tokens: 0, costUsd: 0, calls: 0 }, cron: { tokens: 0, costUsd: 0, calls: 0 } },
    }));
    ANALYTICS_STATE.windowModels = Array.from(new Set(allDaily.flatMap(d => Object.keys(d.models || {}))));
    _renderAnalyticsToolbar();
    if (allDaily.length > 0) initWeekNav(ANALYTICS_STATE.allDaily.map(d => ({ date: d.day, tokens: d.totalTokens, cost: d.totalCost, models: d.models, modelCosts: d.modelCosts })));

  } catch (e) {
    modelsEl.innerHTML = `<div class="empty-state"><p>${escHtml(e.message)}</p></div>`;
  }
}


async function loadOpsAudit() {
  const el = document.getElementById('auditContent');
  if (!el) return;
  try {
    const data = await apiFetch('/ops/audit');
    let html = '';

    // OpenAI
    const oi = data.openai;
    if (oi?.status === 'ok') {
      const t = oi.totals;
      const modelRows = Object.entries(oi.models || {}).sort((a, b) => b[1].input - a[1].input).map(([m, d]) =>
        `<div class="ops-channel-card" style="padding:8px 12px">
          <div class="ops-ch-left"><div class="ops-ch-name" style="font-size:.82rem">🟢 ${escHtml(shortModel(m))}</div>
          <div class="ops-ch-meta"><span>${d.requests} reqs</span><span>cached: ${fmtTokens(d.cached)}</span></div></div>
          <div class="ops-ch-right"><div class="ops-ch-tokens">${fmtTokens(d.input + d.output)}</div></div></div>`
      ).join('');
      html += `<div style="margin-bottom:12px">
        <div style="font-weight:600;margin-bottom:6px">OpenAI <span class="pill" style="border-color:#34d399;color:#34d399">✓ verified</span></div>
        <div class="ops-ch-meta" style="margin-bottom:8px">7d: ${fmtTokens(t.input)} in + ${fmtTokens(t.output)} out · ${t.requests} reqs · ${fmtTokens(t.cached)} cached</div>
        <div class="ops-channel-list">${modelRows}</div>
        ${Object.keys(oi.days||{}).length > 0 ? `<div class="ops-ch-meta" style="margin-top:6px">Days: ${Object.entries(oi.days).sort().map(([d,v])=>d.slice(5)+':'+fmtTokens(v.input+v.output)).join(' · ')}</div>` : ''}
      </div>`;
    } else {
      html += `<div style="margin-bottom:8px">OpenAI <span class="pill">${oi?.status || 'unknown'}</span> ${oi?.error || ''}</div>`;
    }

    // Anthropic
    const ac = data.anthropic;
    if (ac?.status === 'org_only') {
      html += `<div style="margin-bottom:8px">
        <div style="font-weight:600;margin-bottom:4px">Anthropic <span class="pill" style="border-color:#c084fc;color:#c084fc">org verified</span></div>
        <div class="ops-ch-meta">Org: ${escHtml(ac.org?.name)} · ${ac.activeKeys?.length || 0} active keys</div>
        <div class="ops-ch-meta" style="margin-top:2px;font-style:italic">${ac.note}</div>
      </div>`;
    } else {
      html += `<div style="margin-bottom:8px">Anthropic <span class="pill">${ac?.status || 'unknown'}</span></div>`;
    }

    // Google
    html += `<div>Google <span class="pill">${data.google?.status || 'no_api'}</span> <span class="ops-ch-meta">${data.google?.note || ''}</span></div>`;

    el.innerHTML = html;
  } catch (e) {
    el.innerHTML = `<div class="ops-ch-meta">Failed: ${escHtml(e.message)}</div>`;
  }
}

// ─── Usage by Source Type (Channel / Thread / Cron) ─────────────────────
let _sourceRangeDays = 7;

function _ensureSourceRangeFilter() {
  const subEl = document.getElementById('bySourceSub');
  if (!subEl) return;
  const parent = subEl.closest('.glass-card') || subEl.parentElement;
  if (!parent) return;
  if (document.getElementById('sourceRangeFilter')) return;

  const filterDiv = document.createElement('div');
  filterDiv.id = 'sourceRangeFilter';
  filterDiv.style.cssText = 'display:flex;gap:6px;align-items:center;margin-bottom:10px;flex-wrap:wrap';
  ['7d', '14d', '30d'].forEach(label => {
    const days = parseInt(label);
    const btn = document.createElement('button');
    btn.textContent = label;
    btn.dataset.days = days;
    btn.style.cssText = `padding:3px 10px;border-radius:10px;border:1px solid var(--border);
      background:${days === _sourceRangeDays ? 'var(--accent)' : 'var(--surface)'};
      color:${days === _sourceRangeDays ? '#fff' : 'var(--text2)'};
      cursor:pointer;font-size:.72rem;transition:background .15s`;
    btn.onclick = () => {
      _sourceRangeDays = days;
      document.querySelectorAll('#sourceRangeFilter button').forEach(b => {
        const active = Number(b.dataset.days) === _sourceRangeDays;
        b.style.background = active ? 'var(--accent)' : 'var(--surface)';
        b.style.color = active ? '#fff' : 'var(--text2)';
      });
      loadOpsBySource(_sourceRangeDays);
    };
    filterDiv.appendChild(btn);
  });

  const cardHeader = parent.querySelector('.card-header');
  if (cardHeader) {
    cardHeader.after(filterDiv);
  } else {
    parent.insertBefore(filterDiv, parent.firstChild);
  }
}

function renderSourceStackedChart(daily) {
  const chartEl = document.getElementById('bySourceChart');
  if (!chartEl) return;
  const chartDays = _getAnalyticsWindow((daily || []).map(d => ({ day: d.day, totalTokens: d.total?.tokens || 0, totalCost: d.total?.costUsd || 0 })));
  if (!chartDays.length) {
    chartEl.innerHTML = '';
    return;
  }
  const maxTokens = Math.max(...chartDays.map(d0 => {
    const d = daily.find(x => x.day === d0.day) || d0;
    return Number(d.total?.tokens || 0);
  }), 1);
  let chartHtml = '<div style="display:flex;align-items:flex-end;gap:8px;height:140px;padding:10px 0;">';
  for (const d0 of chartDays) {
    const d = daily.find(x => x.day === d0.day) || d0;
    const ch = Number(d.channel?.tokens || 0);
    const th = Number(d.thread?.tokens || 0);
    const cr = Number(d.cron?.tokens || 0);
    const totalLabel = fmtTokens(ch + th + cr);
    const selected = ANALYTICS_STATE.selectedDay === d.day;
    chartHtml += `<div style="flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;min-width:0;cursor:pointer" onclick="ANALYTICS_STATE.selectedDay='${d.day}'; ANALYTICS_STATE.expandedDay='${d.day}'; renderSourceStackedChart(ANALYTICS_STATE.sourceDaily||[]); renderAnalyticsDailyDetails(); renderCostHeatmap();">
      <div style="font-size:.62rem;color:var(--text1);font-variant-numeric:tabular-nums;white-space:nowrap">${totalLabel}</div>
      <div style="width:100%;display:flex;align-items:flex-end;height:110px;border-radius:8px;overflow:hidden;background:${selected ? 'color-mix(in srgb,var(--accent) 14%,transparent)' : 'color-mix(in srgb,var(--text1) 3%,transparent)'};outline:${selected ? '2px solid color-mix(in srgb,var(--accent) 70%,transparent)' : 'none'};outline-offset:2px;box-shadow:${selected ? '0 0 0 2px color-mix(in srgb,var(--accent) 12%,transparent), 0 8px 24px color-mix(in srgb,var(--accent) 18%,transparent)' : 'none'};transform:${selected ? 'translateY(-1px)' : 'none'};transition:all .15s ease">
        <div style="width:100%;display:flex;flex-direction:column;justify-content:flex-end;height:100%">
          <div style="background:var(--yellow);height:${(cr / maxTokens * 100)}%" title="Cron: ${fmtTokens(cr)}"></div>
          <div style="background:var(--green);height:${(th / maxTokens * 100)}%" title="Thread: ${fmtTokens(th)}"></div>
          <div style="background:var(--blue);height:${(ch / maxTokens * 100)}%" title="Channel: ${fmtTokens(ch)}"></div>
        </div>
      </div>
      <div style="font-size:.65rem;color:${selected ? 'var(--text1)' : 'var(--text2)'};white-space:nowrap">${d.day.slice(5)}</div>
    </div>`;
  }
  chartHtml += '</div>';
  chartHtml += `<div style="display:flex;gap:12px;justify-content:center;font-size:.72rem;margin-top:8px;flex-wrap:wrap">
    <span><span style="display:inline-block;width:8px;height:8px;background:var(--blue);border-radius:2px;margin-right:4px"></span>${tt('Channel', '频道')}</span>
    <span><span style="display:inline-block;width:8px;height:8px;background:var(--green);border-radius:2px;margin-right:4px"></span>${tt('Thread', '线程')}</span>
    <span><span style="display:inline-block;width:8px;height:8px;background:var(--yellow);border-radius:2px;margin-right:4px"></span>${tt('Cron', '定时')}</span>
  </div>`;
  chartEl.innerHTML = chartHtml;
}

function renderCostHeatmap() {
  const el = document.getElementById('costHeatmap');
  if (!el) return;
  const daily = _getAnalyticsWindow(ANALYTICS_STATE.allDaily || []);
  const modelKeys = (ANALYTICS_STATE.windowModels || []).filter(m => daily.some(d => (d.models?.[m] || d.modelCosts?.[m])));
  if (!daily.length || !modelKeys.length) {
    el.innerHTML = '';
    return;
  }
  let maxCost = 0;
  daily.forEach(d => modelKeys.forEach(m => { maxCost = Math.max(maxCost, Number(d.modelCosts?.[m] || 0)); }));
  maxCost = Math.max(maxCost, 0.001);
  let html = '<table><thead><tr><th>Model</th>' + daily.map(d => `<th style="${ANALYTICS_STATE.selectedDay===d.day ? 'color:var(--text1)' : ''}">${d.day.slice(5)}</th>`).join('') + '</tr></thead><tbody>';
  for (const mk of modelKeys) {
    const visual = getModelVisual(mk, daily.find(d => d.modelProviders?.[mk])?.modelProviders?.[mk]);
    html += `<tr><td><span style="display:inline-block;width:8px;height:8px;border-radius:999px;background:${visual.color};margin-right:6px"></span>${escHtml(shortModel(mk))}</td>`;
    for (const d of daily) {
      const val = Number(d.modelCosts?.[mk] || 0);
      const alpha = val > 0 ? Math.max(0.10, val / maxCost) : 0.04;
      const selected = ANALYTICS_STATE.selectedDay === d.day;
      const heatStrength = Math.round(alpha * 100);
      html += `<td onclick="ANALYTICS_STATE.selectedDay='${d.day}'; ANALYTICS_STATE.expandedDay='${d.day}'; renderSourceStackedChart(ANALYTICS_STATE.sourceDaily||[]); renderAnalyticsDailyDetails(); renderCostHeatmap();" style="cursor:pointer;${selected ? 'outline:2px solid color-mix(in srgb,var(--accent) 72%,transparent);border-radius:6px;box-shadow:inset 0 0 0 1px var(--border);background:color-mix(in srgb,var(--accent) 10%,transparent);' : ''}"><span class="heat-cell" style="background:color-mix(in srgb,var(--accent) ${heatStrength}%,transparent)">${val > 0 ? '$' + val.toFixed(2) : '·'}</span></td>`;
    }
    html += '</tr>';
  }
  html += '</tbody></table>';
  el.innerHTML = html;
}

function renderAnalyticsDailyDetails() {
  const listEl = document.getElementById('bySourceList');
  if (!listEl) return;
  const daily = _getAnalyticsWindow(ANALYTICS_STATE.allDaily || []);
  if (!daily.length) return;
  const sourceMap = new Map((ANALYTICS_STATE.sourceDaily || []).map(d => [d.day, d]));
  let html = '<div class="ops-channel-list">';
  for (const d of [...daily].reverse()) {
    const src = sourceMap.get(d.day) || {};
    const expanded = ANALYTICS_STATE.expandedDay === d.day;
    const selected = ANALYTICS_STATE.selectedDay === d.day;
    const topModels = Object.entries(d.models || {}).sort((a, b) => b[1] - a[1]);
    html += `<div class="ops-channel-card" style="display:block;padding:14px 16px;cursor:pointer;transition:all .15s ease;${selected ? 'outline:2px solid color-mix(in srgb,var(--accent) 72%,transparent);background:color-mix(in srgb,var(--accent) 10%,transparent);box-shadow:0 8px 24px color-mix(in srgb,var(--accent) 14%,transparent);transform:translateY(-1px);' : ''}" onclick="ANALYTICS_STATE.selectedDay='${d.day}'; ANALYTICS_STATE.expandedDay = ANALYTICS_STATE.expandedDay === '${d.day}' ? null : '${d.day}'; renderSourceStackedChart(ANALYTICS_STATE.sourceDaily||[]); renderAnalyticsDailyDetails(); renderCostHeatmap();">
      <div style="display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap">
        <div>
          <div class="ops-ch-name">📅 ${escHtml(d.day)} ${expanded ? '▾' : '▸'}</div>
          <div class="ops-ch-meta" style="margin-top:4px">
            <span>💬 ${fmtTokens(src.channel?.tokens || 0)}</span>
            <span>🧵 ${fmtTokens(src.thread?.tokens || 0)}</span>
            <span>⚙️ ${fmtTokens(src.cron?.tokens || 0)}</span>
          </div>
        </div>
        <div style="text-align:right">
          <div class="ops-ch-tokens">${fmtTokens(d.totalTokens || 0)}</div>
          <div class="ops-ch-cost">$${Number(d.totalCost || 0).toFixed(2)}</div>
        </div>
      </div>
      <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:10px">${topModels.slice(0, 4).map(([mk, v]) => {
        const visual = getModelVisual(mk, d.modelProviders?.[mk]);
        return `<span class="pill" style="border-color:${visual.borderColor};color:${visual.textColor};background:${visual.softBg}"><span style="display:inline-block;width:8px;height:8px;border-radius:999px;background:${visual.color};margin-right:6px"></span>${escHtml(shortModel(mk))} ${fmtTokens(v)}</span>`;
      }).join('')}</div>
      ${expanded ? `<div style="margin-top:12px;padding-top:12px;border-top:1px solid var(--border)">${topModels.map(([mk, v]) => {
        const cost = Number(d.modelCosts?.[mk] || 0);
        const visual = getModelVisual(mk, d.modelProviders?.[mk]);
        return `<div style="display:flex;justify-content:space-between;gap:12px;align-items:center;padding:6px 0">
          <div style="display:flex;align-items:center;gap:8px;min-width:0">
            <span style="display:inline-block;width:10px;height:10px;border-radius:999px;background:${visual.color}"></span>
            <span style="color:${visual.textColor}">${escHtml(shortModel(mk))}</span>
          </div>
          <div class="ops-ch-meta"><span>${fmtTokens(v)}</span><span>$${cost.toFixed(2)}</span></div>
        </div>`;
      }).join('')}</div>` : ''}
    </div>`;
  }
  html += '</div>';
  listEl.innerHTML = html;
}

async function loadOpsBySource(days) {
  if (days === undefined) days = _sourceRangeDays;
  else _sourceRangeDays = days;

  const listEl = document.getElementById('bySourceList');
  const subEl = document.getElementById('bySourceSub');
  const chartEl = document.getElementById('bySourceChart');
  if (!listEl) return;

  _ensureSourceRangeFilter();

  try {
    const data = await apiFetch(`/dashboard/usage/source/history?days=${days}`);
    const summary = data.summary || {};
    const daily = data.daily || [];
    ANALYTICS_STATE.sourceDaily = daily;
    const total = summary.total || { tokens: 0, costUsd: 0, calls: 0 };

    const windowDaily = _getAnalyticsWindow((daily || []).map(d => ({ day: d.day, totalTokens: d.total?.tokens || 0, totalCost: d.total?.costUsd || 0 })));
    if (subEl) {
      subEl.textContent = `${fmtTokens(total.tokens || 0)} tokens · ${(total.calls || 0).toLocaleString()} calls · $${Number(total.costUsd || 0).toFixed(2)} · ${_getAnalyticsWindowLabel(windowDaily, ANALYTICS_STATE.rangeDays)}`;
    }

    const sourceTypes = [
      { key: 'channel', icon: '💬', name: tt('Channel Sessions', '对话频道') },
      { key: 'thread', icon: '🧵', name: tt('Thread Sessions', '线程对话') },
      { key: 'cron', icon: '⚙️', name: tt('Cron Jobs', '定时任务') }
    ];

    let html = '<div class="ops-channel-list">';
    for (const st of sourceTypes) {
      const s = summary[st.key] || { calls: 0, tokens: 0, costUsd: 0 };
      const pct = (total.tokens || 0) > 0 ? ((s.tokens / total.tokens) * 100).toFixed(1) : '0';
      html += `<div class="ops-channel-card">
        <div class="ops-ch-left">
          <div class="ops-ch-name">${st.icon} ${escHtml(st.name)}</div>
          <div class="ops-ch-meta">
            <span>${(s.calls || 0).toLocaleString()} ${tt('calls', '调用')}</span>
            <span>${pct}% ${tt('of tokens', 'Token 占比')}</span>
          </div>
        </div>
        <div class="ops-ch-right">
          <div class="ops-ch-tokens">${fmtTokens(s.tokens || 0)}</div>
          <div class="ops-ch-cost">$${Number(s.costUsd || 0).toFixed(2)}</div>
        </div>
      </div>`;
    }
    html += '</div>';

    listEl.innerHTML = html;

    renderSourceStackedChart(daily);
    renderAnalyticsDailyDetails();
    renderCostHeatmap();
  } catch (e) {
    listEl.innerHTML = `<div class="empty-state"><h3>Unable to load</h3><p>${escHtml(e.message)}</p></div>`;
  }
}

// ─── Ops Management Actions ───
