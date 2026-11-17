
/* Overview Tab — Sessions, Agent Monitor, DGX Spark */
var escHtml = window.escHtml || function(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\"/g, '&quot;')
    .replace(/'/g, '&#39;');
};

async function loadOverviewHealthCards() {
  try {
    await renderAgentMonitor();
  } catch(e) {
    console.warn('Overview health cards failed:', e.message);
  }
}

async function loadOverviewUsageCards() {
  try {
    const data = await apiFetch('/dashboard/usage/models/today');
    const summary = data.summary || {};
    const rows = data.rows || [];

    const mainBadge = document.getElementById('mainAgentBadge');
    const mainValue = document.getElementById('mainAgentValue');
    const mainDetail = document.getElementById('mainAgentDetail');
    if (mainValue) {
      mainBadge.className = 'agent-stat-badge active';
      mainBadge.innerHTML = '<span class="pulse-dot"></span> today';
      mainValue.textContent = '$' + Number(summary.costUsd || 0).toFixed(2);
      mainDetail.textContent = (summary.calls || 0) + ' calls';
    }

    const subBadge = document.getElementById('subagentBadge');
    const subVal = document.getElementById('subagentValue');
    const subDetail = document.getElementById('subagentDetail');
    if (subVal) {
      subVal.textContent = fmtTokens(summary.totalTokens || 0);
      subBadge.className = 'agent-stat-badge active';
      subBadge.innerHTML = 'today';
      const top = [...rows].sort((a, b) => Number(b.totalTokens || 0) - Number(a.totalTokens || 0))[0];
      subDetail.textContent = top ? 'Top: ' + shortModel(top.model) : '—';
    }

    const mixEl = document.getElementById('modelMixBars');
    if (mixEl) {
      if (!rows.length) {
        mixEl.innerHTML = '<div class="ops-ch-meta">No usage data today</div>';
      } else {
        const total = Number(summary.totalTokens || 0) || 1;
        let barHtml = '<div style="display:flex;height:10px;border-radius:5px;overflow:hidden;margin-bottom:6px">';
        const colors = {};
        rows.forEach(r => {
          const m = r.model || 'unknown';
          const tk = Number(r.totalTokens || 0);
          const pct = (tk / total) * 100;
          const c = getModelColor(m);
          colors[m] = c;
          barHtml += `<div style="width:${pct}%;background:${c};min-width:2px" title="${shortModel(m)} ${pct.toFixed(0)}%"></div>`;
        });
        barHtml += '</div><div style="display:flex;flex-wrap:wrap;gap:4px 10px;font-size:.7rem">';
        rows.forEach(r => {
          const m = r.model || 'unknown';
          const pct = ((Number(r.totalTokens || 0) / total) * 100).toFixed(0);
          barHtml += `<span style="color:${colors[m]}">● ${shortModel(m)} <b>${pct}%</b></span>`;
        });
        barHtml += '</div>';
        mixEl.innerHTML = barHtml;
      }
    }
  } catch(e) {
    console.warn('Overview usage cards failed:', e.message);
  }
}

async function loadAgentMonitor() {
  agentData = await apiFetch('/agents').catch(() => null);
  await Promise.all([
    loadOverviewUsageCards(),
    loadOverviewHealthCards(),
  ]);
}


async function loadDiscordSurfacesTable() {
  const tableEl = document.getElementById('sessionsTable');
  const alertsEl = document.getElementById('sessionsAlerts');
  if (!tableEl) return;
  try {
    const data = await apiFetch('/ops/discord-surfaces');
    const rows = data.rows || [];
    const summary = data.summary || {};
    if (alertsEl) {
      alertsEl.innerHTML = `<div class="sess-alert info"><span>💬</span><strong>${tt('Discord surfaces', 'Discord 面')}</strong> ${tt('Primary view groups usage by Discord channel first, then shows OpenClaw stats.', '主视图先按 Discord 频道聚合，再展示 OpenClaw 统计。')}</div>`;
    }
    if (!rows.length) {
      tableEl.innerHTML = '<div class="empty-state"><h3>No Discord channel usage today</h3></div>';
      return;
    }
    let html = `<div style="margin-bottom:10px;color:var(--text2);font-size:.78rem">${tt('Today summary', '今日汇总')}: <b>${Number(summary.calls || 0).toLocaleString()}</b> calls · <b>${fmtTokens(summary.totalTokens || 0)}</b> · <b>$${Number(summary.costUsd || 0).toFixed(2)}</b></div>`;
    html += `<table class="sessions-table">
      <thead><tr>
        <th>${tt('Discord Channel / Thread', 'Discord 频道 / 线程')}</th>
        <th>${tt('Calls', '调用')}</th>
        <th>Tokens</th>
        <th>${tt('Cost', '花费')}</th>
        <th>${tt('Top Model', '主模型')}</th>
        <th>${tt('Last Activity', '最近活动')}</th>
      </tr></thead><tbody>`;
    for (const r of rows) {
      const isThreadSurface = r.surfaceType === 'thread-surface';
      const parent = (r.parentChannelName && r.parentChannelName !== r.channelName) ? r.parentChannelName : r.channelName;
      const subLine = isThreadSurface
        ? `<br><span style="color:var(--text2);font-size:.68rem">🧵 ${escHtml(r.threadName || 'thread')}</span>`
        : '';
      html += `<tr>
        <td style="font-weight:600">${escHtml(parent || ('#' + r.channelId))}${subLine}</td>
        <td>${Number(r.calls || 0).toLocaleString()}</td>
        <td>${fmtTokens(r.totalTokens || 0)}</td>
        <td style="font-weight:600">$${Number(r.costUsd || 0).toFixed(2)}</td>
        <td>${r.topModel ? `<span class="sess-model" style="border-color:${getModelColor(r.topModel)};color:${getModelColor(r.topModel)}">${shortModel(r.topModel)}</span>` : '—'}</td>
        <td style="color:var(--text2);font-size:.75rem">${r.lastTs ? new Date(r.lastTs).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '—'}</td>
      </tr>`;
    }
    html += '</tbody></table>';
    tableEl.innerHTML = html;
  } catch (e) {
    tableEl.innerHTML = `<div class="empty-state"><p>${escHtml(e.message)}</p></div>`;
  }
}

async function loadSessions() {
  const alertsEl = document.getElementById('sessionsAlerts');
  const tableEl = document.getElementById('sessionsTable');
  if (!tableEl) return;

  // New primary view: Discord surfaces first.
  return loadDiscordSurfacesTable();

  try {
    const url = _sessionsHideStale ? '/ops/sessions?hideStale=1' : '/ops/sessions';
    const data = await apiFetch(url);
    let sessions = data.sessions || [];
    
    // Filter out inactive sessions (no activity today) if toggle is on
    if (window._sessionsHideInactive) {
      sessions = sessions.filter(s => (s.today?.messages || 0) > 0 || (s.today?.totalTokens || 0) > 0);
    }
    const alerts = data.alerts || [];
    const summary = data.summary || {};

    // Alerts
    if (alertsEl) {
      alertsEl.innerHTML = alerts.map(a =>
        `<div class="sess-alert ${a.type}"><span>${a.type === 'error' ? '🔴' : a.type === 'waste' ? '🟡' : '⚪'}</span><strong>${escHtml(a.session)}</strong> ${escHtml(a.msg)}</div>`
      ).join('');
    }

    // Table
    if (sessions.length === 0) {
      tableEl.innerHTML = '<div class="empty-state"><h3>No sessions</h3></div>';
      return;
    }

    // Chinese names + task type for Discord channels
    const rowKindMeta = {
      channel: { label: tt('Channel Session', '频道会话'), emoji: '💬' },
      cron: { label: tt('Cron Job', '定时任务'), emoji: '⚙️' },
      system: { label: tt('System / Internal', '系统 / 内部'), emoji: '🫀' },
      other: { label: tt('Pseudo / Other', '伪会话 / 其他'), emoji: '•' },
    };

    const channelMeta = {
      '#dev_build':              { cn: '开发构建', task: '🔧 深度开发', tier: 'hard' },
      '#ai-learning':            { cn: 'AI学习', task: '🧠 架构讨论', tier: 'hard' },
      '#ops-report':             { cn: '运维报告', task: '📊 汇报转发', tier: 'easy' },
      '#general':                { cn: '综合频道', task: '💬 闲聊', tier: 'easy' },
      '#openclaw-watch':         { cn: '生态监控', task: '🔍 监控播报', tier: 'medium' },
      '#jobs-intel':             { cn: '求职情报', task: '💼 搜索整理', tier: 'medium' },
      '#x-ai-socal-radar':      { cn: 'X/AI雷达', task: '🐦 内容创作', tier: 'hard' },
      '#tech-news':              { cn: '科技新闻', task: '📰 摘要生成', tier: 'medium' },
      '#podcast_video_article':  { cn: '播客/视频', task: '📝 内容摘要', tier: 'medium' },
      '#meta-vision-ingest':     { cn: '视觉入口', task: '👁️ 图片路由', tier: 'easy' },
      '#socal-ai-events':        { cn: '南加AI活动', task: '🎯 活动搜索', tier: 'medium' },
      '#event-planning':         { cn: '活动策划', task: '📅 规划', tier: 'easy' },
      '#networking-log':         { cn: '人脉记录', task: '👤 信息录入', tier: 'easy' },
      '#工作搭子碎碎念':          { cn: '工作搭子', task: '💬 闲聊', tier: 'easy' },
      '#饮酒':                   { cn: '饮酒', task: '🍷 品鉴记录', tier: 'easy' },
      '#灰茄':                   { cn: '灰茄', task: '🚬 品鉴记录', tier: 'easy' },
      '#品茶':                   { cn: '品茶', task: '🍵 品鉴记录', tier: 'easy' },
      '#养花':                   { cn: '养花', task: '🌱 记录', tier: 'easy' },
      '#灵修':                   { cn: '灵修', task: '📖 灵修提醒', tier: 'easy' },
    };

    // Model tier: what complexity level is this model suited for
    const modelTier = m => {
      if (!m) return 'easy';
      if (m.includes('opus')) return 'hard';
      if (m.includes('sonnet') || m.includes('codex') || m.includes('pro')) return 'medium';
      return 'easy'; // flash, etc.
    };

    // Fit assessment
    function fitLabel(s) {
      if (!s.fitEligible) {
        if (s.rowKind === 'cron') return { emoji: '⚙️', text: tt('Cron', '定时'), tip: tt('Cron rows are shown for visibility, not model-fit scoring', 'Cron 行仅展示可见性，不参与模型匹配评分') };
        if (s.rowKind === 'system') return { emoji: '🫀', text: tt('System', '系统'), tip: tt('System/internal rows are excluded from fit scoring', '系统/内部行不参与模型匹配评分') };
        return { emoji: '•', text: tt('Other', '其他'), tip: tt('Not scored for model fit', '不参与模型匹配评分') };
      }
      const meta = channelMeta[s.displayName];
      const taskTier = meta?.tier || 'medium';
      const mTier = modelTier(s.model);
      const tiers = { easy: 0, medium: 1, hard: 2 };
      const diff = tiers[mTier] - tiers[taskTier];
      if (diff >= 2) return { emoji: '🔴', text: tt('Overkill', '过高'), tip: tt('Model is far above task complexity, consider downgrade', '模型远超任务需求，建议降级') };
      if (diff === 1) return { emoji: '🟡', text: tt('High', '偏高'), tip: tt('Could downgrade to save cost', '可考虑降级节省成本') };
      if (diff === 0) return { emoji: '🟢', text: tt('Match', '匹配'), tip: tt('Model matches task complexity', '模型与任务复杂度匹配') };
      if (diff === -1) return { emoji: '🔵', text: tt('Low', '偏低'), tip: tt('Task might need stronger model', '任务较复杂，可考虑升级') };
      return { emoji: '⚪', text: '—', tip: '' };
    }

    const fitSortRank = s => {
      const text = fitLabel(s).text;
      if (text === tt('Overkill', '过高')) return 4;
      if (text === tt('High', '偏高')) return 3;
      if (text === tt('Match', '匹配')) return 2;
      if (text === tt('Low', '偏低')) return 1;
      return 0;
    };

    const getSortValue = (s, key) => {
      const eff = s.today.effectiveMessages || 0;
      if (key === 'model') return shortModel(s.model || '').toLowerCase();
      if (key === 'messages') return s.today.messages || 0;
      if (key === 'tokens') return s.today.totalTokens || 0;
      if (key === 'cost') return s.today.cost || 0;
      if (key === 'costPerMsg') return eff > 0 ? (s.today.cost || 0) / eff : null;
      if (key === 'fit') return fitSortRank(s);
      return null;
    };

    const sortedSessions = [...sessions];
    if (sessionSortState.key) {
      const dir = sessionSortState.dir === 'asc' ? 1 : -1;
      sortedSessions.sort((a, b) => {
        const av = getSortValue(a, sessionSortState.key);
        const bv = getSortValue(b, sessionSortState.key);
        if (av == null && bv == null) return a.displayName.localeCompare(b.displayName, 'zh-Hans');
        if (av == null) return 1;
        if (bv == null) return -1;
        if (typeof av === 'string' || typeof bv === 'string') {
          const cmp = String(av).localeCompare(String(bv), 'zh-Hans');
          if (cmp !== 0) return cmp * dir;
          return a.displayName.localeCompare(b.displayName, 'zh-Hans');
        }
        if (av === bv) return a.displayName.localeCompare(b.displayName, 'zh-Hans');
        return (av - bv) * dir;
      });
    }

    let html = `<table class="sessions-table">
      <thead><tr>
        <th>${tt('Channel', '频道')}</th>
        <th>${tt('Task', '任务')}</th>
        <th><button type="button" class="sess-sort-btn ${sessionSortState.key === 'model' ? 'active' : ''}" onclick="toggleSessionSort('model')">${tt('Model', '模型')} <span class="sess-sort-indicator">${sessionSortIndicator('model')}</span></button></th>
        <th title="Effective = total − HEARTBEAT_OK − NO_REPLY"><button type="button" class="sess-sort-btn ${sessionSortState.key === 'messages' ? 'active' : ''}" onclick="toggleSessionSort('messages')">${tt('Messages', '消息')} ⓘ <span class="sess-sort-indicator">${sessionSortIndicator('messages')}</span></button></th>
        <th><button type="button" class="sess-sort-btn ${sessionSortState.key === 'tokens' ? 'active' : ''}" onclick="toggleSessionSort('tokens')">Tokens <span class="sess-sort-indicator">${sessionSortIndicator('tokens')}</span></button></th>
        <th><button type="button" class="sess-sort-btn ${sessionSortState.key === 'cost' ? 'active' : ''}" onclick="toggleSessionSort('cost')">${tt('Cost', '花费')} <span class="sess-sort-indicator">${sessionSortIndicator('cost')}</span></button></th>
        <th><button type="button" class="sess-sort-btn ${sessionSortState.key === 'costPerMsg' ? 'active' : ''}" onclick="toggleSessionSort('costPerMsg')">${tt('$/msg', '$/条')} <span class="sess-sort-indicator">${sessionSortIndicator('costPerMsg')}</span></button></th>
        <th><button type="button" class="sess-sort-btn ${sessionSortState.key === 'fit' ? 'active' : ''}" onclick="toggleSessionSort('fit')">${tt('Fit', '匹配')} <span class="sess-sort-indicator">${sessionSortIndicator('fit')}</span></button></th>
      </tr></thead><tbody>`;

    for (const s of sortedSessions) {
      const meta = channelMeta[s.displayName] || {};
      const cn = meta.cn || '';
      const kindMeta = rowKindMeta[s.rowKind] || rowKindMeta.other;
      const taskTag = s.fitEligible ? normalizeTaskTag(meta.task || '') : `<span title="${escHtml(kindMeta.label)}">${kindMeta.emoji} ${escHtml(kindMeta.label)}</span>`;
      const eff = s.fitEligible ? (s.today.effectiveMessages || 0) : 0;
      const costPerMsg = eff > 0 ? (s.today.cost / eff) : 0;
      const costColor = !s.fitEligible ? 'var(--text2)' : costPerMsg > 1.5 ? '#f87171' : costPerMsg > 0.5 ? '#fbbf24' : 'var(--green)';
      const fit = fitLabel(s);

      const thinkingLvl = s.thinkingLevel && s.thinkingLevel !== '—' ? s.thinkingLevel : '';
      const thinkingColor = thinkingLvl === 'low' ? 'var(--green)' : thinkingLvl === 'medium' ? '#fbbf24' : thinkingLvl === 'high' ? '#f87171' : 'var(--text2)';
      const thinkingTag = thinkingLvl
        ? `<span style="font-size:.58rem;padding:0 4px;border-radius:3px;border:1px solid ${thinkingColor};color:${thinkingColor};margin-left:4px;vertical-align:middle">🧠 ${escHtml(thinkingLvl)}</span>`
        : '';

      const nameHtml = cn
        ? `<span class="sess-name">${escHtml(s.displayName)}</span>${thinkingTag}<br><span style="color:var(--text2);font-size:.65rem">${isZh() ? cn : `CN: ${cn}`}</span>`
        : `<span class="sess-name">${escHtml(s.displayName)}</span>${thinkingTag}`;

      // Model selector dropdown
      const modelSelect = s.channelId ? buildModelSelect(s.model, s.channelId, 'session') : `<span class="sess-model" style="border-color:${getModelColor(s.model)};color:${getModelColor(s.model)}">${shortModel(s.model)}</span>`;

      // Status badge colors: active=green, idle=yellow, stale=gray, error=red
      const statusColor = s.status === 'active' ? '#34d399' : s.status === 'idle' ? '#fbbf24' : s.status === 'stale' ? '#6b7280' : s.status === 'error' ? '#f87171' : '#6b7280';
      html += `<tr>
        <td><span class="sess-status" style="display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;background:${statusColor};border:1px solid rgba(255,255,255,0.1)"></span>${nameHtml}</td>
        <td style="font-size:.7rem">${taskTag}</td>
        <td>${modelSelect}</td>
        <td>${s.today.messages}<span style="color:var(--text2);font-size:.65rem"><br>${s.fitEligible ? `${eff} ${tt('effective', '有效')}` : tt('not scored', '不计评分')}</span></td>
        <td>${fmtTokens(s.today.totalTokens)}</td>
        <td style="font-weight:600">$${s.today.cost.toFixed(2)}</td>
        <td style="color:${costColor};font-weight:600">${eff > 0 ? '$' + costPerMsg.toFixed(2) : '—'}</td>
        <td title="${fit.tip}">${fit.emoji} <span style="font-size:.65rem">${fit.text}</span></td>
      </tr>`;
    }
    html += '</tbody></table>';
    tableEl.innerHTML = html;
  } catch (e) {
    tableEl.innerHTML = `<div class="empty-state"><p>${escHtml(e.message)}</p></div>`;
  }
}


async function loadDgxStatus() {
  const badge = document.getElementById('dgxStatusBadge');
  const content = document.getElementById('dgxContent');
  if (!content) return;
  try {
    const d = await apiFetch('/ops/dgx-status');

    const snap = d.snapshot || {};
    const llama = snap.llama || {};
    const modelFromSnap = llama.model || {};

    const online = !!d.online;
    const isSleeping = !!d.isSleeping;
    // Status badge
    if (!online) {
      badge.textContent = '🔴 Offline';
      badge.style.background = 'rgba(239,68,68,.2)';
      badge.style.color = '#ef4444';
      content.innerHTML = '<div style="color:var(--text2);font-size:.85rem">DGX Spark is not reachable.</div>';
      return;
    }
    if (isSleeping) {
      badge.textContent = '😴 Sleeping';
      badge.style.background = 'rgba(251,191,36,.15)';
      badge.style.color = '#fbbf24';
    } else {
      badge.textContent = '🟢 Online';
      badge.style.background = 'rgba(34,197,94,.15)';
      badge.style.color = '#22c55e';
    }

    // Backward + forward compatible field mapping
    const m = d.model || {
      name: modelFromSnap.model_path || modelFromSnap.name || 'Qwen-35B',
      nParams: modelFromSnap.n_params_human || modelFromSnap.n_params || null,
      sizeGiB: modelFromSnap.size_gib || null,
      nCtxTrain: modelFromSnap.n_ctx_train || null,
      buildInfo: llama.version || null,
    };
    const slotsObj = d.slots || {};
    const slotList = Array.isArray(llama.slots) ? llama.slots : [];
    const slotBusyFallback = slotList.filter(x => x.is_processing).length;
    const slotTotalFallback = slotList.length;
    const ctxPerSlotFallback = slotList[0]?.n_ctx || null;
    const s = {
      busy: slotsObj.busy ?? slotBusyFallback,
      total: slotsObj.total ?? slotTotalFallback,
      ctxPerSlot: slotsObj.ctxPerSlot ?? ctxPerSlotFallback,
      totalCtx: slotsObj.totalCtx ?? ((slotTotalFallback && ctxPerSlotFallback) ? slotTotalFallback * ctxPerSlotFallback : null),
    };
    const g = d.genDefaults || {
      temperature: llama.default_generation_settings?.temperature,
      topP: llama.default_generation_settings?.top_p,
      topK: llama.default_generation_settings?.top_k,
      minP: llama.default_generation_settings?.min_p,
      maxTokens: llama.default_generation_settings?.n_predict,
      reasoningFormat: llama.default_generation_settings?.reasoning_format,
    };
    const slotUsed = s.busy || 0;
    const slotTotal = s.total || 0;
    const slotPct = slotTotal ? Math.round(slotUsed / slotTotal * 100) : 0;
    const slotColor = slotPct >= 75 ? '#ef4444' : slotPct >= 50 ? '#fbbf24' : '#22c55e';

    // Metrics section (GPU)
    let gpuHtml = '';
    if (d.metricsAvailable && d.metrics) {
      const mx = d.metrics;
      const kvPct = mx.kvCacheUsage != null ? (mx.kvCacheUsage * 100).toFixed(1) : null;
      const kvColor = kvPct >= 90 ? '#ef4444' : kvPct >= 70 ? '#fbbf24' : '#22c55e';
      gpuHtml = `
        <div class="ops-row" style="grid-template-columns:repeat(3,1fr);margin-top:12px">
          ${kvPct != null ? `<div class="glass-card" style="padding:10px;text-align:center">
            <div style="font-size:.7rem;color:var(--text2);margin-bottom:4px">KV Cache</div>
            <div style="font-size:1.1rem;font-weight:700;color:${kvColor}">${kvPct}%</div>
          </div>` : ''}
          ${mx.promptTps != null ? `<div class="glass-card" style="padding:10px;text-align:center">
            <div style="font-size:.7rem;color:var(--text2);margin-bottom:4px">Prompt t/s</div>
            <div style="font-size:1.1rem;font-weight:700">${mx.promptTps.toFixed(0)}</div>
          </div>` : ''}
          ${mx.predictTps != null ? `<div class="glass-card" style="padding:10px;text-align:center">
            <div style="font-size:.7rem;color:var(--text2);margin-bottom:4px">Predict t/s</div>
            <div style="font-size:1.1rem;font-weight:700">${mx.predictTps.toFixed(0)}</div>
          </div>` : ''}
        </div>`;
    } else if (d.metricsNote) {
      gpuHtml = `<div style="margin-top:10px;padding:8px 12px;background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.2);border-radius:8px;font-size:.72rem;color:#fbbf24">
        ⚠️ ${escHtml(d.metricsNote)}
      </div>`;
    }

    content.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px">
        <!-- Model Info -->
        <div class="glass-card" style="padding:12px">
          <div style="font-size:.7rem;color:var(--text2);margin-bottom:6px;font-weight:600">MODEL</div>
          <div style="font-weight:600;font-size:.88rem;word-break:break-all">${escHtml(m.name || '—')}</div>
          <div style="font-size:.73rem;color:var(--text2);margin-top:4px">
            ${m.nParams ? `<span>${m.nParams} params</span>` : ''}
            ${m.sizeGiB ? `<span style="margin-left:8px">${m.sizeGiB} GiB quantized</span>` : ''}
          </div>
          <div style="font-size:.72rem;color:var(--text2);margin-top:2px">
            ${m.nCtxTrain ? `Train ctx: ${(m.nCtxTrain/1024).toFixed(0)}k tokens` : ''}
          </div>
          ${m.buildInfo ? `<div style="font-size:.68rem;color:var(--text2);margin-top:4px;opacity:.6">Build: ${escHtml(m.buildInfo)}</div>` : ''}
        </div>

        <!-- Slots -->
        <div class="glass-card" style="padding:12px">
          <div style="font-size:.7rem;color:var(--text2);margin-bottom:6px;font-weight:600">SLOTS & CONTEXT</div>
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
            <span style="font-size:1.3rem;font-weight:700;color:${slotColor}">${slotUsed}</span>
            <span style="color:var(--text2);font-size:.8rem">/ ${slotTotal} slots busy</span>
          </div>
          <div style="height:6px;background:rgba(255,255,255,.1);border-radius:3px;overflow:hidden;margin-bottom:6px">
            <div style="width:${slotPct}%;height:100%;background:${slotColor};border-radius:3px;transition:width .4s"></div>
          </div>
          <div style="font-size:.72rem;color:var(--text2)">
            ${s.ctxPerSlot ? `${(s.ctxPerSlot/1024).toFixed(0)}k ctx/slot` : ''}
            ${s.totalCtx ? ` · ${(s.totalCtx/1024).toFixed(0)}k total` : ''}
          </div>
        </div>
      </div>

      <!-- Generation Defaults -->
      <div class="glass-card" style="padding:12px;margin-bottom:0">
        <div style="font-size:.7rem;color:var(--text2);margin-bottom:8px;font-weight:600">GENERATION SETTINGS</div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;font-size:.73rem">
          ${g.temperature != null ? `<span class="pill">temp <b>${g.temperature.toFixed(2)}</b></span>` : ''}
          ${g.topP != null ? `<span class="pill">top_p <b>${g.topP.toFixed(2)}</b></span>` : ''}
          ${g.topK != null ? `<span class="pill">top_k <b>${g.topK}</b></span>` : ''}
          ${g.minP != null ? `<span class="pill">min_p <b>${g.minP.toFixed(3)}</b></span>` : ''}
          ${g.maxTokens != null && g.maxTokens > 0 ? `<span class="pill">max_tokens <b>${g.maxTokens}</b></span>` : ''}
          ${g.reasoningFormat ? `<span class="pill" style="border-color:#818cf8;color:#818cf8">reasoning <b>${escHtml(g.reasoningFormat)}</b></span>` : ''}
          ${g.thinkingForcedOpen ? `<span class="pill" style="border-color:#818cf8;color:#818cf8">think 🧠</span>` : ''}
        </div>
      </div>
      ${gpuHtml}
      <div style="font-size:.68rem;color:var(--text2);margin-top:8px;text-align:right">
        ${escHtml(baseUrl)} · updated ${new Date(d.fetchedAt || Date.now()).toLocaleTimeString()}
      </div>
    `;
  } catch(e) {
    badge.textContent = '❓ Error';
    content.innerHTML = `<div style="color:#ef4444;font-size:.8rem">${escHtml(e.message)}</div>`;
  }
}
