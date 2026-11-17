window.escHtml = window.escHtml || function escHtml(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\"/g, '&quot;')
    .replace(/'/g, '&#39;');
};

/* Boot & Init — runs after all tab modules loaded */

function activateTab(tabName) {
  let activeButton = null;
  document.querySelectorAll('.tab-btn').forEach(btn => {
    const active = btn.dataset.tab === tabName;
    btn.classList.toggle('active', active);
    btn.setAttribute('aria-current', active ? 'page' : 'false');
    if (active) activeButton = btn;
  });
  document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.toggle('active', panel.id === `panel-${tabName}`));
  const pageTitle = document.getElementById('pageTitle');
  const pageDescription = document.getElementById('pageDescription');
  const titleKey = isZh() ? 'titleZh' : 'title';
  const descriptionKey = isZh() ? 'descriptionZh' : 'description';
  if (activeButton && pageTitle) pageTitle.textContent = activeButton.dataset[titleKey] || activeButton.textContent.trim();
  if (activeButton && pageDescription) pageDescription.textContent = activeButton.dataset[descriptionKey] || '';
  if (tabName === 'copilot' && typeof initCopilot === 'function') initCopilot();
}

async function refreshTabData(tabName) {
  if (tabName === 'overview') {
    try { await loadSessions(); } catch {}
    try { await loadCronRuns(); } catch {}
    return;
  }
  if (tabName === 'ops') {
    const range = (window.ANALYTICS_STATE && window.ANALYTICS_STATE.rangeDays) || 7;
    try { await loadOpsAlltime(range); } catch (e) { console.error('loadOpsAlltime failed', e); }
    try { await loadOpsBySource(range); } catch (e) { console.error('loadOpsBySource failed', e); }
    return;
  }
  if (tabName === 'tasks') {
    try { await loadCronCosts(); } catch (e) { console.error('loadCronCosts failed', e); }
    try { await loadCronRuns(); } catch (e) { console.error('loadCronRuns failed', e); }
    return;
  }
  if (tabName === 'health') {
    try { await loadSystemInfo(); } catch {}
    return;
  }
  if (tabName === 'spark') {
    try { await loadSparkMonitor(); } catch {}
    return;
  }
  if (tabName === 'config') {
    try { await loadConfig(); } catch {}
    try { await loadSkills(); } catch {}
    try { await loadFileList(); } catch {}
    return;
  }
}

function initTabs() {
  document.querySelectorAll('.tab-btn[data-tab]').forEach(btn => {
    btn.onclick = async () => {
      const tabName = btn.dataset.tab;
      activateTab(tabName);
      await refreshTabData(tabName);
    };
  });
}

// ─── Week Navigation ───
let _weekAllDaily = [];
let _weekOffset = 0; // 0 = current week, -1 = last week, etc.

function initWeekNav(allDaily) {
  _weekAllDaily = allDaily;
  _weekOffset = 0;
  const prevBtn = document.getElementById('weekPrev');
  const nextBtn = document.getElementById('weekNext');
  if (prevBtn) prevBtn.onclick = () => { _weekOffset--; renderWeekView(); };
  if (nextBtn) nextBtn.onclick = () => { _weekOffset++; renderWeekView(); };
  renderWeekView();
}

function getWeekSlice(allDaily, offset) {
  const fmtDate = (d) => new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/Los_Angeles',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(d);

  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Los_Angeles',
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    weekday: 'short',
  }).formatToParts(new Date());
  const part = (type) => parts.find(p => p.type === type)?.value;
  const y = Number(part('year'));
  const m = Number(part('month'));
  const d0 = Number(part('day'));
  const wd = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(part('weekday'));
  const dayOfWeek = wd >= 0 ? wd : 0;
  const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;

  const thisMonday = new Date(Date.UTC(y, m - 1, d0 + mondayOffset + (offset * 7), 12, 0, 0));
  const thisSunday = new Date(Date.UTC(y, m - 1, d0 + mondayOffset + (offset * 7) + 6, 12, 0, 0));

  const startStr = fmtDate(thisMonday);
  const endStr = fmtDate(thisSunday);

  const result = [];
  for (let i = 0; i < 7; i++) {
    const di = new Date(Date.UTC(y, m - 1, d0 + mondayOffset + (offset * 7) + i, 12, 0, 0));
    const dateStr = fmtDate(di);
    const existing = allDaily.find(x => x.date === dateStr);
    result.push(existing || { date: dateStr, tokens: 0, cost: 0, models: {}, modelCosts: {} });
  }

  return { days: result, startStr, endStr, monday: thisMonday };
}

