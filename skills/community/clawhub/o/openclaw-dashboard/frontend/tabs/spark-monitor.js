/**
 * spark-monitor.js — Spark Monitor Tab
 * Shows: task summary cards, GPU timeline chart, recent task list, PR Hunter results
 */

// ── Summary Cards ─────────────────────────────────────────────────────────────

async function loadSparkSummary() {
  try {
    const data = await apiFetch('/dashboard/spark/today');
    if (!data?.ok) {
      console.warn('[spark-monitor] summary not ok:', data);
      return;
    }

    document.getElementById('sparkTasksDone').textContent    = data.summary?.completedTasks ?? '0';
    document.getElementById('sparkTasksRunning').textContent = data.summary?.runningTasks ?? '0';
    document.getElementById('sparkTasksError').textContent   = data.summary?.failedTasks ?? '0';
    document.getElementById('sparkGpuAvg').textContent = data.summary?.gpuUtilizationPct != null ? Number(data.summary.gpuUtilizationPct).toFixed(1) + '%' : '—';
    document.getElementById('sparkTokensTotal').textContent = (data.summary?.totalTokens || 0) > 0 ? fmtTokens(data.summary.totalTokens) : '0';

    // PR Hunter latest / recent tasks summary reuse
    renderPrHunterLatest(data.recent || []);
  } catch (e) {
    console.warn('[spark-monitor] summary error:', e);
  }
}

function fmtTokens(n) {
  if (n >= 1e6) return (n / 1e6).toFixed(1) + 'M';
  if (n >= 1e3) return (n / 1e3).toFixed(1) + 'K';
  return String(n);
}

// ── Task Timeline Chart (24h) ─────────────────────────────────────────────────
// REMOVED: Timeline deleted per user request. Task info now shown in Recent Tasks list.
async function loadSparkGpuTimeline() {
  // No-op: timeline removed
  const el = document.getElementById('sparkGpuChart');
  if (el) el.innerHTML = '<div style="color:var(--text2);text-align:center;padding:20px;font-size:.8rem">Task activity shown in Recent Tasks below</div>';
}

// ── Task List (Enhanced) ─────────────────────────────────────────────────────

