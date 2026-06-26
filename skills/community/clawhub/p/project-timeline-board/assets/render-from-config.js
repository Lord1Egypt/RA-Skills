/**
 * render-from-config.js — project-timeline 数据驱动渲染器
 *
 * 功能：从 window.PROJECT_CONFIG 读取数据，动态渲染页面的所有内容区域。
 * 依赖：本文件必须在 project-timeline.html 的 <script> 末尾引入，
 *       且 window.PROJECT_CONFIG 必须在引入前已加载。
 *
 * 渲染区域：
 * 1. Hero 区
 * 2. Overview 四宫格
 * 3. Key Nodes 节点列表
 * 4. Gantt 甘特图
 * 5. To-Do 待办清单
 * 6. Extras Callout
 *
 * 使用方法：
 * 1. 引入 project-timeline-data.js（项目数据）
 * 2. 引入 project-timeline.html（页面骨架 + CSS）
 * 3. 引入本文件（渲染逻辑）
 */
(function() {
'use strict';

var cfg = window.PROJECT_CONFIG || {};
var now = new Date();
var todayMonth = now.getMonth() + 1;
var todayDay   = now.getDate();

// ============================================================
// 工具函数
// ============================================================

/** 解析 data-date 属性，返回 {month, day} 或 null */
function parseDateAttr(attr) {
  if (!attr || attr === 'post') return null;
  var parts = attr.split('-');
  if (parts.length !== 2) return null;
  return { month: parseInt(parts[0], 10), day: parseInt(parts[1], 10) };
}

/** 判断 chip 状态：today / done / soon / later */
function chipState(subDate) {
  var parsed = parseDateAttr(subDate);
  if (!parsed) return 'later'; // 无日期默认 later
  var m = parsed.month, d = parsed.day;
  if (todayMonth === m && todayDay === d) return 'today';
  if (todayMonth > m || (todayMonth === m && todayDay > d)) return 'done';
  var target = new Date(now.getFullYear(), m - 1, d);
  var diff = Math.ceil((target - now) / 86400000);
  return diff <= 3 ? 'soon' : 'later';
}

/** 格式化日期字符串 */
function fmtDate(attr) {
  var parsed = parseDateAttr(attr);
  if (!parsed) return attr;
  return parsed.month + '.' + String(parsed.day).padStart(2, '0');
}

// ============================================================
// 1. Hero 区
// ============================================================
function renderHero() {
  var badge = document.querySelector('.hero-badge');
  if (badge) {
    badge.innerHTML = '<span class="dot"></span>' + (cfg.status || '进行中');
  }

  var h1 = document.querySelector('.hero h1');
  if (h1) {
    h1.innerHTML = cfg.projectName + ' 项目<em>时间线</em>';
  }

  var sub = document.querySelector('.hero-sub');
  if (sub) sub.textContent = cfg.projectSubtitle || '';

  var phase = document.querySelector('.hero > div[style*="rgba"]');
  if (phase) {
    phase.textContent = cfg.heroPhase || '';
  }

  var meta = document.querySelector('.hero-meta');
  if (meta) {
    meta.innerHTML =
      '<span>' + (cfg.startDate || '') + ' → ' + (cfg.endDate || '') + '</span>' +
      '<span>' + (cfg.totalWeeks || '') + ' 周</span>';
  }

  var footDate = document.getElementById('footDate');
  if (footDate) {
    footDate.textContent = (cfg.projectName || '项目') + ' 时间线 · 更新于 ' +
      now.getFullYear() + '.' + String(todayMonth).padStart(2,'0') + '.' +
      String(todayDay).padStart(2,'0');
  }
}

// ============================================================
// 2. Overview 四宫格
// ============================================================
function renderOverview() {
  var ov = document.querySelector('.ov');
  if (!ov || !cfg.overview) return;
  var colors = { blue:'var(--blue)', purple:'var(--purple)', cyan:'var(--cyan)', rose:'var(--rose)', green:'var(--green)', amber:'var(--amber)' };
  ov.innerHTML = cfg.overview.map(function(item) {
    return '<div class="ov-c"><div class="ov-v" style="color:' + (colors[item.color] || 'var(--text)') + '">' +
           item.date + '</div><div class="ov-l">' + item.label + '</div></div>';
  }).join('');
}

// ============================================================
// 3. Key Nodes
// ============================================================
function renderKeyNodes() {
  var track = document.querySelector('.kn-track');
  if (!track || !cfg.keyNodes) return;

  var dotColors  = { blue:'c-blue', purple:'c-purple', amber:'c-amber', green:'c-green', cyan:'c-cyan', rose:'c-rose' };
  var badgeColors = { blue:'b-blue', purple:'b-purple', amber:'b-amber', green:'b-green', cyan:'b-cyan', rose:'b-rose' };

  track.innerHTML = cfg.keyNodes.map(function(node) {
    var dotCls   = dotColors[node.color]   || 'c-blue';
    var badgeCls = badgeColors[node.color] || 'b-blue';
    var openCls  = node.open  ? ' open' : '';
    var activeCls = node.active ? ' active' : '';
    var dotStyle = node.active ? 'style="background:var(--' + (node.color === 'rose' ? 'rose' : node.color) + ');box-shadow:0 0 0 3px rgba(var(--' + node.color + '),.15)"' : '';

    var detailsHtml = '';
    if (node.detail && node.detail.length) {
      detailsHtml = '<div class="kn-detail' + openCls + '"><div class="kn-detail-inner">' +
        node.detail.map(function(sub) {
          var cs = chipState(sub.subDate);
          var label = sub.subDate === 'post' ? sub.subLabel : fmtDate(sub.subDate) + (cs === 'done' ? ' ✓' : '');
          return '<div class="kn-row"><span class="kn-row-name">' + sub.subLabel + '</span>' +
                 '<span class="kn-chip ' + cs + '">' + label + '</span></div>';
        }).join('') + '</div></div>';
    }

    var arrow = detailsHtml ? '<span class="kn-arrow">▾</span>' : '';

    return '<div class="kn' + openCls + '" onclick="this.classList.toggle(\'open\')">' +
      '<div class="kn-dot ' + dotCls + '"></div>' +
      '<div class="kn-card">' +
        '<div class="kn-head kn-toggle">' +
          '<div class="kn-left">' +
            '<div class="kn-date ' + dotCls + '">' + node.date + '</div>' +
            '<div class="kn-info">' +
              '<div class="kn-title">' + node.title + ' ' + arrow + '</div>' +
              '<div class="kn-sub">' + node.subtitle + '</div>' +
            '</div>' +
          '</div>' +
          '<span class="kn-badge ' + badgeCls + '">' + node.badge + '</span>' +
        '</div>' +
        detailsHtml +
      '</div>' +
    '</div>';
  }).join('');

  // 给最后一个 dot 添加特殊样式（rose 色）
  var dots = track.querySelectorAll('.kn:last-child .kn-dot');
  dots.forEach(function(dot) {
    dot.style.cssText = 'background:var(--rose);box-shadow:0 0 0 3px rgba(233,69,96,.15)';
  });
}

// ============================================================
// 4. Gantt 甘特图
// ============================================================
function renderGantt() {
  var ganttDates = document.getElementById('ganttDates');
  var ganttBody  = document.getElementById('ganttBody');
  if (!ganttDates || !ganttBody || !(cfg.gantt || cfg.ganttData)) return;

  var S = cfg.ganttStart || 7;
  var E = cfg.ganttEnd   || 22;
  var cols = E - S + 1;
  var TODAY = (todayMonth === 4 && todayDay >= S && todayDay <= E) ? todayDay : -1;
  var monthLabel = (now.getMonth() + 1) + '.';

  // 表头
  ganttDates.innerHTML = '';
  for (var d = S; d <= E; d++) {
    var el = document.createElement('div');
    el.className = 'd' + (d === TODAY ? ' today' : '');
    el.textContent = d === S ? monthLabel + d : d;
    ganttDates.appendChild(el);
  }

  // 甘特条
  ganttBody.innerHTML = '';
  var tp = TODAY > 0 ? ((TODAY - S + 0.5) / cols) * 100 : -10;
  var colorMap = cfg.ganttColorMap || { ix:{cls:'ix',label:'交互'}, vis:{cls:'vis',label:'视觉'}, tool:{cls:'tool',label:'工具'} };

  (cfg.gantt || cfg.ganttData || []).forEach(function(row) {
    var label = row[0];
    var bars   = row[1] || [];
    var r = document.createElement('div');
    r.className = 'gantt-row';
    r.innerHTML = '<div class="gantt-rl">' + label + '</div>' +
                  '<div class="gantt-rb"><div class="gantt-tl" style="left:' + tp + '%"></div></div>';
    var rb = r.querySelector('.gantt-rb');
    bars.forEach(function(b) {
      var info = colorMap[b.t] || { cls: b.t, label: b.t };
      var left = ((b.f - S) / cols) * 100;
      var w    = ((b.to - b.f + 1) / cols) * 100;
      var bar  = document.createElement('div');
      bar.className = 'gantt-bar ' + info.cls;
      bar.style.cssText = 'left:' + left.toFixed(2) + '%;width:' + w.toFixed(2) + '%';
      bar.textContent = info.label;
      rb.appendChild(bar);
    });
    ganttBody.appendChild(r);
  });
}

// ============================================================
// 5. To-Do 列表
// ============================================================
function renderTodos() {
  var container = document.querySelector('.container');
  if (!container || !cfg.todos) return;

  var todosSection = document.getElementById('todos');
  if (!todosSection) return;

  var tagLabels = { ix:'交互', vis:'视觉', plan:'规划', collab:'协作', tool:'工具', fe:'前端', be:'后端', test:'测试' };

  todosSection.innerHTML =
    '<div class="sl">03 — To-Do</div>' +
    '<div class="st">待办事项</div>' +
    '<div class="sd">点击切换完成状态。</div>' +
    cfg.todos.map(function(group) {
      return '<div class="todo-g">' +
        '<div class="todo-gh"><span class="todo-gl">' + group.period + '</span><span class="todo-gc">' + group.count + '项</span></div>' +
        '<ul class="todo-ul">' +
          group.items.map(function(item) {
            return '<li class="todo-li' + (item.done ? ' done' : '') + '" onclick="this.classList.toggle(\'done\')">' +
                   '<div class="todo-ck">✓</div><div class="todo-tx">' + item.text + '</div>' +
                   '<span class="todo-tg ' + item.tag + '">' + (tagLabels[item.tag] || item.tag) + '</span></li>';
          }).join('') +
        '</ul></div>';
    }).join('');
}

// ============================================================
// 6. Extras Callout（支持任意数量和名称的 card）
// ============================================================
function renderExtras() {
  var extrasSection = document.getElementById('extra');
  if (!extrasSection || !cfg.extras) return;

  // 支持任意 key 的 card，自动识别 type 字段
  var cards = Object.keys(cfg.extras).map(function(key) {
    var card = cfg.extras[key];
    var cls = card.type || '';
    return '<div class="co ' + cls + '"><div class="co-t">' + card.label + '</div><div class="co-b">' + card.content + '</div></div>';
  }).join('');

  extrasSection.innerHTML =
    '<div class="sl">04 — Extras</div>' +
    '<div class="st">关注事项</div>' +
    '<div class="co-grid">' + cards + '</div>';
}

// ============================================================
// 7. 滚动进度条 + 入场动画
// ============================================================
function renderScrollBehavior() {
  // 滚动进度条
  var sp = document.getElementById('sp');
  if (sp) {
    window.addEventListener('scroll', function() {
      var h = document.documentElement;
      sp.style.width = (h.scrollTop / (h.scrollHeight - h.clientHeight)) * 100 + '%';
    });
  }

  // 入场动画
  var obs = new IntersectionObserver(function(es) {
    es.forEach(function(e) {
      if (e.isIntersecting) e.target.style.animationPlayState = 'running';
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.anim').forEach(function(el) {
    el.style.animationPlayState = 'paused';
    obs.observe(el);
  });
}

// ============================================================
// 统一入口
// ============================================================
function render() {
  if (!cfg.projectName) {
    console.warn('[render-from-config] window.PROJECT_CONFIG 未设置或为空，将保留 HTML 原始内容。');
    return;
  }
  renderHero();
  renderOverview();
  renderKeyNodes();
  renderGantt();
  renderTodos();
  renderExtras();
  renderScrollBehavior();
}

// 自动执行（页面加载完成后）
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', render);
} else {
  render();
}

// 暴露给全局以便手动调用
window.renderProjectTimeline = render;

})();