function _drawWeeklyStackedChart(canvas, days, valueKey, modelKeys, providersByModel, legendSelector) {
  if (!canvas || !days || !days.length) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const W = Math.max(320, (canvas.parentElement?.clientWidth || 360) - 12);
  const H = 120;
  canvas.width = W * 2;
  canvas.height = H * 2;
  canvas.style.width = W + 'px';
  canvas.style.height = H + 'px';
  ctx.setTransform(2, 0, 0, 2, 0, 0);
  ctx.clearRect(0, 0, W, H);

  const pad = { l: 24, r: 8, t: 10, b: 22 };
  const innerW = W - pad.l - pad.r;
  const innerH = H - pad.t - pad.b;
  const totals = days.map(d => Number(d[valueKey] || 0));
  const maxVal = Math.max(...totals, 1);
  const step = innerW / days.length;
  const barW = Math.max(12, step * 0.58);
  const theme = getChartThemeColors();

  ctx.strokeStyle = theme.border;
  ctx.lineWidth = 1;
  for (let i = 0; i <= 3; i++) {
    const y = pad.t + (innerH / 3) * i;
    ctx.beginPath();
    ctx.moveTo(pad.l, y);
    ctx.lineTo(W - pad.r, y);
    ctx.stroke();
  }

  days.forEach((d, i) => {
    const x = pad.l + i * step + (step - barW) / 2;
    let yCursor = pad.t + innerH;
    for (const mk of (modelKeys || [])) {
      const sourceMap = valueKey === 'totalCost' ? (d.modelCosts || {}) : (d.models || {});
      const v = Number(sourceMap[mk] || 0);
      if (!v) continue;
      const h = Math.max(1, (v / maxVal) * innerH);
      yCursor -= h;
      const visual = typeof getModelVisual === 'function' ? getModelVisual(mk, providersByModel?.[mk]) : { color: theme.accent };
      ctx.fillStyle = visual.color;
      ctx.fillRect(x, yCursor, barW, h);
    }

    const total = Number(d[valueKey] || 0);
    if (total > 0) {
      const label = valueKey === 'totalCost'
        ? ('$' + (total >= 100 ? total.toFixed(0) : total.toFixed(2)))
        : (typeof fmtTokens === 'function' ? fmtTokens(total) : String(total));
      ctx.fillStyle = theme.text;
      ctx.font = '10px system-ui, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(label, x + barW / 2, Math.max(10, yCursor - 4));
    }
  });

  ctx.fillStyle = theme.muted;
  ctx.font = '10px system-ui, sans-serif';
  ctx.textAlign = 'center';
  days.forEach((d, i) => {
    const x = pad.l + i * step + step / 2;
    ctx.fillText(String(d.day || d.date || '').slice(5), x, H - 6);
  });

  const legendEl = legendSelector ? document.querySelector(legendSelector) : null;
  if (legendEl) {
    legendEl.innerHTML = (modelKeys || []).slice(0, 8).map(mk => {
      const visual = typeof getModelVisual === 'function' ? getModelVisual(mk, providersByModel?.[mk]) : { color: theme.accent, providerColor: theme.accent };
      return `<span class="pill" style="border-color:${visual.borderColor};color:${visual.textColor};background:${visual.softBg}"><span style="display:inline-block;width:8px;height:8px;border-radius:999px;background:${visual.color};margin-right:6px"></span>${escHtml(shortModel(mk))}</span>`;
    }).join('');
  }
}

function renderWeekView() {
  const { days, startStr, endStr } = getWeekSlice(_weekAllDaily, _weekOffset);
  const label = document.getElementById('weekLabel');
  const prevBtn = document.getElementById('weekPrev');
  const nextBtn = document.getElementById('weekNext');
  const dailyCanvas = document.getElementById('dailyChart');
  const costCanvas = document.getElementById('dailyCostChart');

  const oldestDate = _weekAllDaily.length > 0 ? _weekAllDaily[0].date : startStr;
  const hasPrev = startStr > oldestDate;
  const hasNext = _weekOffset < 0;

  if (prevBtn) prevBtn.disabled = !hasPrev;
  if (nextBtn) nextBtn.disabled = !hasNext;

  if (label) {
    if (_weekOffset === 0) label.textContent = `This Week · ${startStr.slice(5)} – ${endStr.slice(5)}`;
    else label.textContent = `${startStr.slice(5)} – ${endStr.slice(5)}`;
  }

  const fullDaily = (window.ANALYTICS_STATE && Array.isArray(window.ANALYTICS_STATE.allDaily)) ? window.ANALYTICS_STATE.allDaily : [];
  const windowDays = fullDaily.filter(d => days.some(w => (w.date || w.day) === d.day));
  const modelKeys = (window.ANALYTICS_STATE?.windowModels || []).filter(m => windowDays.some(d => (d.models?.[m] || d.modelCosts?.[m])));
  const providersByModel = {};
  windowDays.forEach(d => Object.entries(d.modelProviders || {}).forEach(([k, v]) => { if (!providersByModel[k]) providersByModel[k] = v; }));

  _drawWeeklyStackedChart(dailyCanvas, windowDays, 'totalTokens', modelKeys, providersByModel, '.chart-legend');
  _drawWeeklyStackedChart(costCanvas, windowDays, 'totalCost', modelKeys, providersByModel, '.chart-cost-legend');
}

// Continue normal boot flow below (hotfix boot sequence)
async function bootstrapDashboard() {
  try { checkConnection(); } catch {}
  try { applyLanguageUI(); } catch {}
  try { initTabs(); } catch {}
  try { await refreshCapabilities(); } catch {}
  try { if (typeof loadCopilotStatus === 'function') await loadCopilotStatus(); } catch {}
  try { await loadAgentMonitor(); } catch {}
  try { await loadSessions(); } catch {}
  try { await loadCronEnhanced(); } catch {}
  try { await loadCronCosts(); } catch {}
  try {
    const range = (window.ANALYTICS_STATE && window.ANALYTICS_STATE.rangeDays) || 7;
    if (typeof loadOpsAlltime === 'function') await loadOpsAlltime(range);
    if (typeof loadOpsBySource === 'function') await loadOpsBySource(range);
    if (typeof renderAnalyticsDailyDetails === 'function') renderAnalyticsDailyDetails();
    if (typeof renderCostHeatmap === 'function') renderCostHeatmap();
    if (typeof renderSourceStackedChart === 'function' && window.ANALYTICS_STATE?.sourceDaily?.length) renderSourceStackedChart(window.ANALYTICS_STATE.sourceDaily);
  } catch (e) {
    console.error('analytics bootstrap failed', e);
  }
  try { await loadSystemInfo(); } catch {}
  try { await loadTasks(true); } catch {}
  try { pollWatchdogStatus(); } catch {}
}

bootstrapDashboard();
setInterval(checkConnection, 10000);
setInterval(pollWatchdogStatus, 10000);
