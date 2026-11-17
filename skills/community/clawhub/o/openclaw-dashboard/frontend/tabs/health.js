
/* Health Tab — Operations Control */
var escHtml = window.escHtml || function(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\"/g, '&quot;')
    .replace(/'/g, '&#39;');
};

async function loadSystemInfo() {
  // Model registry is now static (defined in cron.js)
  // Only refresh colors from server (non-critical visual)
  try {
    const data = await apiFetch('/ops/models');
    if (data.colors) Object.assign(MODEL_COLORS, data.colors);
  } catch(e) {}

  try {
    const [sys, mx] = await Promise.all([
      apiFetch('/ops/system').catch(() => ({})),
      apiFetch('/metrics').catch(() => ({})),
    ]);
    if (sys.models?.primary) {
      const p = sys.models.primary;
      globalDefaultModel = p.includes('/') ? p.split('/').pop() : p;
    }
    const navVersion = document.getElementById('navVersion');
    if (navVersion && sys.clawVersion) navVersion.textContent = `OpenClaw ${sys.clawVersion}`;
    const el = document.getElementById('systemInfoBar');
    const c = document.getElementById('systemInfoContent');
    if (!el || !c) return;

    const memPct = Number(sys.memory?.usePct ?? mx.memory?.pct ?? 0);
    const memColor = memPct > 85 ? 'var(--red)' : memPct > 60 ? 'var(--yellow)' : 'var(--green)';
    const diskUse = sys.disk?.usePct || sys.disk?.percent || (sys.disk?.usedHuman && sys.disk?.totalHuman ? `${sys.disk.usedHuman}/${sys.disk.totalHuman}` : '—');
    const diskPct = parseInt(diskUse, 10) || 0;
    const diskColor = diskPct > 80 ? 'var(--red)' : diskPct > 60 ? 'var(--yellow)' : 'var(--green)';

    const host = sys.macModel || sys.hostname || mx.hostname || 'Mac mini';
    const cpus = sys.cpus || mx.cpu?.count || '—';
    const load1 = Number(sys.loadAvg?.['1m'] ?? mx.cpu?.overall ?? 0).toFixed(1);

    const chips = [
      `<span>🖥️ <strong>${escHtml(host)}</strong></span>`,
      sys.macOS ? `<span>🍎 ${escHtml(sys.macOS)}</span>` : '',
      `<span>🧮 ${cpus} ${tt('cores', '核')} · Load ${load1}</span>`,
      `<span style="color:${memColor}">💾 RAM ${memPct.toFixed(0)}%</span>`,
      `<span style="color:${diskColor}">💿 Disk ${escHtml(diskUse)}</span>`,
      sys.nodeVersion ? `<span>📦 Node ${escHtml(sys.nodeVersion)}</span>` : '',
      sys.clawVersion ? `<span>🦞 v${escHtml(sys.clawVersion)}</span>` : '',
    ].filter(Boolean);
    c.innerHTML = chips.join('');
    el.style.display = '';
  } catch (_) {
    const el = document.getElementById('systemInfoBar');
    const c = document.getElementById('systemInfoContent');
    if (el && c) {
      c.innerHTML = `<span style="color:var(--yellow)">⚠️ ${tt('Mac mini status unavailable', 'Mac mini 状态暂不可用')}</span>`;
      el.style.display = '';
    }
  }
}

async function renderAgentMonitor() {
  await loadSystemInfo();

  const [watchdog, sessionsData, cronData] = await Promise.all([
    apiFetch('/ops/watchdog?limit=60&windowMinutes=240').catch(() => ({})),
    apiFetch('/ops/sessions').catch(() => ({ alerts: [] })),
    apiFetch('/ops/cron').catch(() => ({ jobs: [] })),
  ]);

  // Overview cards are rendered by Overview tab, not Health tab.

  // Overview health cards only: Alert Snapshot, Watchdog, System Sentinel.
  // Usage cards are owned by Overview tab.

  // Card 3: Alert Snapshot
  const sessionAlerts = (sessionsData.alerts || []).length;
  const cronErrors = (cronData.jobs || []).filter(j => {
    const s = String(j?.lastRun?.status || '').toLowerCase();
    return s && s !== 'ok' && s !== 'success' && s !== 'delivered';
  }).length;
  const watchdogDown = String(watchdog.effectiveStatus || '') === 'down' ? 1 : 0;
  const alertTotal = sessionAlerts + cronErrors + watchdogDown;

  const cronVal = document.getElementById('cronValue');
  const cronBadge = document.getElementById('cronBadge');
  const cronDetail = document.getElementById('cronDetail');
  cronVal.textContent = alertTotal;
  cronBadge.className = `agent-stat-badge ${alertTotal > 0 ? 'error' : 'active'}`;
  cronBadge.innerHTML = alertTotal > 0 ? `⚠️ ${alertTotal} ${tt('open', '未恢复')}` : `✅ ${tt('clear', '正常')}`;
  cronDetail.textContent = `${sessionAlerts} ${tt('session', '会话')} · ${cronErrors} cron · ${watchdogDown} watchdog`;

  // Card 4: Watchdog Status
  const hookVal = document.getElementById('hookValue');
  const hookBadge = document.getElementById('hookBadge');
  const hookDetail = document.getElementById('hookDetail');
  const wdStatus = watchdog.effectiveStatus || 'unknown';
  const wdRunning = !!watchdog.runtime?.running;
  hookVal.textContent = wdStatus === 'healthy' ? tt('Healthy', '健康') : wdStatus === 'down' ? tt('Down', '断连') : tt('Unknown', '未知');
  hookBadge.className = `agent-stat-badge ${wdRunning ? 'active' : 'error'}`;
  hookBadge.innerHTML = wdRunning ? '✓' : '✕';
  hookDetail.textContent = wdRunning ? tt('Watchdog active', 'Watchdog 运行中') : tt('Watchdog inactive', 'Watchdog 未运行');

  // Card 5: System Status
  const sentinelValue = document.getElementById('sentinelValue');
  const sentinelBadge = document.getElementById('sentinelBadge');
  const sentinelDetail = document.getElementById('sentinelDetail');
  const allHealthy = wdRunning && alertTotal === 0;
  sentinelValue.textContent = allHealthy ? tt('All Good', '一切正常') : tt('Check', '需检查');
  sentinelBadge.className = `agent-stat-badge ${allHealthy ? 'active' : 'error'}`;
  sentinelBadge.innerHTML = allHealthy ? '✓' : '⚠';
  sentinelDetail.textContent = allHealthy ? tt('No alerts', '无告警') : `${alertTotal} ${tt('alerts', '告警')}`;

  renderSessionsPanel();
}

function renderSessionsPanel() {
  // Load today's cron runs instead of active sessions
  loadCronRuns();
}


async function loadQuality() {
  const el = document.getElementById('qualityContent');
  if (!el) return;
  try {
    const data = await apiFetch('/ops/sessions');
    const sessions = (data.sessions || []).filter(s => s.today.messages > 0);
    sessions.sort((a, b) => (b.today.messages || 0) - (a.today.messages || 0));

    let html = `<div class="glass-card" style="padding:16px;margin-bottom:12px"><div class="card-title">${tt('Session Activity (Today)', '会话活跃度（今日）')}</div><div class="card-sub">${tt(
      'Simplified view: channel/thread name + messages + tokens + cost.',
      '简化视图：仅展示频道/线程名称 + 消息数 + tokens + 成本。'
    )}</div></div>`;
    html += '<div class="ops-channel-list">';
    for (const s of sessions) {
      html += `<div class="ops-channel-card">
        <div class="ops-ch-left" style="flex:1">
          <div class="ops-ch-name">${escHtml(s.displayName)}</div>
          <div class="ops-ch-meta"><span>${s.today.messages} msgs</span><span>${fmtTokens(s.today.totalTokens || 0)} tokens</span><span>$${Number(s.today.cost || 0).toFixed(2)}</span></div>
        </div>
      </div>`;
    }
    html += '</div>';
    el.innerHTML = html;
  } catch (e) { el.innerHTML = `<p>${escHtml(e.message)}</p>`; }
}


async function loadAudit() {
  const el = document.getElementById('auditContent2');
  if (!el) return;
  try {
    const [data, changelog] = await Promise.all([
      apiFetch('/ops/sessions'),
      apiFetch('/ops/model-changelog').catch(() => ({ entries: [] })),
    ]);
    const channelMap = new Map((data.sessions || []).map(s => [String(s.channelId), s.displayName || s.channelId]));
    const sessions = (data.sessions || []).filter(s => s.today.messages > 0);
    const changeEntries = Array.isArray(changelog?.entries) ? changelog.entries.slice(0, 20) : [];

    const recommendations = [];
    for (const s of sessions) {
      // Expensive model with high idle rate
      if (s.model?.includes('opus') && s.today.noReplyRate > 40 && s.today.messages > 3) {
        recommendations.push({ severity: 'high', session: s.displayName, msg: `Using Claude Opus 4 but ${s.today.noReplyRate}% idle → switch to Claude Sonnet 4 (save ~$${(s.today.cost * 0.8).toFixed(0)}/day)`, model: s.model });
      }
      // Opus for simple channel
      if (s.model?.includes('opus') && s.today.effectiveMessages < 5 && s.today.cost > 1) {
        recommendations.push({ severity: 'medium', session: s.displayName, msg: `Claude Opus 4 overkill — only ${s.today.effectiveMessages} effective msgs, costing $${s.today.cost.toFixed(2)}`, model: s.model });
      }
      // No thinking level set
      if (s.thinkingLevel === '—' && s.today.messages > 0) {
        recommendations.push({ severity: 'low', session: s.displayName, msg: 'No thinking level set — consider setting to "low" to save tokens', model: s.model });
      }
    }

    let html = '<div class="glass-card" style="padding:16px;margin-bottom:12px"><div class="card-title">Config Audit</div><div class="card-sub">' + recommendations.length + ' recommendations</div></div>';

    if (recommendations.length === 0) {
      html += '<div class="empty-state"><h3>✅ All Good</h3><p>No optimization opportunities detected.</p></div>';
    } else {
      html += '<div class="ops-channel-list">';
      const sevColors = { high: '#f87171', medium: '#fbbf24', low: '#6b7280' };
      for (const r of recommendations) {
        html += `<div class="sess-alert" style="background:${sevColors[r.severity]}15;border:1px solid ${sevColors[r.severity]}40">
          <span style="font-size:1.1rem">${r.severity === 'high' ? '🔴' : r.severity === 'medium' ? '🟡' : '⚪'}</span>
          <div><strong>${escHtml(r.session)}</strong><br><span style="font-size:.8rem;color:var(--text2)">${escHtml(r.msg)}</span></div>
        </div>`;
      }
      html += '</div>';
    }

    // Provider audit (from existing)
    try {
      const audit = await apiFetch('/ops/audit');
      html += '<div class="glass-card" style="padding:16px;margin-top:12px"><div class="card-title">Provider Verification</div>';
      const oi = audit.openai;
      if (oi?.status === 'ok') {
        html += `<div style="margin:8px 0"><strong>OpenAI</strong> <span class="pill" style="border-color:#34d399;color:#34d399">✓</span> 7d: ${oi.totals.requests} reqs</div>`;
      }
      const ac = audit.anthropic;
      if (ac?.org) {
        html += `<div><strong>Anthropic</strong> <span class="pill" style="border-color:#c084fc;color:#c084fc">org ✓</span> ${ac.org.name} · ${ac.activeKeys?.length} keys</div>`;
      }
      html += '</div>';
    } catch {}

    // System info
    try {
      const sys = await apiFetch('/ops/system');
      const memPct = sys.memory?.usePct || '—';
      const memUsed = ((sys.memory?.used || 0) / 1073741824).toFixed(1);
      const memTotal = ((sys.memory?.total || 0) / 1073741824).toFixed(1);
      const load = sys.loadAvg?.['1m']?.toFixed(2) || '—';
      const uptimeH = Math.floor((sys.dashboardUptime || 0) / 3600);
      const uptimeM = Math.floor(((sys.dashboardUptime || 0) % 3600) / 60);
      html += `<div class="glass-card" style="padding:16px;margin-top:12px">
        <div class="card-title">🖥️ System (${escHtml(sys.hostname || '')})</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px;font-size:.82rem">
          <div>💻 <strong>${escHtml(sys.macModel || sys.platform)}</strong></div>
          <div>🍎 macOS ${escHtml(sys.macOS || '—')}</div>
          <div>🧮 CPU: ${sys.cpus} cores · Load: ${load}</div>
          <div>💾 RAM: ${memUsed}/${memTotal} GB (${memPct}%)</div>
          <div>💿 Disk: ${sys.disk?.used || '—'} / ${sys.disk?.total || '—'} (${sys.disk?.usePct || '—'})</div>
          <div>⏱️ Dashboard: ${uptimeH}h ${uptimeM}m</div>
          <div>📦 Node: ${escHtml(sys.nodeVersion || '—')}</div>
          <div>🦞 OpenClaw: ${escHtml(sys.clawVersion || '—')}</div>
        </div>
        <div style="margin-top:8px">
          <div style="font-size:.72rem;color:var(--text2);margin-bottom:2px">Memory ${memPct}%</div>
          <div style="height:8px;border-radius:4px;background:rgba(255,255,255,.1);overflow:hidden">
            <div style="height:100%;width:${memPct}%;background:${+memPct>80?'var(--red)':+memPct>60?'var(--yellow)':'var(--green)'};border-radius:4px;transition:width .5s"></div>
          </div>
          <div style="font-size:.72rem;color:var(--text2);margin:4px 0 2px">Disk ${sys.disk?.usePct || '—'}</div>
          <div style="height:8px;border-radius:4px;background:rgba(255,255,255,.1);overflow:hidden">
            <div style="height:100%;width:${sys.disk?.usePct || '0%'};background:${parseInt(sys.disk?.usePct)>80?'var(--red)':parseInt(sys.disk?.usePct)>60?'var(--yellow)':'var(--green)'};border-radius:4px;transition:width .5s"></div>
          </div>
        </div>
      </div>`;
    } catch {}

    const fmtChangeTs = (ts) => {
      const ms = Date.parse(ts || '');
      if (!Number.isFinite(ms)) return '—';
      const d = new Date(ms);
      const mm = String(d.getMonth() + 1).padStart(2, '0');
      const dd = String(d.getDate()).padStart(2, '0');
      const hh = String(d.getHours()).padStart(2, '0');
      const mi = String(d.getMinutes()).padStart(2, '0');
      return `${mm}/${dd} ${hh}:${mi}`;
    };
    const shortId = (id) => {
      const raw = String(id || '');
      if (!raw) return '—';
      if (raw.length <= 14) return raw;
      return `${raw.slice(0, 6)}...${raw.slice(-4)}`;
    };

    html += `<div class="glass-card" style="padding:16px;margin-top:12px">
      <div class="card-title">🔄 ${tt('Model Change History', '模型变更历史')}</div>`;
    if (!changeEntries.length) {
      html += `<div class="empty-state" style="padding:10px 4px 2px"><p>${tt('No model changes yet', '暂无变更记录')}</p></div>`;
    } else {
      html += '<div style="margin-top:8px">';
      for (const item of changeEntries) {
        const isCron = item?.type === 'cron';
        const typeLabel = isCron ? 'CRON' : 'SESSION';
        const typeColor = isCron ? 'var(--yellow)' : 'var(--blue)';
        const displayName = isCron ? (item?.name || item?.id || '—') : (channelMap.get(String(item?.id)) || shortId(item?.id));
        const fromModel = shortModel(item?.from || 'unknown');
        const toModel = shortModel(item?.to || 'unknown');
        const via = item?.via || 'dashboard';
        html += `<div style="display:grid;grid-template-columns:82px 74px 1fr;gap:8px;align-items:center;padding:7px 2px;border-bottom:1px solid var(--border);font-size:.76rem">
          <span style="font-family:var(--mono);color:var(--text2)">${fmtChangeTs(item?.ts)}</span>
          <span style="display:inline-flex;align-items:center;justify-content:center;padding:2px 8px;border-radius:999px;font-size:.66rem;font-weight:700;letter-spacing:.5px;background:${typeColor}1f;color:${typeColor};border:1px solid ${typeColor}4d">${typeLabel}</span>
          <div style="min-width:0;display:flex;align-items:center;gap:8px;flex-wrap:wrap">
            <span style="color:var(--text);font-family:var(--mono);font-size:.72rem">${escHtml(displayName)}</span>
            <span style="color:var(--text2)">${escHtml(fromModel)} → ${escHtml(toModel)}</span>
            <span style="display:inline-flex;align-items:center;padding:1px 7px;border-radius:999px;border:1px solid var(--border);color:var(--text2);font-size:.64rem;text-transform:lowercase">${escHtml(via)}</span>
          </div>
        </div>`;
      }
      html += '</div>';
    }
    html += '</div>';

    el.innerHTML = html;
  } catch (e) { el.innerHTML = `<p>${escHtml(e.message)}</p>`; }
}

// timeSince() is defined in shared/ui-utils.js

// ─── Config Viewer ───