async function loadSparkTaskList() {
  const type   = document.getElementById('sparkTaskTypeFilter')?.value || '';
  const status = document.getElementById('sparkTaskStatusFilter')?.value || '';
  const el     = document.getElementById('sparkTaskList');
  if (!el) return;

  try {
    // Fetch tasks from last 24 hours
    const data = await apiFetch(`/api/spark-tasks/list?type=${type}&status=${status}&hours=24&limit=100`);
    const tasks = data?.tasks || [];

    if (tasks.length === 0) {
      el.innerHTML = '<div style="color:var(--text2);text-align:center;padding:20px;font-size:.8rem">No tasks yet — first run at 3:00 AM PST</div>';
      return;
    }

    const statusColor = { done: 'var(--green)', running: 'var(--blue)', error: 'var(--red)', unknown: 'var(--text2)' };
    const statusBg    = {
      done: 'color-mix(in srgb,var(--green) 14%,transparent)',
      running: 'color-mix(in srgb,var(--blue) 14%,transparent)',
      error: 'color-mix(in srgb,var(--red) 14%,transparent)',
      unknown: 'color-mix(in srgb,var(--text2) 12%,transparent)',
    };
    const statusIcon  = { done: '✓', running: '●', error: '✕', unknown: '?' };

    const rows = tasks.map(t => {
      const sc   = statusColor[t.status] || statusColor.unknown;
      const sb   = statusBg[t.status] || statusBg.unknown;
      const si   = statusIcon[t.status]  || statusIcon.unknown;
      
      // Format duration
      let dur = '—';
      if (t.duration_s != null) {
        const mins = Math.floor(t.duration_s / 60);
        const secs = Math.floor(t.duration_s % 60);
        dur = mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;
      }
      
      // Format tokens
      const tokens = t.tokens_used ? fmtTokens(t.tokens_used) : '—';
      
      // Format time - larger and more prominent
      const finishedTime = t.finished_at 
        ? new Date(t.finished_at).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
        : (t.started_at ? new Date(t.started_at).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—');
      
      // Summary
      const sum = t.result_summary ? `<div style="font-size:.75rem;color:var(--text2);margin-top:4px;line-height:1.4">${t.result_summary}</div>` : '';
      
      return `<div style="display:flex;align-items:flex-start;gap:12px;padding:12px 0;border-bottom:1px solid var(--border)">
        <!-- Status Icon -->
        <div style="width:28px;height:28px;border-radius:50%;background:${sb};color:${sc};display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:600;flex-shrink:0">${si}</div>
        
        <!-- Main Content -->
        <div style="flex:1;min-width:0">
          <!-- Task Name -->
          <div style="font-size:.9rem;font-weight:600;color:var(--text1);margin-bottom:2px">${t.task_name}</div>
          
          <!-- Type -->
          <div style="font-size:.72rem;color:var(--text2);margin-bottom:6px">${t.task_type}</div>
          
          <!-- Summary -->
          ${sum}
        </div>
        
        <!-- Right Side: Time, Duration, Tokens -->
        <div style="text-align:right;flex-shrink:0;min-width:100px">
          <!-- Finished Time - Larger -->
          <div style="font-size:.85rem;font-weight:500;color:var(--text1);margin-bottom:4px">${finishedTime}</div>
          
          <!-- Duration & Tokens - Highlighted -->
          <div style="display:flex;gap:8px;justify-content:flex-end;margin-bottom:4px">
            <span style="font-size:.75rem;padding:3px 8px;border-radius:6px;background:color-mix(in srgb,var(--blue) 12%,transparent);color:var(--blue);font-weight:500">⏱ ${dur}</span>
            <span style="font-size:.75rem;padding:3px 8px;border-radius:6px;background:color-mix(in srgb,var(--green) 12%,transparent);color:var(--green);font-weight:500">🪙 ${tokens}</span>
          </div>
          
          <!-- Status Badge -->
          <span style="font-size:.7rem;padding:2px 10px;border-radius:12px;background:${sb};color:${sc};font-weight:500">${t.status}</span>
        </div>
      </div>`;
    }).join('');

    el.innerHTML = `<div>${rows}</div>`;
  } catch (e) {
    el.innerHTML = `<div style="color:var(--red);font-size:.8rem">Error: ${escHtml(e.message)}</div>`;
  }
}

// ── PR Hunter Results ─────────────────────────────────────────────────────────

function renderPrHunterLatest(recent) {
  const el = document.getElementById('sparkPrHunterContent');
  if (!el) return;

  const prTask = recent.find(t => t.task_type === 'pr_hunter' && t.status === 'done');
  if (!prTask) {
    el.innerHTML = `<div style="color:var(--text2);font-size:.82rem;padding:20px;text-align:center">
      <div style="font-size:1.5rem;margin-bottom:8px">🌙</div>
      PR Hunter 首次运行在凌晨 3:00 AM PST<br>
      <span style="font-size:.72rem">分析 OpenClaw 最近 merge 的 PR，找趋势 + 生成 PR 草稿</span>
    </div>`;
    return;
  }

  const ts  = new Date(prTask.finished_at || prTask.started_at).toLocaleString();
  const dur = prTask.duration_s ? `${Number(prTask.duration_s).toFixed(0)}s` : '—';
  el.innerHTML = `<div style="font-size:.8rem">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">
      <span style="color:var(--green);font-weight:600">✅ Last Run: ${ts}</span>
      <span style="color:var(--text2)">· ${dur}</span>
    </div>
    <div style="padding:10px;background:rgba(255,255,255,.04);border-radius:8px;color:var(--text1);line-height:1.6">
      ${prTask.result_summary || 'No summary available'}
    </div>
    <div style="margin-top:8px;font-size:.7rem;color:var(--text2)">
      结果文件保存在 Spark: ~/spark-agent/results/pr-hunter/ · 每天凌晨 3:00 更新
    </div>
  </div>`;
}

// ── Tab Init ──────────────────────────────────────────────────────────────────

async function loadSparkMonitor() {
  await Promise.all([
    loadSparkSummary(),
    loadSparkGpuTimeline(),
    loadSparkTaskList(),
  ]);
}

// Register with boot system (same pattern as other tabs)
if (typeof window !== 'undefined') {
  window._sparkMonitorInit = false;
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        if (btn.dataset.tab === 'spark' && !window._sparkMonitorInit) {
          window._sparkMonitorInit = true;
          loadSparkMonitor();
        }
      });
    });

    // i18n labels
    const el = document.getElementById('tabSparkLabel');
    if (el) el.textContent = (window._lang === 'zh') ? 'Spark' : 'Spark';
  });
}
