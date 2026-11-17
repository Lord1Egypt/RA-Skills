/* 多科目智能复习题库 - 主程序 v3
   纯前端实现，不依赖任何在线服务。
   v3 新增：科目图标、首页统计条形图、今日复习模态浮层、错题/收藏全科目、日历日详情、主题色预设。 */
(function () {
  'use strict';

  var BANK = null;
  var QMAP = {};
  var TYPE_LABEL = { single: '单选题', multiple: '多选题', judge: '判断题', blank: '填空题', short: '简答题' };
  var TYPE_ORDER = ['single', 'multiple', 'judge', 'blank', 'short'];
  var DIFF_LABEL = { 1: '基础', 2: '进阶', 3: '挑战' };
  var POOL_LABEL = { all: '全部题目', wrong: '错题', fav: '收藏题', fresh: '新题', due: '仅到期复习题' };
  var DAILY_MODAL_ORDER = ['subject', 'global', 'off'];
  var DAILY_MODAL_LABEL = { subject: '每科每日', global: '全局每日', off: '关闭自动弹出' };
  var DAILY_MODAL_DESC = {
    subject: '同一科目当天只弹出一次',
    global: '所有科目加起来一天只弹一次',
    off: '完全不自动弹出，科目页保留手动入口'
  };
  var PACE_ORDER = ['steady', 'normal', 'fast'];
  var PACE_LABEL = { steady: '稳扎稳打', normal: '标准', fast: '快速推进' };
  var PACE_DESC = {
    steady: '间隔缩短约 20%，复习更勤，适合考前冲刺或记忆易衰退的内容',
    normal: '按遗忘曲线的标准节奏排程，兼顾牢固度与效率',
    fast: '间隔拉长约 30%，每日题量更少，适合已经比较熟的内容'
  };

  /* 图标库（线性 SVG，与导航图标风格一致） */
  /* 科目图标库：题库 JSON 里 subjects[].icon / meta.brandIcon 填下列任一 key。
     未命中时自动回退 book。全部为 24×24 线性图标，跟随文字颜色。 */
  var ICONS = {
    book: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h11a2 2 0 0 1 2 2v14a2 2 0 0 0 2-2H4z"/><path d="M20 4h-4v16h4a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"/></svg>',
    pill: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.5 3.5l10 10a4.95 4.95 0 0 1-7 7l-10-10a4.95 4.95 0 0 1 7-7z"/><line x1="7.5" y1="7.5" x2="16.5" y2="16.5"/></svg>',
    leaf: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 4 13C4 8 8 4 20 4c0 9-4 16-9 16z"/><path d="M9 15c2-3 5-5 8-6"/></svg>',
    sprout: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22V10"/><path d="M12 10C12 7 9 4 4 4c0 4 3 6 8 6z"/><path d="M12 10c0-3 3-6 8-6 0 4-3 6-8 6z"/></svg>',
    flask: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6"/><path d="M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/><path d="M7.5 15h9"/></svg>',
    brain: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5a3 3 0 0 0-6 0 3 3 0 0 0-2 5.2A3 3 0 0 0 6 16a3 3 0 0 0 6 1.5z"/><path d="M12 5a3 3 0 0 1 6 0 3 3 0 0 1 2 5.2A3 3 0 0 1 18 16a3 3 0 0 1-6 1.5z"/><path d="M12 5v14.5"/></svg>',
    code: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/><line x1="14" y1="4" x2="10" y2="20"/></svg>',
    sigma: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 5H6l6 7-6 7h12"/></svg>',
    scale: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><path d="M6 21h12"/><path d="M3 8h18"/><path d="M6 8l-3 6a3 3 0 0 0 6 0z"/><path d="M18 8l-3 6a3 3 0 0 0 6 0z"/></svg>',
    globe: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18z"/></svg>',
    language: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 5h11"/><path d="M8 3v2"/><path d="M11 5c0 5-3.5 9-8 10"/><path d="M6 11c1.5 2.5 4 4.5 7 5.5"/><path d="M13 21l4.5-11L22 21"/><path d="M15 17h5"/></svg>',
    atom: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="2"/><ellipse cx="12" cy="12" rx="10" ry="4.5"/><ellipse cx="12" cy="12" rx="10" ry="4.5" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4.5" transform="rotate(120 12 12)"/></svg>',
    heart: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 1 0-7.1 7.1L12 21.4l8.8-8.7a5 5 0 0 0 0-7.1z"/></svg>',
    chart: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="21" x2="21" y2="21"/><rect x="5" y="11" width="4" height="8"/><rect x="11" y="6" width="4" height="13"/><rect x="17" y="14" width="4" height="5"/></svg>',
    scroll: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h11a2 2 0 0 1 2 2v13a3 3 0 0 0 3 3H8a3 3 0 0 1-3-3V6"/><path d="M5 6a2 2 0 1 1-2-2h2"/><path d="M9 8h7"/><path d="M9 12h7"/></svg>',
    cpu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="12" height="12" rx="1"/><rect x="10" y="10" width="4" height="4"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/></svg>',
    palette: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a9 9 0 1 0 0 18c1.1 0 2-.9 2-2 0-.5-.2-1-.5-1.3-.3-.4-.5-.8-.5-1.2 0-1 .9-1.5 2-1.5h1.5A4.5 4.5 0 0 0 21 10.5C21 6.4 16.9 3 12 3z"/><circle cx="7.5" cy="10.5" r="1"/><circle cx="12" cy="7.5" r="1"/><circle cx="16.5" cy="10.5" r="1"/></svg>',
    music: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/></svg>',
    briefcase: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><path d="M2 13h20"/></svg>',
    compass: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polygon points="16 8 14 14 8 16 10 10 16 8"/></svg>'
  };

  var ctx = { subject: null, listKind: null, backView: 'home' };
  var session = null;

  /* ---------------- 动效（集中收口；无 GSAP / 关闭动效 / 系统减弱动态时静默降级） ---------------- */
  var Motion = (function () {
    var g = (typeof window !== 'undefined') && window.gsap;
    function enabled() {
      if (!g) return false;                       // jsdom 或加载失败 → 降级
      try { if (Store.getMotion() !== true) return false; } catch (e) {}
      try {
        if (window.matchMedia &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches) return false;
      } catch (e) {}
      return true;
    }
    function safe(fn) { try { fn(); } catch (e) {} }
    function reset(el) { safe(function () { if (el && el.style) { el.style.opacity = ''; el.style.transform = ''; } }); }
    return {
      enabled: enabled,
      viewIn: function (el) {
        if (!enabled() || !el) return;
        safe(function () {
          g.fromTo(el, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.4, ease: 'power3.out', clearProps: 'transform' });
        });
        if (!g) reset(el);
      },
      stagger: function (nodes) {
        if (!enabled() || !nodes || !nodes.length) return;
        safe(function () {
          g.fromTo(nodes, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.42, ease: 'power3.out', stagger: 0.05, clearProps: 'transform' });
        });
      },
      modalIn: function (overlay) {
        if (!overlay) return;
        if (!enabled()) { overlay.hidden = false; return; }
        var box = overlay.querySelector('.modal-box');
        overlay.hidden = false;
        safe(function () {
          g.fromTo(overlay, { opacity: 0 }, { opacity: 1, duration: 0.2, ease: 'power2.out' });
          if (box) g.fromTo(box, { opacity: 0, y: 12, scale: 0.98 }, { opacity: 1, y: 0, scale: 1, duration: 0.34, ease: 'power3.out', clearProps: 'transform' });
        });
      },
      modalOut: function (overlay, done) {
        if (!overlay) { if (done) done(); return; }
        if (!enabled()) { overlay.hidden = true; if (done) done(); return; }
        var box = overlay.querySelector('.modal-box');
        try {
          if (box) g.to(box, { opacity: 0, y: 8, scale: 0.99, duration: 0.2, ease: 'power2.in' });
          g.to(overlay, { opacity: 0, duration: 0.22, ease: 'power2.in', onComplete: function () { overlay.hidden = true; if (done) done(); } });
        } catch (e) { overlay.hidden = true; if (done) done(); }
      },
      answerCorrect: function (el) {
        if (!enabled() || !el) return;
        safe(function () {
          g.fromTo(el, { opacity: 0.4, scale: 0.98 }, { opacity: 1, scale: 1, duration: 0.34, ease: 'power3.out', clearProps: 'transform' });
        });
      },
      answerWrong: function (el) {
        if (!enabled() || !el) return;
        safe(function () {
          g.fromTo(el, { x: -6 }, { x: 6, duration: 0.08, repeat: 3, yoyo: true, ease: 'sine.inOut',
            onComplete: function () { reset(el); } });
        });
      },
      countUp: function (el, to, suffix) {
        if (!enabled() || !el) return;            // 禁用时 HTML 已是最终值
        var raw = el.getAttribute('data-num');
        var t = (typeof to === 'number' && !isNaN(to)) ? to : (parseFloat(raw) || 0);
        var s = (typeof suffix === 'string') ? suffix : (/%$/.test(raw || '') ? '%' : '');
        var final = Math.round(t) + s;
        try {
          el.textContent = '0' + s;
          var o = { v: 0 };
          g.to(o, { v: t, duration: 0.62, ease: 'power2.out',
            onUpdate: function () { el.textContent = Math.round(o.v) + s; },
            onComplete: function () { el.textContent = final; } });
        } catch (e) { el.textContent = final; }
      },
      growBars: function (nodes) {
        if (!enabled() || !nodes) return;
        var arr = (nodes.length !== undefined && nodes.forEach) ? nodes : [nodes];
        arr.forEach(function (el) {
          if (!el) return;
          var target = el.getAttribute('data-w') || el.style.width || '0%';
          try {
            el.style.width = '0%';
            g.to(el, { width: target, duration: 0.62, ease: 'power2.out', delay: 0.05 });
          } catch (e) { el.style.width = target; }
        });
      },
      expand: function (el) {
        if (!enabled() || !el) return;
        safe(function () {
          g.fromTo(el, { opacity: 0, y: -8 }, { opacity: 1, y: 0, duration: 0.36, ease: 'power3.out', clearProps: 'transform' });
        });
      },
      collapse: function (el, done) {
        if (!el) { if (done) done(); return; }
        if (!enabled()) { if (done) done(); return; }
        safe(function () {
          g.to(el, { opacity: 0, height: 0, duration: 0.2, ease: 'power2.in', onComplete: function () { if (done) done(); } });
        });
      }
    };
  })();

  /* ---------------- 工具 ---------------- */
  function $(id) { return document.getElementById(id); }
  function esc(s) {
    return String(s === undefined || s === null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function pct(n, d) { return d ? Math.round(n * 100 / d) + '%' : '0%'; }
  function fmtTime(ts) {
    var d = new Date(ts);
    function p(x) { return x < 10 ? '0' + x : '' + x; }
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
  }
  function normalize(s) {
    return String(s || '')
      .toLowerCase()
      .replace(/\s+/g, '')
      .replace(/[《》（）()【】\[\]。，,、；;：:！!？?"'""·．.\-—_]/g, '');
  }

  /* ---------------- 视图切换 ---------------- */
  function show(view) {
    var list = document.querySelectorAll('.view');
    for (var i = 0; i < list.length; i++) list[i].classList.remove('active');
    if (view === 'stats') renderStatsPage();
    var el = $('view-' + view);
    if (el) el.classList.add('active');
    var modal = $('dailyModal');
    if (modal) modal.hidden = true;
    window.scrollTo(0, 0);
    updateNavActive(view);
    if (el) Motion.viewIn(el);
  }
  function setCrumb(text) { $('crumb').textContent = text || ''; }

  function updateNavActive(view) {
    document.querySelectorAll('.nav-icon').forEach(function (el) { el.classList.remove('active'); });
    if (view === 'settings') $('navSettings').classList.add('active');
    else if (view === 'calendar') $('navCalendar').classList.add('active');
    else if (view === 'stats') $('navStats').classList.add('active');
    else if (view === 'list') {
      if (ctx.listKind === 'wrong') $('navWrong').classList.add('active');
      if (ctx.listKind === 'fav') $('navFav').classList.add('active');
    }
  }

  /* ---------------- 数据检索 ---------------- */
  function subjectQuestions(name) {
    return BANK.questions.filter(function (q) { return q.subject === name; });
  }
  function subjectMeta(name) {
    for (var i = 0; i < BANK.subjects.length; i++) if (BANK.subjects[i].name === name) return BANK.subjects[i];
    return { name: name, desc: '', chapters: [] };
  }
  function allChapters() {
    var s = [];
    BANK.questions.forEach(function (q) { if (s.indexOf(q.chapter) < 0) s.push(q.chapter); });
    return s;
  }
  function statsOf(qs) {
    var s = { total: qs.length, practiced: 0, correct: 0, seen: 0, due: 0, wrong: 0, fav: 0 };
    qs.forEach(function (q) {
      var r = Store.rec(q.id);
      if (r.seen) { s.practiced++; s.correct += r.correct; s.seen += r.seen; }
      if (SRS.isDue(r)) s.due++;
      if (r.everWrong && !r.mastered) s.wrong++;
      if (r.fav) s.fav++;
    });
    s.rate = pct(s.correct, s.seen);
    return s;
  }

  /* ---------------- 判题 ---------------- */
  function answerText(q) {
    if (q.type === 'single') { var o = findOpt(q, q.answer); return q.answer + '. ' + (o ? o.text : ''); }
    if (q.type === 'multiple') {
      return q.answer.map(function (k) { var op = findOpt(q, k); return k + '. ' + (op ? op.text : ''); }).join('\n');
    }
    if (q.type === 'judge') return q.answer === 'T' ? '正确' : '错误';
    if (q.type === 'blank') {
      return q.answer.map(function (b, i) { return '第' + (i + 1) + '空：' + b.accept[0]; }).join('；');
    }
    return q.answer;
  }
  function findOpt(q, key) {
    for (var i = 0; i < (q.options || []).length; i++) if (q.options[i].key === key) return q.options[i];
    return null;
  }
  function userAnswerText(q, ua) {
    if (ua === undefined || ua === null || ua === '' || (Array.isArray(ua) && !ua.length)) return '（未作答）';
    if (q.type === 'single') return ua;
    if (q.type === 'multiple') return ua.slice().sort().join('、');
    if (q.type === 'judge') return ua === 'T' ? '正确' : '错误';
    if (q.type === 'blank') return ua.map(function (v, i) { return '第' + (i + 1) + '空：' + (v || '（空）'); }).join('；');
    return ua;
  }
  function judgeObjective(q, ua) {
    if (ua === undefined || ua === null) return false;
    if (q.type === 'single' || q.type === 'judge') return ua === q.answer;
    if (q.type === 'multiple') {
      if (!Array.isArray(ua) || ua.length !== q.answer.length) return false;
      var a = ua.slice().sort().join(','), b = q.answer.slice().sort().join(',');
      return a === b;
    }
    if (q.type === 'blank') {
      if (!Array.isArray(ua)) return false;
      var vals = ua.map(normalize);
      if (q.unordered) {
        var pool = vals.slice();
        return q.answer.every(function (blk) {
          for (var i = 0; i < pool.length; i++) { if (matchBlank(blk, pool[i])) { pool.splice(i, 1); return true; } }
          return false;
        });
      }
      return q.answer.every(function (blk, i) { return matchBlank(blk, vals[i]); });
    }
    return false;
  }
  function matchBlank(blk, val) {
    if (!val) return false;
    return blk.accept.some(function (a) { return normalize(a) === val; });
  }
  function keywordHits(q, text) {
    var t = normalize(text);
    var hits = [];
    (q.keywords || []).forEach(function (k) { if (t && t.indexOf(normalize(k)) >= 0) hits.push(k); });
    return hits;
  }

  /* ---------------- 记录提交 ---------------- */
  function commitGrade(qid, grade, right) {
    var g = session.graded[qid];
    var rec = Store.recW(qid);
    if (g.appliedWith) {
      rec.seen = Math.max(0, rec.seen - 1);
      if (g.appliedWith.right) rec.correct = Math.max(0, rec.correct - 1);
      else rec.wrong = Math.max(0, rec.wrong - 1);
      rec.everWrong = g.snapshot.everWrong;
      rec.mastered = g.snapshot.mastered;
      rec.stage = g.snapshot.stage;
      rec.interval = g.snapshot.interval;
      rec.due = g.snapshot.due;
      rec.lastAt = g.snapshot.lastAt;
      rec.lastResult = g.snapshot.lastResult;
    } else {
      g.snapshot = {
        everWrong: rec.everWrong, mastered: rec.mastered, stage: rec.stage,
        interval: rec.interval, due: rec.due, lastAt: rec.lastAt, lastResult: rec.lastResult
      };
    }
    SRS.apply(rec, grade, right);
    g.appliedWith = { grade: grade, right: right };
    g.grade = grade;
    g.right = right;
    Store.commit();
  }

  /* ==================== 首页 ==================== */
  function renderHome() {
    ctx.subject = null;
    ctx.backView = 'home';
    setCrumb('');
    var all = statsOf(BANK.questions);
    // 问候卡片（Hero 区）
    renderGreeting();
    // 科目卡片（图标在上 / 名称居中 / 进度小字在下）
    var html = '';
    BANK.subjects.forEach(function (s) {
      var st = statsOf(subjectQuestions(s.name));
      var icon = ICONS[s.icon] || ICONS.book;
      html += '<div class="card subject-card" data-subject="' + esc(s.name) + '">'
        + '<span class="subject-icon">' + icon + '</span>'
        + '<h3>' + esc(s.name) + '</h3>'
        + '<div class="subject-progress">' + st.total + ' 题 · 待复习 <b>' + st.due + '</b> · 正确率 <b>' + st.rate + '</b></div>'
        + '</div>';
    });
    $('subjectGrid').innerHTML = html || '<div class="empty"><div class="t">暂无科目</div><div class="d">题库中没有可用科目。</div></div>';
    // 首页学习数据区（替代旧的统计面板）
    renderHomeDataSection(all);
    Motion.stagger($('subjectGrid').querySelectorAll('.subject-card'));
    $('storageNotice').hidden = Store.isAvailable();
    show('home');
  }

  /* 问候卡片（根据时段显示太阳/月亮 + 情感文案 + 今日简报） */
  function getGreeting() {
    var h = new Date().getHours();
    if (h >= 5 && h < 12) return { badge: '上午好', text: '准备好开始今天的学习了吗？', sub: '保持节奏，每一步都算数。', icon: 'sun' };
    if (h >= 12 && h < 14) return { badge: '中午好', text: '午休过后，来几道题提提神？', sub: '短暂休息也是积累的一部分。', icon: 'sun' };
    if (h >= 14 && h < 18) return { badge: '下午好', text: '下午的专注力，值得用来挑战自己。', sub: '循序渐进，稳扎稳打。', icon: 'sun' };
    if (h >= 18 && h < 22) return { badge: '晚上好', text: '今晚的目标是什么？', sub: '夜晚安静，适合深度思考。', icon: 'moon' };
    return { badge: '夜深了', text: '还在坚持，这份毅力很珍贵。', sub: '注意休息，别太累了。', icon: 'moon' };
  }
  function renderGreeting() {
    var g = getGreeting();
    $('greetingBadge').textContent = g.badge;
    $('greetingText').textContent = g.text;
    $('greetingSub').innerHTML = '<em class="em">' + esc(g.sub) + '</em>';

    var visual = $('greetingVisual');
    if (g.icon === 'sun') {
      visual.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>';
      visual.style.color = 'var(--warn)';
    } else {
      visual.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
      visual.style.color = 'var(--accent)';
    }

    var today = Store.todayKey();
    var ci = Store.getCheckin(today) || {};
    var target = Store.getDailyTarget() || 10;
    $('greetingStats').innerHTML =
      '<span>今日已练 <b>' + (ci.count || 0) + '</b> 题</span>'
      + '<span>目标 <b>' + target + '</b> 题</span>'
      + '<span>连续打卡 <b>' + currentStreak() + '</b> 天</span>';

    Motion.stagger($('greetingCard').querySelectorAll('.greeting-badge, .greeting-body, .greeting-stats'));
  }

  /* 首页学习数据区（大数字总览 + 2×2 简要统计，可折叠隐藏，点击详情跳转统计页） */
  function renderHomeDataSection(all) {
    var heroHtml = '<div class="stats-hero-mini">'
      + '<span class="big-num" data-num="' + all.total + '">' + esc(all.total) + '</span>'
      + '<span class="unit">题</span>'
      + '<button class="btn primary small cta-btn" data-go="stats">去刷题</button>'
      + '</div>';

    var mini = [
      ['icon-ok', '✓', '已完成', all.practiced],
      ['icon-err', '✗', '错题', all.wrong],
      ['icon-accent', '%', '正确率', all.rate],
      ['icon-warn', '★', '收藏', all.fav]
    ];
    var gridHtml = '<div class="stats-mini-grid">';
    mini.forEach(function (c) {
      gridHtml += '<div class="stats-mini-card">'
        + '<div class="stats-mini-icon ' + c[0] + '">' + c[1] + '</div>'
        + '<div class="stats-mini-info"><div class="stats-mini-label">' + c[2] + '</div>'
        + '<div class="stats-mini-num">' + esc(c[3]) + '</div></div></div>';
    });
    gridHtml += '</div>';

    $('homeDataBody').innerHTML = heroHtml + gridHtml;
    $('homeDataLink').onclick = function () { show('stats'); };

    if (Motion.enabled()) Motion.countUp($('homeDataBody').querySelector('.big-num'), all.total);
  }

  function ov(pairs) {
    return pairs.map(function (p) {
      return '<div><div class="num" data-num="' + esc(p[1]) + '">' + esc(p[1]) + '</div><div class="lbl">' + esc(p[0]) + '</div></div>';
    }).join('');
  }

  /* ==================== 科目主页（今日复习改为模态浮层） ==================== */
  function renderSubject(name) {
    ctx.subject = name;
    ctx.backView = 'subject';
    var st = statsOf(subjectQuestions(name));
    setCrumb(name);
    $('subjectTitle').textContent = name;

    var entries = [
      ['free', '自由练习', '自选模式与题量'],
      ['wrong', '错题本', '共 ' + st.wrong + ' 道待巩固错题'],
      ['fav', '收藏夹', '共 ' + st.fav + ' 道收藏题'],
      ['stats', '学习统计', '查看本科目的练习情况']
    ];
    $('subjectEntries').innerHTML = entries.map(function (e) {
      return '<div class="entry" data-entry="' + e[0] + '"><div class="t">' + esc(e[1]) + '</div><div class="d">' + esc(e[2]) + '</div></div>';
    }).join('');

    renderDailyHint(name);

    show('subject');

    // 自动弹出今日复习模态（受频率设置控制：每科每日 / 全局每日 / 关闭）
    if (Store.shouldShowDailyModal(name)) showDailyModal(name);
  }

  /* 科目页顶部「今日复习」迷你卡片入口：始终可见（除非手动关闭），跳过模态后保留入口 */
  function renderDailyHint(name) {
    var g = pickDaily(name);
    var totalDue = g.due.length + g.wrong.length + g.fav.length;
    var hint = $('dailyHint');
    if (totalDue > 0 || g.fresh.length > 0) {
      var suggest = totalDue > 0 ? Math.min(totalDue + Math.min(5, g.fresh.length), 40) : Math.min(10, g.fresh.length);
      $('dailyHintText').innerHTML = '今日复习待完成 · ' + esc(name) + '（<b>' + Math.max(1, suggest) + '</b> 题）';
      $('dailyHintStart').onclick = function () { hint.hidden = true; renderDaily(); };
      $('dailyHintClose').onclick = function () { hint.hidden = true; };
      hint.hidden = false;
    } else {
      hint.hidden = true;
    }
  }

  /* 今日复习模态浮层（含随机样题预览） */
  function showDailyModal(name) {
    var g = pickDaily(name);
    var totalDue = g.due.length + g.wrong.length + g.fav.length;
    var modal = $('dailyModal');
    var title = $('dailyModalTitle'), desc = $('dailyModalDesc');
    var sampleBox = $('dailySample');
    var startBtn = $('dailyModalStart'), skipBtn = $('dailyModalSkip');

    // 随机抽一道推荐题作为预览：题型标签 + 题干（截断）
    var pool = [].concat(g.due, g.wrong, g.fav, g.fresh);
    if (pool.length) {
      var sample = pool[Math.floor(Math.random() * pool.length)];
      var stemPreview = sample.stem.length > 84 ? sample.stem.slice(0, 84) + '…' : sample.stem;
      sampleBox.innerHTML = '<span class="daily-sample-tag">' + TYPE_LABEL[sample.type] + '</span>'
        + '<div class="daily-sample-stem">' + esc(stemPreview) + '</div>';
      sampleBox.hidden = false;
    } else {
      sampleBox.hidden = true;
    }

    if (totalDue > 0 || g.fresh.length > 0) {
      var suggest = totalDue > 0 ? Math.min(totalDue + Math.min(5, g.fresh.length), 40) : Math.min(10, g.fresh.length);
      title.textContent = '今日复习推荐';
      desc.innerHTML = '「' + esc(name) + '」今天有 <b>' + totalDue + '</b> 道题值得再看'
        + (g.fresh.length ? '，另有 <b>' + g.fresh.length + '</b> 道新题。' : '。') + '<br>建议练习 <b>' + Math.max(1, suggest) + '</b> 题。';
      startBtn.textContent = '开始今日复习（' + Math.max(1, suggest) + ' 题）';
      startBtn.onclick = function () {
        modal.hidden = true;
        Store.dismissDailyModal(name);
        var mode = Store.getDefaultMode();
        var list = [].concat(shuffle(g.due), shuffle(g.wrong), shuffle(g.fav), shuffle(g.fresh)).slice(0, Math.max(1, suggest));
        if (list.length) startSession(list, mode, 'daily');
      };
    } else {
      title.textContent = '今日无需复习';
      desc.innerHTML = '「' + esc(name) + '」的题目都已安排在更晚的时间复习，可以先做新题或自由练习。';
      startBtn.textContent = '练习新题';
      startBtn.onclick = function () {
        modal.hidden = true;
        Store.dismissDailyModal(name);
        var mode = Store.getDefaultMode();
        var list = shuffle(g.fresh).slice(0, Math.min(10, g.fresh.length));
        if (list.length) startSession(list, mode, 'daily');
      };
    }
    skipBtn.onclick = function () {
      Motion.modalOut(modal);
      Store.dismissDailyModal(name);
    };
    Motion.modalIn(modal);
  }

  /* ==================== 今日复习（独立视图，仍可从入口进入） ==================== */
  function pickDaily(name) {
    var qs = subjectQuestions(name);
    var due = [], wrong = [], fav = [], fresh = [];
    qs.forEach(function (q) {
      var r = Store.rec(q.id);
      if (SRS.isDue(r)) due.push(q);
      else if (r.everWrong && !r.mastered) wrong.push(q);
      else if (r.fav) fav.push(q);
      else if (!r.seen) fresh.push(q);
    });
    return { due: due, wrong: wrong, fav: fav, fresh: fresh };
  }
  function renderDaily() {
    var name = ctx.subject;
    if (!name) { renderHome(); return; }
    setCrumb(name + ' / 今日复习');
    var g = pickDaily(name);
    var base = g.due.length + g.wrong.length + g.fav.length;
    var suggest = base > 0 ? Math.min(base + Math.min(5, g.fresh.length), 40) : Math.min(10, g.fresh.length);
    $('dailyLead').textContent = base > 0
      ? '有 ' + base + ' 道题今天值得再看一遍，另有 ' + g.fresh.length + ' 道尚未练习。'
      : (g.fresh.length > 0 ? '今天没有到期需要复习的题目，可以先练习新题。' : '今天没有需要复习的题目。');

    if (base + g.fresh.length === 0) {
      $('dailyBody').innerHTML = '<div class="empty"><div class="t">今日无待复习题</div>'
        + '<div class="d">该科目的题目都已安排在更晚的时间复习。</div></div>'
        + '<div class="btn-row"><button class="btn" data-go="subject" type="button">返回科目</button>'
        + '<button class="btn" data-go="free" type="button">去自由练习</button></div>';
      show('daily');
      return;
    }
    $('dailyBody').innerHTML =
      '<div class="card">'
      + '<div class="kv" style="margin-bottom:14px">'
      + '<span>已到期 <b>' + g.due.length + '</b></span>'
      + '<span>曾经答错 <b>' + g.wrong.length + '</b></span>'
      + '<span>收藏题 <b>' + g.fav.length + '</b></span>'
      + '<span>尚未练习 <b>' + g.fresh.length + '</b></span>'
      + '</div>'
      + '<div class="form-row" style="margin-bottom:8px"><label class="field-label" for="dailyCount">本次题量</label>'
      + '<input type="number" id="dailyCount" min="1" max="100" value="' + Math.max(1, suggest) + '"></div>'
      + '<div class="form-row" style="margin-bottom:0"><label class="field-label">作答方式</label>'
      + '<div class="chips" id="dailyMode">'
      + '<span class="chip on" data-mode="instant">单题模式</span>'
      + '<span class="chip" data-mode="batch">连续答题</span></div></div>'
      + '</div>'
      + '<div class="btn-row"><button class="btn primary" id="dailyStart" type="button">开始今日复习</button>'
      + '<button class="btn" data-go="subject" type="button">返回科目</button></div>';

    bindChips($('dailyMode'), false);
    $('dailyStart').onclick = function () {
      var n = parseInt($('dailyCount').value, 10) || 1;
      var mode = $('dailyMode').querySelector('.chip.on').getAttribute('data-mode');
      var list = [].concat(shuffle(g.due), shuffle(g.wrong), shuffle(g.fav), shuffle(g.fresh)).slice(0, n);
      if (list.length) startSession(list, mode, 'daily');
    };
    show('daily');
  }

  /* ==================== 自由练习（重新设计） ==================== */
  var setupSelectedMode = 'instant';

  function renderSetup() {
    var name = ctx.subject;
    setCrumb(name + ' / 自由练习');

    var defMode = Store.getDefaultMode();
    setupSelectedMode = defMode;
    $('modeButtons').innerHTML =
      '<div class="mode-btn' + (defMode === 'instant' ? ' selected' : '') + '" data-mode="instant">'
      + '<span class="mode-name">单题模式</span>'
      + '<span class="mode-desc">逐题作答，提交后立即看解析</span></div>'
      + '<div class="mode-btn' + (defMode !== 'instant' ? ' selected' : '') + '" data-mode="batch">'
      + '<span class="mode-name">连续答题</span>'
      + '<span class="mode-desc">所有题目一页展示，做完一键对答案</span></div>';

    $('modeButtons').onclick = function (e) {
      var btn = e.target.closest('.mode-btn');
      if (!btn) return;
      setupSelectedMode = btn.getAttribute('data-mode');
      $('modeButtons').querySelectorAll('.mode-btn').forEach(function (b) { b.classList.remove('selected'); });
      btn.classList.add('selected');
    };

    var defCount = Store.getDefaultCount();
    $('setupCount').value = defCount;
    $('countMinus').onclick = function () { var el = $('setupCount'); var v = parseInt(el.value, 10) || 1; el.value = Math.max(1, v - 1); };
    $('countPlus').onclick = function () { var el = $('setupCount'); var v = parseInt(el.value, 10) || 1; el.value = Math.min(200, v + 1); };

    $('setupTypes').innerHTML = TYPE_ORDER.map(function (t) {
      return '<span class="chip" data-type="' + t + '">' + TYPE_LABEL[t] + '</span>';
    }).join('');
    bindChips($('setupTypes'), true, refreshAvail);

    $('setupDiff').innerHTML = [1, 2, 3].map(function (d) {
      return '<span class="chip" data-diff="' + d + '">' + DIFF_LABEL[d] + '</span>';
    }).join('');
    bindChips($('setupDiff'), true, refreshAvail);

    $('setupPool').innerHTML = Object.keys(POOL_LABEL).map(function (k, i) {
      return '<span class="chip' + (i === 0 ? ' on' : '') + '" data-pool="' + k + '">' + POOL_LABEL[k] + '</span>';
    }).join('');
    bindChips($('setupPool'), false, refreshAvail);

    fillChapters($('setupChapter'), name);
    $('setupChapter').onchange = refreshAvail;
    refreshAvail();

    $('setupStart').onclick = function () {
      var list = collectSetup();
      if (!list.length) return;
      var n = parseInt($('setupCount').value, 10) || list.length;
      startSession(shuffle(list).slice(0, n), setupSelectedMode, 'free');
    };
    show('setup');
  }
  function fillChapters(sel, subject) {
    var meta = subject ? subjectMeta(subject) : { chapters: allChapters() };
    sel.innerHTML = '<option value="">全部章节</option>' + meta.chapters.map(function (c) {
      return '<option value="' + esc(c) + '">' + esc(c) + '</option>';
    }).join('');
  }
  function fillSubjects(sel) {
    sel.innerHTML = '<option value="">全部科目</option>' + BANK.subjects.map(function (s) {
      return '<option value="' + esc(s.name) + '">' + esc(s.name) + '</option>';
    }).join('');
  }
  function chipValues(box, attr) {
    var on = box.querySelectorAll('.chip.on'), out = [];
    for (var i = 0; i < on.length; i++) out.push(on[i].getAttribute(attr));
    return out;
  }
  function collectSetup() {
    var name = ctx.subject;
    var chapter = $('setupChapter').value;
    var types = chipValues($('setupTypes'), 'data-type');
    var diffs = chipValues($('setupDiff'), 'data-diff').map(Number);
    var pool = (chipValues($('setupPool'), 'data-pool')[0]) || 'all';
    return BANK.questions.filter(function (q) {
      if (q.subject !== name) return false;
      if (chapter && q.chapter !== chapter) return false;
      if (types.length && types.indexOf(q.type) < 0) return false;
      if (diffs.length && diffs.indexOf(q.difficulty) < 0) return false;
      var r = Store.rec(q.id);
      if (pool === 'wrong') return r.everWrong && !r.mastered;
      if (pool === 'fav') return r.fav;
      if (pool === 'fresh') return !r.seen;
      if (pool === 'due') return SRS.isDue(r);
      return true;
    });
  }
  function refreshAvail() {
    var list = collectSetup();
    var input = $('setupCount');
    $('setupAvail').textContent = '当前可用题目 ' + list.length + ' 道。';
    $('setupStart').disabled = list.length === 0;
    input.max = Math.max(1, list.length);
    if (!list.length) { input.value = 0; return; }
    var cur = parseInt(input.value, 10) || 0;
    if (cur <= 0 || cur > list.length) input.value = Math.min(Store.getDefaultCount(), list.length);
  }
  function bindChips(box, multi, onChange) {
    box.onclick = function (e) {
      var c = e.target.closest('.chip');
      if (!c || !box.contains(c)) return;
      if (multi) c.classList.toggle('on');
      else { var all = box.querySelectorAll('.chip'); for (var i = 0; i < all.length; i++) all[i].classList.remove('on'); c.classList.add('on'); }
      if (onChange) onChange();
    };
  }

  /* ==================== 答题 — 单题模式 ==================== */
  function startSession(questions, mode, origin, subjectOverride) {
    session = {
      list: questions, idx: 0, mode: mode, origin: origin,
      subject: (subjectOverride !== undefined ? subjectOverride : ctx.subject),
      answers: {}, graded: {}, startAt: Date.now(), finished: false
    };
    if (mode === 'batch') {
      renderBatch();
      show('batch');
    } else {
      renderQuiz();
      show('quiz');
    }
  }
  function curQ() { return session.list[session.idx]; }

  function renderQuiz() {
    var q = curQ();
    var total = session.list.length;
    setCrumb(session.subject + ' / ' + (session.origin === 'daily' ? '今日复习' : '练习'));
    $('quizProgress').textContent = '第 ' + (session.idx + 1) + ' / ' + total + ' 题　单题模式';
    $('quizBar').style.width = ((session.idx) / total * 100) + '%';
    updateFavBtn(q.id);

    var g = session.graded[q.id];
    var locked = session.mode === 'instant' && g && g.submitted;
    var html = '<div class="q-meta">'
      + '<span class="tag t-accent">' + TYPE_LABEL[q.type] + '</span>'
      + '<span class="tag">' + esc(q.chapter) + '</span>'
      + '<span class="tag">' + DIFF_LABEL[q.difficulty] + '</span>'
      + '<span class="tag">' + esc(q.id) + '</span>'
      + '</div>'
      + '<div class="stem">' + esc(q.stem) + '</div>'
      + renderInput(q, session.answers[q.id], locked);
    $('quizBody').innerHTML = html;
    bindInput(q, locked);
    if (locked) {
      $('quizBody').insertAdjacentHTML('beforeend', renderFeedback(q, session.answers[q.id], g));
      var fbEl = $('quizBody').querySelector('.feedback');
      if (fbEl) (g.right ? Motion.answerCorrect : Motion.answerWrong)(fbEl);
    }
    bindFeedback(q);
    renderQuizActions(locked);
  }

  function renderInput(q, ua, locked) {
    if (q.type === 'judge') {
      var opts = [{ key: 'T', text: '正确' }, { key: 'F', text: '错误' }];
      return optionsHtml(q, opts, ua ? [ua] : [], locked, ['T', 'F'].filter(function (k) { return k === q.answer; }));
    }
    if (q.type === 'single' || q.type === 'multiple') {
      var sel = q.type === 'single' ? (ua ? [ua] : []) : (ua || []);
      var right = q.type === 'single' ? [q.answer] : q.answer;
      return optionsHtml(q, q.options, sel, locked, right);
    }
    if (q.type === 'blank') {
      var vals = ua || [];
      return '<div class="blank-list">' + q.answer.map(function (b, i) {
        return '<div class="blank-item"><span>第 ' + (i + 1) + ' 空</span>'
          + '<input type="text" class="blank-input" data-i="' + i + '" value="' + esc(vals[i] || '') + '"'
          + (locked ? ' disabled' : '') + ' placeholder="请输入答案"></div>';
      }).join('') + '</div>'
        + (q.unordered ? '<div class="lead" style="margin:8px 0 0">本题各空填写顺序不限。</div>' : '');
    }
    return '<textarea class="short-input" placeholder="请写出你的回答要点"' + (locked ? ' disabled' : '') + '>'
      + esc(ua || '') + '</textarea>';
  }
  function optionsHtml(q, opts, sel, locked, right) {
    return '<div class="options">' + opts.map(function (o) {
      var cls = 'opt';
      if (locked) {
        cls += ' locked';
        if (right.indexOf(o.key) >= 0) cls += ' ok';
        else if (sel.indexOf(o.key) >= 0) cls += ' bad';
      } else if (sel.indexOf(o.key) >= 0) cls += ' sel';
      return '<div class="' + cls + '" data-key="' + o.key + '"><span class="k">' + o.key + '</span>'
        + '<span class="v">' + esc(o.text) + '</span></div>';
    }).join('') + '</div>';
  }
  function bindInput(q, locked) {
    if (locked) return;
    var box = $('quizBody');
    if (q.type === 'single' || q.type === 'multiple' || q.type === 'judge') {
      box.querySelectorAll('.opt').forEach(function (el) {
        el.onclick = function () {
          var k = el.getAttribute('data-key');
          if (q.type === 'multiple') {
            var cur = session.answers[q.id] || []; var i = cur.indexOf(k);
            if (i >= 0) cur.splice(i, 1); else cur.push(k);
            session.answers[q.id] = cur; el.classList.toggle('sel');
          } else {
            session.answers[q.id] = k;
            box.querySelectorAll('.opt').forEach(function (o) { o.classList.remove('sel'); });
            el.classList.add('sel');
          }
          syncActionState();
        };
      });
    } else if (q.type === 'blank') {
      box.querySelectorAll('.blank-input').forEach(function (el) {
        el.oninput = function () {
          var arr = session.answers[q.id] || [];
          arr[parseInt(el.getAttribute('data-i'), 10)] = el.value;
          session.answers[q.id] = arr; syncActionState();
        };
      });
    } else {
      var ta = box.querySelector('.short-input');
      if (ta) ta.oninput = function () { session.answers[q.id] = ta.value; syncActionState(); };
    }
  }
  function hasAnswer(q) {
    var ua = session.answers[q.id];
    if (ua === undefined || ua === null) return false;
    if (Array.isArray(ua)) return ua.some(function (v) { return v !== undefined && String(v).trim() !== ''; });
    return String(ua).trim() !== '';
  }

  function renderFeedback(q, ua, g) {
    var cls = q.type === 'short' ? 'info' : (g.right ? 'ok' : 'bad');
    var title = q.type === 'short' ? '简答题需要你自己判断掌握程度' : (g.right ? '回答正确' : '回答错误');
    var html = '<div class="feedback ' + cls + '">'
      + '<div class="fb-title ' + cls + '">' + title + '</div>';
    if (q.type === 'short') {
      var hits = keywordHits(q, ua || '');
      html += '<div class="fb-block"><span class="lbl">关键词匹配情况（仅供参考）</span>'
        + '<div>命中 ' + hits.length + ' / ' + (q.keywords || []).length + '</div>'
        + '<div class="kw-list">' + (q.keywords || []).map(function (k) {
          return '<span class="kw' + (hits.indexOf(k) >= 0 ? ' hit' : '') + '">' + esc(k) + '</span>';
        }).join('') + '</div></div>';
      html += '<div class="fb-block"><span class="lbl">你的回答</span><div style="white-space:pre-wrap">'
        + esc(ua && String(ua).trim() ? ua : '（未作答）') + '</div></div>';
      html += '<div class="fb-block"><span class="lbl">参考答案</span><div style="white-space:pre-wrap">' + esc(q.answer) + '</div></div>';
    } else {
      html += '<div class="fb-block"><span class="lbl">你的作答</span><div style="white-space:pre-wrap">'
        + esc(userAnswerText(q, ua)) + '</div></div>';
      html += '<div class="fb-block"><span class="lbl">正确答案</span><div style="white-space:pre-wrap">'
        + esc(answerText(q)) + '</div></div>';
    }
    html += '<div class="fb-block"><span class="lbl">解析</span><div>' + esc(q.analysis) + '</div></div>';
    html += '<div class="fb-block"><span class="lbl">出处</span><div class="source-line">' + esc(sourceText(q)) + '</div></div>';
    html += rateHtml(q, g);
    html += '<div class="fb-block"><span class="lbl">下次复习</span><div class="source-line" id="dueHint-' + esc(q.id) + '">'
      + esc(SRS.dueText(Store.rec(q.id))) + '</div></div>';
    html += '</div>';
    return html;
  }
  function rateHtml(q, g) {
    var opts = q.type === 'short'
      ? [['good', '已掌握'], ['hard', '基本掌握'], ['again', '不熟悉']]
      : (g.right ? [['good', '记住了'], ['hard', '不太熟悉']] : [['again', '再练一次']]);
    return '<div class="self-rate" data-rate-for="' + esc(q.id) + '">'
      + '<div class="lbl">' + (q.type === 'short' ? '请自评掌握程度' : '掌握程度') + '</div>'
      + '<div class="chips">' + opts.map(function (o) {
        return '<span class="chip' + (g.grade === o[0] ? ' on' : '') + '" data-grade="' + o[0] + '">' + o[1] + '</span>';
      }).join('') + '</div></div>';
  }
  function bindFeedback(q) {
    var box = $('quizBody').querySelector('[data-rate-for]');
    if (!box) return;
    box.onclick = function (e) {
      var c = e.target.closest('.chip');
      if (!c) return;
      var chips = box.querySelectorAll('.chip');
      for (var i = 0; i < chips.length; i++) chips[i].classList.remove('on');
      c.classList.add('on');
      var grade = c.getAttribute('data-grade');
      var g = session.graded[q.id];
      var right = q.type === 'short' ? (grade !== 'again') : g.right;
      commitGrade(q.id, grade, right);
      var hint = $('dueHint-' + q.id);
      if (hint) hint.textContent = SRS.dueText(Store.rec(q.id));
    };
  }
  function sourceText(q) {
    var s = q.source || {};
    var loc = s.page ? ('第 ' + s.page + ' 页') : s.locator;
    return '《' + s.file + '》 ' + loc + '　题库编号 ' + (s.bankId || q.id);
  }

  function renderQuizActions(locked) {
    var box = $('quizActions');
    var last = session.idx === session.list.length - 1;
    if (session.mode === 'instant') {
      if (!locked) {
        box.innerHTML = '<button class="btn primary" id="btnSubmitOne" type="button">提交本题</button>'
          + '<button class="btn" id="btnSkip" type="button">跳过本题</button>';
        $('btnSubmitOne').onclick = submitCurrent;
        $('btnSubmitOne').disabled = !hasAnswer(curQ());
        $('btnSkip').onclick = function () { next(); };
      } else {
        box.innerHTML = '<button class="btn primary" id="btnNext" type="button">' + (last ? '完成练习' : '下一题') + '</button>';
        $('btnNext').onclick = function () { last ? finish() : next(); };
      }
    } else {
      box.innerHTML = '<button class="btn" id="btnPrev" type="button">上一题</button>'
        + (last ? '<button class="btn primary" id="btnSubmitAll" type="button">提交全部</button>'
          : '<button class="btn primary" id="btnNext" type="button">下一题</button>');
      $('btnPrev').disabled = session.idx === 0;
      $('btnPrev').onclick = function () { session.idx--; renderQuiz(); };
      if (last) $('btnSubmitAll').onclick = submitAll;
      else $('btnNext').onclick = next;
    }
  }
  function syncActionState() {
    var b = $('btnSubmitOne');
    if (b) b.disabled = !hasAnswer(curQ());
  }
  function next() {
    if (session.idx < session.list.length - 1) { session.idx++; renderQuiz(); }
    else finish();
  }
  function submitCurrent() {
    var q = curQ();
    var ua = session.answers[q.id];
    var g = { submitted: true };
    if (q.type === 'short') {
      var hits = keywordHits(q, ua || '');
      var ratio = (q.keywords || []).length ? hits.length / (q.keywords || []).length : 0;
      g.grade = ratio >= 0.6 ? 'good' : (ratio >= 0.3 ? 'hard' : 'again');
      g.right = g.grade !== 'again';
    } else {
      g.right = judgeObjective(q, ua);
      g.grade = g.right ? 'good' : 'again';
    }
    session.graded[q.id] = g;
    commitGrade(q.id, g.grade, g.right);
    renderQuiz();
  }
  function submitAll() {
    session.list.forEach(function (q) {
      if (session.graded[q.id] && session.graded[q.id].submitted) return;
      var ua = session.answers[q.id];
      var g = { submitted: true };
      if (q.type === 'short') {
        var hits = keywordHits(q, ua || '');
        var ratio = (q.keywords || []).length ? hits.length / (q.keywords || []).length : 0;
        g.grade = ratio >= 0.6 ? 'good' : (ratio >= 0.3 ? 'hard' : 'again');
        g.right = g.grade !== 'again';
      } else {
        g.right = judgeObjective(q, ua);
        g.grade = g.right ? 'good' : 'again';
      }
      session.graded[q.id] = g;
      commitGrade(q.id, g.grade, g.right);
    });
    finish();
  }

  /* ==================== 连续答题模式（整页展示） ==================== */
  function renderBatch() {
    var total = session.list.length;
    setCrumb(session.subject + ' / 连续答题');
    $('batchProgress').textContent = '共 ' + total + ' 题　连续答题模式';

    var html = '';
    session.list.forEach(function (q, idx) {
      var ua = session.answers[q.id];
      html += '<div class="batch-item" data-batch-idx="' + idx + '">'
        + '<div class="bi-num">第 ' + (idx + 1) + ' / ' + total + ' 题　' + TYPE_LABEL[q.type] + ' · ' + esc(q.chapter) + '</div>'
        + '<div class="stem">' + esc(q.stem) + '</div>'
        + renderBatchInput(q, ua, idx)
        + '</div>';
    });
    $('batchBody').innerHTML = html;
    bindBatchInputs();
  }

  function renderBatchInput(q, ua, idx) {
    if (q.type === 'judge') {
      var opts = [{ key: 'T', text: '正确' }, { key: 'F', text: '错误' }];
      return batchOptionsHtml(q, opts, ua ? [ua] : [], idx);
    }
    if (q.type === 'single' || q.type === 'multiple') {
      var sel = q.type === 'single' ? (ua ? [ua] : []) : (ua || []);
      return batchOptionsHtml(q, q.options, sel, idx);
    }
    if (q.type === 'blank') {
      var vals = ua || [];
      return '<div class="blank-list">' + q.answer.map(function (b, i) {
        return '<div class="blank-item"><span>第 ' + (i + 1) + ' 空</span>'
          + '<input type="text" class="blank-input batch-blank" data-qid="' + esc(q.id) + '" data-i="' + i + '" value="' + esc(vals[i] || '') + '" placeholder="请输入答案"></div>';
      }).join('') + '</div>';
    }
    return '<textarea class="short-input batch-short" data-qid="' + esc(q.id) + '" placeholder="请写出你的回答要点">'
      + esc(ua || '') + '</textarea>';
  }

  function batchOptionsHtml(q, opts, sel, idx) {
    return '<div class="options">' + opts.map(function (o) {
      var cls = 'opt' + (sel.indexOf(o.key) >= 0 ? ' sel' : '');
      return '<div class="' + cls + '" data-key="' + o.key + '" data-batch-opt="' + idx + '"><span class="k">' + o.key + '</span>'
        + '<span class="v">' + esc(o.text) + '</span></div>';
    }).join('') + '</div>';
  }

  function bindBatchInputs() {
    var wrap = $('batchBody');
    wrap.querySelectorAll('[data-batch-opt]').forEach(function (el) {
      el.onclick = function () {
        var idx = parseInt(el.getAttribute('data-batch-opt'), 10);
        var q = session.list[idx];
        var k = el.getAttribute('data-key');
        if (q.type === 'multiple') {
          var cur = session.answers[q.id] || []; var i = cur.indexOf(k);
          if (i >= 0) cur.splice(i, 1); else cur.push(k);
          session.answers[q.id] = cur; el.classList.toggle('sel');
        } else {
          session.answers[q.id] = k;
          var container = el.closest('.batch-item');
          container.querySelectorAll('.opt').forEach(function (o) { o.classList.remove('sel'); });
          el.classList.add('sel');
        }
      };
    });
    wrap.querySelectorAll('.batch-blank').forEach(function (el) {
      el.oninput = function () {
        var qid = el.getAttribute('data-qid');
        var arr = session.answers[qid] || [];
        arr[parseInt(el.getAttribute('data-i'), 10)] = el.value;
        session.answers[qid] = arr;
      };
    });
    wrap.querySelectorAll('.batch-short').forEach(function (el) {
      el.oninput = function () { session.answers[el.getAttribute('data-qid')] = el.value; };
    });

    $('batchSubmitAll').onclick = function () { submitAll(); };
    $('batchExit').onclick = function () {
      if (session && !session.finished) finish();
      else (ctx.subject ? renderSubject(ctx.subject) : renderHome());
    };
  }

  /* ==================== 完成与复盘 ==================== */
  function finish() {
    if (session.mode === 'instant') {
      session.list = session.list.filter(function (q) { return session.graded[q.id]; });
    }
    session.finished = true;
    var total = session.list.length;
    var right = session.list.filter(function (q) { return session.graded[q.id] && session.graded[q.id].right; }).length;
    if (total > 0) {
      Store.pushHistory({
        at: Date.now(), subject: session.subject,
        origin: session.origin, total: total, correct: right,
        dur: Math.round((Date.now() - session.startAt) / 1000),
        qids: session.list.map(function (q) { return q.id; })
      });
      Store.recordCheckin(total);
    }
    renderResult();
  }

  function renderResult() {
    setCrumb(session.subject + ' / 复盘');
    var total = session.list.length;
    if (!total) {
      $('resultSummary').innerHTML = '';
      $('resultList').innerHTML = '<div class="empty"><div class="t">本次没有完成任何题目</div>'
        + '<div class="d">没有提交的题目不会计入学习记录。</div></div>';
      $('checkinBanner').innerHTML = '';
      show('result');
      return;
    }
    var right = 0, shortN = 0;
    session.list.forEach(function (q) {
      var g = session.graded[q.id];
      if (g && g.right) right++;
      if (q.type === 'short') shortN++;
    });
    $('resultSummary').innerHTML = ov([
      ['本次题量', total], ['判定正确', right], ['正确率', pct(right, total)],
      ['简答题', shortN], ['用时', Math.max(1, Math.round((Date.now() - session.startAt) / 60000)) + ' 分钟']
    ]);

    var checkedToday = Store.isCheckedInToday();
    var ci = Store.getCheckin();
    $('checkinBanner').innerHTML = checkedToday
      ? '<span class="checkin-icon">&#10003;</span> 今日已打卡！累计完成 <b>' + (ci ? ci.count : 0) + '</b> 题，目标 <b>' + Store.getDailyTarget() + '</b> 题'
      : '';

    var html = '';
    session.list.forEach(function (q, i) {
      var g = session.graded[q.id];
      var ua = session.answers[q.id];
      html += '<div class="item">'
        + '<div class="item-head"><div class="q-meta" style="margin:0">'
        + '<span class="tag t-accent">' + (i + 1) + ' / ' + total + '</span>'
        + '<span class="tag">' + TYPE_LABEL[q.type] + '</span>'
        + '<span class="tag">' + esc(q.chapter) + '</span>'
        + '</div>'
        + favBtnHtml(q.id) + '</div>'
        + '<div class="stem">' + esc(q.stem) + '</div>'
        + renderFeedback(q, ua, g)
        + '</div>';
    });
    $('resultList').innerHTML = html;
    bindResultInteractions();
    show('result');
  }
  function favBtnHtml(qid) {
    var on = Store.rec(qid).fav;
    return '<button class="fav-btn' + (on ? ' on' : '') + '" data-fav="' + esc(qid) + '" type="button">'
      + (on ? '已收藏' : '收藏') + '</button>';
  }
  function bindResultInteractions() {
    var root = $('resultList');
    root.querySelectorAll('[data-rate-for]').forEach(function (box) {
      var qid = box.getAttribute('data-rate-for');
      var q = QMAP[qid];
      box.onclick = function (e) {
        var c = e.target.closest('.chip');
        if (!c) return;
        var chips = box.querySelectorAll('.chip');
        for (var i = 0; i < chips.length; i++) chips[i].classList.remove('on');
        c.classList.add('on');
        var grade = c.getAttribute('data-grade');
        var g = session.graded[qid];
        var right = q.type === 'short' ? (grade !== 'again') : g.right;
        commitGrade(qid, grade, right);
        var hint = $('dueHint-' + qid);
        if (hint) hint.textContent = SRS.dueText(Store.rec(qid));
      };
    });
    bindFavButtons(root);
  }
  function bindFavButtons(root) {
    root.querySelectorAll('[data-fav]').forEach(function (btn) {
      btn.onclick = function () {
        var qid = btn.getAttribute('data-fav');
        var on = Store.toggleFav(qid);
        btn.classList.toggle('on', on);
        btn.textContent = on ? '已收藏' : '收藏';
      };
    });
  }
  function updateFavBtn(qid) {
    var b = $('quizFav');
    var on = Store.rec(qid).fav;
    b.textContent = on ? '已收藏' : '收藏';
    b.onclick = function () {
      var v = Store.toggleFav(qid);
      b.textContent = v ? '已收藏' : '收藏';
    };
  }

  /* ==================== 错题本 / 收藏夹（全科目，可折叠筛选） ==================== */
  function renderList(kind) {
    ctx.listKind = kind;
    setCrumb((kind === 'wrong' ? '错题本' : '收藏夹'));
    $('listTitle').textContent = kind === 'wrong' ? '错题本' : '收藏夹';
    $('listLead').textContent = kind === 'wrong'
      ? '答错过的题目会自动进入这里。答对后记录不会被立刻清除，你可以手动标记为已掌握。'
      : '你收藏的题目。可随时取消收藏。';

    fillSubjects($('listSubject'));
    fillChapters($('listChapter'), null);
    $('listTypes').innerHTML = TYPE_ORDER.map(function (t) {
      return '<span class="chip" data-type="' + t + '">' + TYPE_LABEL[t] + '</span>';
    }).join('');
    bindChips($('listTypes'), true, paint);
    $('listSubject').onchange = function () {
      var subj = $('listSubject').value;
      fillChapters($('listChapter'), subj || null);
      paint();
    };
    $('listChapter').onchange = paint;
    $('listPractice').onclick = function () {
      var list = filtered();
      if (!list.length) return;
      startSession(shuffle(list.slice()), 'instant', kind, '（全部科目）');
    };
    paint();
    Motion.stagger($('listBody').querySelectorAll('.item'));
    show('list');

    function filtered() {
      var subj = $('listSubject').value;
      var chapter = $('listChapter').value;
      var types = chipValues($('listTypes'), 'data-type');
      return BANK.questions.filter(function (q) {
        var r = Store.rec(q.id);
        var inKind = kind === 'wrong' ? (r.everWrong) : r.fav;
        if (!inKind) return false;
        if (subj && q.subject !== subj) return false;
        if (chapter && q.chapter !== chapter) return false;
        if (types.length && types.indexOf(q.type) < 0) return false;
        return true;
      });
    }
    function paint() {
      var list = filtered();
      $('listPractice').disabled = !list.length;
      if (!list.length) {
        $('listBody').innerHTML = '<div class="empty"><div class="t">'
          + (kind === 'wrong' ? '暂无错题' : '暂无收藏题')
          + '</div><div class="d">'
          + (kind === 'wrong' ? '在练习中答错的题目会自动出现在这里。' : '在答题页或复盘页点击"收藏"即可把题目加入收藏夹。')
          + '</div></div>';
        return;
      }
      $('listBody').innerHTML = list.map(function (q) {
        var r = Store.rec(q.id);
        var extra = kind === 'wrong'
          ? '<button class="btn small" data-master="' + esc(q.id) + '" type="button">'
          + (r.mastered ? '取消已掌握' : '标记为已掌握') + '</button>'
          : '';
        return '<div class="item">'
          + '<div class="item-head"><div class="q-meta" style="margin:0">'
          + '<span class="tag t-accent">' + TYPE_LABEL[q.type] + '</span>'
          + '<span class="tag">' + esc(q.chapter) + '</span>'
          + '<span class="tag">答对 ' + r.correct + ' / 答错 ' + r.wrong + '</span>'
          + '<span class="tag">下次复习：' + esc(SRS.dueText(r)) + '</span>'
          + (r.mastered ? '<span class="tag t-accent">已掌握</span>' : '')
          + '</div><div>' + extra + ' ' + favBtnHtml(q.id) + '</div></div>'
          + '<div class="stem">' + esc(q.stem) + '</div>'
          + '<div class="fb-block"><span class="lbl">正确答案</span><div style="white-space:pre-wrap">' + esc(answerText(q)) + '</div></div>'
          + '<div class="fb-block"><span class="lbl">解析</span><div>' + esc(q.analysis) + '</div></div>'
          + '<div class="fb-block"><span class="lbl">出处</span><div class="source-line">' + esc(sourceText(q)) + '</div></div>'
          + '</div>';
      }).join('');
      bindFavButtons($('listBody'));
      $('listBody').querySelectorAll('[data-master]').forEach(function (btn) {
        btn.onclick = function () {
          var qid = btn.getAttribute('data-master');
          Store.setMastered(qid, !Store.rec(qid).mastered);
          paint();
        };
      });
    }
  }

  /* ==================== 打卡日历 ==================== */
  function renderCalendar() {
    setCrumb('打卡日历');
    var now = new Date();
    var year = now.getFullYear();
    var month = now.getMonth();
    var today = now.getDate();

    $('calendarLead').textContent = year + '年' + (month + 1) + '月 · 坚持每天打卡，养成复习习惯';

    var ym = year + '-' + (month < 9 ? '0' : '') + (month + 1);
    var checkedDays = Store.getCheckinDays(ym);

    var firstDay = new Date(year, month, 1);
    var startDow = firstDay.getDay();
    var startOffset = startDow === 0 ? 6 : startDow - 1;
    var daysInMonth = new Date(year, month + 1, 0).getDate();

    var header = '<h3>' + year + ' 年 ' + (month + 1) + ' 月</h3>';
    var dowLabels = ['一', '二', '三', '四', '五', '六', '日'];
    var headCells = dowLabels.map(function (d) { return '<div class="cal-head-cell">' + d + '</div>'; }).join('');

    var cells = '';
    var prevMonthDays = new Date(year, month, 0).getDate();
    for (var i = startOffset - 1; i >= 0; i--) {
      cells += '<div class="cal-day other-month">' + (prevMonthDays - i) + '</div>';
    }
    for (var d = 1; d <= daysInMonth; d++) {
      var isChecked = checkedDays.indexOf(d) >= 0;
      var isToday = d === today;
      var cls = 'cal-day clickable';
      if (isChecked) cls += ' checked';
      if (isToday) cls += ' today';
      cells += '<div class="' + cls + '" data-day="' + d + '">' + d + '</div>';
    }
    var totalCells = startOffset + daysInMonth;
    var remaining = totalCells % 7 === 0 ? 0 : 7 - (totalCells % 7);
    for (var j = 1; j <= remaining; j++) {
      cells += '<div class="cal-day other-month">' + j + '</div>';
    }

    $('calendarWrap').innerHTML =
      '<div class="cal-header">' + header + '</div>'
      + '<div class="cal-grid">' + headCells + cells + '</div>';

    $('calendarDetail').hidden = true;
    $('calendarDetail').innerHTML = '';

    var allDays = Object.keys(Store.all().checkins || {});
    var totalCheckins = allDays.length;
    var thisMonthCheckins = checkedDays.length;
    var streak = calcStreak(year, month, today, checkedDays);
    $('calendarStats').innerHTML = '本月已打卡 <b>' + thisMonthCheckins + '</b> 天 · '
      + '当前连续 <b>' + streak + '</b> 天 · 累计打卡 <b>' + totalCheckins + '</b> 天';

    show('calendar');
  }

  function calcStreak(year, month, today, checkedDays) {
    var streak = 0;
    if (checkedDays.indexOf(today) >= 0) streak++;
    for (var d = today - 1; d >= 1; d--) {
      if (checkedDays.indexOf(d) >= 0) streak++; else break;
    }
    return streak;
  }

  function renderDayDetail(year, month, day) {
    var ym = year + '-' + (month < 9 ? '0' : '') + (month + 1);
    var key = ym + '-' + (day < 10 ? '0' + day : '' + day);
    var d = Store.getDayDetail(key);
    var subjectChips = Object.keys(d.bySubject).map(function (s) {
      return '<span>' + esc(s) + ' ' + d.bySubject[s] + ' 题</span>';
    }).join('');
    var qlist = d.qids.slice(0, 60).map(function (qid) {
      var q = QMAP[qid];
      return q ? '<div class="item"><div class="stem">' + esc(q.stem) + '</div></div>' : '';
    }).join('');
    var html = '<h4>' + key + ' 练习总览</h4>'
      + '<div class="cd-grid">'
      + '<span>题量 <b>' + d.total + '</b></span>'
      + '<span>正确率 <b>' + d.rate + '%</b></span>'
      + '<span>打卡 <b>' + (d.checked ? '已打卡' : '未打卡') + '</b></span>'
      + '</div>'
      + (subjectChips ? '<div class="cd-subject">' + subjectChips + '</div>' : '')
      + (qlist
          ? '<details open><summary>当日题目明细（' + d.qids.length + '）</summary><div class="cd-qlist">' + qlist + '</div></details>'
          : '<div class="cd-grid" style="margin-bottom:0">当日没有可展示的题目明细（仅统计了练习次数）。</div>');
    var panel = $('calendarDetail');
    panel.innerHTML = html;
    panel.hidden = false;
    Motion.expand(panel);
  }

  /* ==================== 设置 ==================== */
  function renderSettings() {
    setCrumb('设置');
    var s = Store.getSettings();

    // 外观主题（从顶栏主题切换按钮移入此处）
    var themeBox = $('settingTheme');
    if (themeBox) {
      var curTheme = Store.getTheme();
      themeBox.innerHTML = '<span class="chip' + (curTheme === 'light' ? ' on' : '') + '" data-theme="light">浅色</span>'
        + '<span class="chip' + (curTheme === 'dark' ? ' on' : '') + '" data-theme="dark">深色</span>';
      themeBox.onclick = function (e) {
        var c = e.target.closest('.chip'); if (!c) return;
        var t = c.getAttribute('data-theme');
        Store.setTheme(t); applyTheme(t);
        Array.prototype.forEach.call(themeBox.querySelectorAll('.chip'), function (x) { x.classList.remove('on'); });
        c.classList.add('on');
      };
    }

    var motionBox = $('settingMotion');
    if (motionBox) {
      var motionOn = Store.getMotion();
      motionBox.innerHTML = '<span class="chip' + (motionOn ? ' on' : '') + '" data-motion="1">开</span>'
        + '<span class="chip' + (!motionOn ? ' on' : '') + '" data-motion="0">关</span>';
      motionBox.onclick = function (e) {
        var c = e.target.closest('.chip'); if (!c) return;
        var v = c.getAttribute('data-motion') === '1';
        Store.setMotion(v);
        Array.prototype.forEach.call(motionBox.querySelectorAll('.chip'), function (x) { x.classList.remove('on'); });
        c.classList.add('on');
      };
    }

    // 复习节奏：整体缩放自适应间隔，让遗忘曲线可控
    var paceBox = $('settingPace');
    if (paceBox) {
      var curPace = PACE_ORDER.indexOf(s.pace) >= 0 ? s.pace : 'normal';
      paceBox.innerHTML = PACE_ORDER.map(function (p) {
        return '<span class="chip' + (curPace === p ? ' on' : '') + '" data-pace="' + p + '" title="' + esc(PACE_DESC[p]) + '">' + PACE_LABEL[p] + '</span>';
      }).join('') + '<div class="set-hint" id="paceHint">' + esc(PACE_DESC[curPace]) + '</div>';
      bindChips(paceBox, false, function () {
        var p = paceBox.querySelector('.chip.on').getAttribute('data-pace');
        Store.setSetting('pace', p);
        if (window.SRS && SRS.setPace) SRS.setPace(p);
        var ph = $('paceHint');
        if (ph) ph.textContent = PACE_DESC[p];
      });
    }

    $('settingMode').innerHTML =
      '<span class="chip' + (s.defaultMode === 'instant' ? ' on' : '') + '" data-smode="instant">单题模式</span>'
      + '<span class="chip' + (s.defaultMode !== 'instant' ? ' on' : '') + '" data-smode="batch">连续答题</span>';
    bindChips($('settingMode'), false);

    // 今日复习弹出频率（每科每日 / 全局每日 / 关闭），带一句话说明
    var dmBox = $('settingDailyModal');
    if (dmBox) {
      var curDm = Store.getDailyModalSetting();
      dmBox.innerHTML = DAILY_MODAL_ORDER.map(function (m) {
        return '<span class="chip' + (curDm === m ? ' on' : '') + '" data-dm="' + m + '" title="' + esc(DAILY_MODAL_DESC[m]) + '">' + DAILY_MODAL_LABEL[m] + '</span>';
      }).join('') + '<div class="set-hint" id="dailyModalHint">' + esc(DAILY_MODAL_DESC[curDm]) + '</div>';
      bindChips(dmBox, false, function () {
        var m = dmBox.querySelector('.chip.on').getAttribute('data-dm');
        Store.setDailyModalSetting(m);
        var h = $('dailyModalHint');
        if (h) h.textContent = DAILY_MODAL_DESC[m];
      });
    }

    $('settingCount').value = s.defaultCount || 20;
    $('settingTarget').value = s.dailyTarget || 10;

    $('saveSettingsBtn').onclick = function () {
      var mode = $('settingMode').querySelector('.chip.on').getAttribute('data-smode');
      var count = parseInt($('settingCount').value, 10) || 20;
      var target = parseInt($('settingTarget').value, 10) || 10;
      Store.setSetting('defaultMode', mode);
      Store.setSetting('defaultCount', count);
      Store.setSetting('dailyTarget', target);
      alert('设置已保存');
    };

    $('clearDataBtn').onclick = function () {
      showConfirm('清除所有学习数据', '此操作将清空所有答题记录、打卡记录、收藏和错题标记，且不可撤销。确定要继续吗？', function () {
        Store.clearAll();
        alert('所有数据已清除');
        renderHome();
      });
    };

    show('settings');
  }

  /* 确认弹窗 */
  function showConfirm(title, msg, onOk) {
    $('confirmTitle').textContent = title;
    $('confirmMsg').textContent = msg;
    $('confirmModal').hidden = false;
    var okHandler = function () {
      $('confirmModal').hidden = true;
      $('confirmOk').removeEventListener('click', okHandler);
      $('confirmCancel').removeEventListener('click', cancelHandler);
      onOk();
    };
    var cancelHandler = function () {
      $('confirmModal').hidden = true;
      $('confirmOk').removeEventListener('click', okHandler);
      $('confirmCancel').removeEventListener('click', cancelHandler);
    };
    $('confirmOk').addEventListener('click', okHandler);
    $('confirmCancel').addEventListener('click', cancelHandler);
  }

  /* ==================== 统计详情（独立页面） ==================== */
  function formatDuration(sec) {
    sec = Math.max(0, Math.round(sec || 0));
    var m = Math.floor(sec / 60);
    var s = sec % 60;
    return m + ' 分 ' + s + ' 秒';
  }
  function countUnits() {
    var units = {};
    BANK.questions.forEach(function (q) { units[q.chapter] = 1; });
    return Object.keys(units).length;
  }
  /* 当前连续打卡天数（向今天回溯；今天未打卡则从昨天起算） */
  function currentStreak() {
    var now = new Date();
    var ym0 = now.getFullYear() + '-' + (now.getMonth() < 9 ? '0' : '') + (now.getMonth() + 1);
    var offset = Store.getCheckinDays(ym0).indexOf(now.getDate()) < 0 ? 1 : 0;
    var streak = 0;
    for (var i = offset; i < 365; i++) {
      var d = new Date(now);
      d.setDate(now.getDate() - i);
      var ym = d.getFullYear() + '-' + (d.getMonth() < 9 ? '0' : '') + (d.getMonth() + 1);
      if (Store.getCheckinDays(ym).indexOf(d.getDate()) >= 0) streak++;
      else break;
    }
    return streak;
  }
  /* 读取 CSS 变量真实值（SVG 内联样式无法用 var()，需注入实际色值） */
  function cssVar(name, fallback) {
    try {
      var v = (getComputedStyle(document.documentElement).getPropertyValue(name) || '').trim();
      return v || fallback;
    } catch (e) { return fallback; }
  }
  function lastNDays(n) {
    var out = [], now = new Date();
    for (var i = n - 1; i >= 0; i--) {
      var d = new Date(now); d.setDate(now.getDate() - i);
      var mm = (d.getMonth() < 9 ? '0' : '') + (d.getMonth() + 1);
      var dd = (d.getDate() < 10 ? '0' : '') + d.getDate();
      out.push({ date: d.getFullYear() + '-' + mm + '-' + dd, label: (d.getMonth() + 1) + '/' + d.getDate() });
    }
    return out;
  }
  function dayStats(n) {
    var days = lastNDays(n);
    var hist = Store.all().history || [];
    return days.map(function (day) {
      var cnt = 0, correct = 0;
      hist.forEach(function (h) {
        if (fmtTime(h.at).slice(0, 10) === day.date) {
          cnt += h.total || 0; correct += h.correct || 0;
        }
      });
      return { date: day.date, label: day.label, count: cnt, correct: correct, rate: cnt ? Math.round(correct / cnt * 100) : 0 };
    });
  }
  function renderTrendChart() {
    var wrap = $('statsChartWrap');
    if (!wrap) return;
    var data = dayStats(7);
    var maxCount = 1;
    data.forEach(function (d) { if (d.count > maxCount) maxCount = d.count; });

    var W = (wrap.clientWidth || 600);
    var H = 220;
    var pad = { t: 20, r: 46, b: 30, l: 40 };
    var chartW = W - pad.l - pad.r;
    var chartH = H - pad.t - pad.b;
    var barW = Math.max(14, Math.min(34, chartW / data.length * 0.46));
    var slot = chartW / data.length;
    var barGap = (slot - barW) / 2;

    var accent = cssVar('--accent', '#35507e');
    var warn = cssVar('--warn', '#97701f');
    var hair = cssVar('--hairline', 'rgba(28,24,20,0.1)');
    var ink3 = cssVar('--ink-3', '#a39e98');
    var ink = cssVar('--ink', '#23201c');

    var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" width="100%" height="' + H + '" xmlns="http://www.w3.org/2000/svg">';
    svg += '<rect x="0" y="0" width="' + W + '" height="' + H + '" fill="transparent"/>';
    // 横向网格线
    for (var i = 0; i <= 4; i++) {
      var y = pad.t + chartH - (chartH * i / 4);
      svg += '<line x1="' + pad.l + '" y1="' + y + '" x2="' + (W - pad.r) + '" y2="' + y + '" stroke="' + hair + '" stroke-width="1"/>';
      svg += '<text x="' + (pad.l - 6) + '" y="' + (y + 3) + '" fill="' + ink3 + '" font-size="10" text-anchor="end">' + Math.round(maxCount * i / 4) + '</text>';
    }
    // 右侧百分比刻度
    for (var j = 0; j <= 4; j++) {
      var yr = pad.t + chartH - (chartH * j / 4);
      svg += '<text x="' + (W - pad.r + 6) + '" y="' + (yr + 3) + '" fill="' + ink3 + '" font-size="10">' + (j * 25) + '%</text>';
    }
    // 柱状图（答题数）
    data.forEach(function (d, idx) {
      var x = pad.l + slot * idx + barGap;
      var barH = (d.count / maxCount) * chartH;
      var y = pad.t + chartH - barH;
      svg += '<rect x="' + x + '" y="' + y + '" width="' + barW + '" height="' + barH + '" rx="4" fill="' + accent + '" opacity="0.75"/>';
      svg += '<text x="' + (x + barW / 2) + '" y="' + (H - pad.b + 14) + '" fill="' + ink3 + '" font-size="10" text-anchor="middle">' + d.label + '</text>';
      if (d.count > 0) {
        svg += '<text x="' + (x + barW / 2) + '" y="' + (y - 4) + '" fill="' + ink + '" font-size="10" font-weight="600" text-anchor="middle">' + d.count + '</text>';
      }
    });
    // 折线图（正确率）
    var pts = data.map(function (d, idx) {
      var x = pad.l + slot * idx + barGap + barW / 2;
      var y = pad.t + chartH - (d.rate / 100) * chartH;
      return x + ',' + y;
    }).join(' ');
    svg += '<polyline points="' + pts + '" fill="none" stroke="' + warn + '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>';
    data.forEach(function (d, idx) {
      var x = pad.l + slot * idx + barGap + barW / 2;
      var y = pad.t + chartH - (d.rate / 100) * chartH;
      svg += '<circle cx="' + x + '" cy="' + y + '" r="3.5" fill="' + cssVar('--surface', '#ffffff') + '" stroke="' + warn + '" stroke-width="2"/>';
    });
    svg += '</svg>';
    wrap.innerHTML = svg;
  }
  function renderStatsPage() {
    var all = statsOf(BANK.questions);

    // 总览大卡片
    $('statsHeroNum').textContent = all.total;
    $('statsHeroNum').setAttribute('data-num', all.total);
    $('statsSubjectCount').textContent = BANK.subjects.length;
    $('statsUnitCount').textContent = countUnits();

    // 2×2 色块卡片
    $('statsTileDoneNum').textContent = all.practiced;
    $('statsTileDoneNum').setAttribute('data-num', all.practiced);
    $('statsTileDoneSub').textContent = '完成度 ' + pct(all.practiced, all.total);

    $('statsTileAccNum').textContent = all.rate;
    $('statsTileAccNum').setAttribute('data-num', all.rate);
    $('statsTileAccSub').textContent = '正 ' + all.correct + ' 题 · 错 ' + all.wrong + ' 题';

    var dur = (Store.all().history || []).reduce(function (a, h) { return a + (h.dur || 0); }, 0);
    $('statsTileTimeNum').textContent = formatDuration(dur);

    $('statsTileWrongNum').textContent = all.wrong;
    $('statsTileWrongNum').setAttribute('data-num', all.wrong);
    $('statsTileWrongSub').textContent = '收藏 ' + all.fav + ' 题 · 未做 ' + (all.total - all.practiced) + ' 题';

    // 趋势图表
    renderTrendChart();

    // 各科目明细表
    var rows = BANK.subjects.map(function (s) {
      var st = statsOf(subjectQuestions(s.name));
      return '<tr><td>' + esc(s.name) + '</td><td>' + st.total + '</td><td>' + st.practiced + '</td><td>'
        + st.rate + '</td><td>' + st.due + '</td><td>' + st.wrong + '</td><td>' + st.fav + '</td></tr>';
    }).join('');
    $('statsTable').innerHTML = '<thead><tr><th>科目</th><th>总题量</th><th>已练习</th><th>正确率</th>'
      + '<th>今日待复习</th><th>错题</th><th>收藏</th></tr></thead><tbody>' + rows + '</tbody>';

    // 最近学习记录
    var hist = (Store.all().history || []).slice(0, 10);
    if (!hist.length) {
      $('statsHistory').innerHTML = '<div class="empty"><div class="t">暂无学习记录</div>'
        + '<div class="d">完成一次练习后，这里会显示最近的练习情况。</div></div>';
    } else {
      $('statsHistory').innerHTML = '<div class="table-scroll"><table class="stat"><thead><tr>'
        + '<th>时间</th><th>科目</th><th>来源</th><th>题量</th><th>正确</th><th>正确率</th></tr></thead><tbody>'
        + hist.map(function (h) {
          var o = { daily: '今日复习', free: '自由练习', wrong: '错题本', fav: '收藏夹' }[h.origin] || '练习';
          return '<tr><td>' + fmtTime(h.at) + '</td><td>' + esc(h.subject) + '</td><td>' + o
            + '</td><td>' + h.total + '</td><td>' + h.correct + '</td><td>' + pct(h.correct, h.total) + '</td></tr>';
        }).join('') + '</tbody></table></div>';
    }

    if (Motion.enabled()) {
      Motion.countUp($('statsHeroNum'), all.total);
      Motion.countUp($('statsTileDoneNum'), all.practiced);
      Motion.countUp($('statsTileWrongNum'), all.wrong);
    }
    $('statsHeroAction').onclick = function () { renderStatsPage(); Motion.viewIn('#view-stats'); };
  }

  /* ==================== 主题 ================= */
  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
  }

  /* ==================== 全局事件绑定 ==================== */
  function bindGlobal() {
    $('brandHome').onclick = renderHome;
    var meta = (BANK && BANK.meta) || {};
    var brandIcon = ICONS[meta.brandIcon] || ICONS.book;
    $('brandMark').innerHTML = brandIcon;
    $('dailyHintIcon').innerHTML = brandIcon;
    if (meta.brandName) $('brandName').textContent = meta.brandName;
    if (meta.title) document.title = meta.title;
    $('navStats').onclick = function () { show('stats'); };

    $('navSettings').onclick = function () { renderSettings(); };
    $('navCalendar').onclick = function () { renderCalendar(); };
    $('navWrong').onclick = function () { renderList('wrong'); };
    $('navFav').onclick = function () { renderList('fav'); };

    // 日历点击日期 → 当日总览
    $('calendarWrap').addEventListener('click', function (e) {
      var cell = e.target.closest('.cal-day.clickable');
      if (!cell) return;
      var day = parseInt(cell.getAttribute('data-day'), 10);
      var now = new Date();
      renderDayDetail(now.getFullYear(), now.getMonth(), day);
    });

    // 今日复习模态：点击遮罩关闭（视为跳过，记录今天不再自动弹）
    $('dailyModal').addEventListener('click', function (e) {
      if (e.target === this) { Motion.modalOut(this); if (ctx.subject) Store.dismissDailyModal(ctx.subject); }
    });

    document.addEventListener('click', function (e) {
      var go = e.target.closest('[data-go]');
      if (go) {
        var v = go.getAttribute('data-go');
        if (v === 'home') renderHome();
        else if (v === 'stats') show('stats');
        else if (v === 'subject') ctx.subject ? renderSubject(ctx.subject) : renderHome();
        else if (v === 'free') renderSetup();
        else if (v === 'back') ctx.subject ? renderSubject(ctx.subject) : renderHome();
        return;
      }
      var card = e.target.closest('[data-subject]');
      if (card) {
        var name = card.getAttribute('data-subject');
        renderSubject(name); // 是否弹模态由 renderSubject 内按频率设置决定
        return;
      }
      var entry = e.target.closest('[data-entry]');
      if (entry) {
        var k = entry.getAttribute('data-entry');
        if (k === 'daily') renderDaily();
        else if (k === 'free') renderSetup();
        else if (k === 'wrong') renderList('wrong');
        else if (k === 'fav') renderList('fav');
        else if (k === 'stats') show('stats');
        return;
      }
    });

    $('quizExit').onclick = function () {
      if (session && !session.finished) finish();
      else (ctx.subject ? renderSubject(ctx.subject) : renderHome());
    };
  }

  /* ==================== 启动 ==================== */
  function boot() {
    Store.init();
    applyTheme(Store.getTheme());
    if (window.SRS && SRS.setPace) SRS.setPace((Store.getSettings() || {}).pace);
    BANK = window.__EMBEDDED_BANK__ || null;

    var booted = false;
    var done = function () {
      if (booted) return;
      booted = true;
      if (!BANK || !BANK.questions || !BANK.questions.length) { show('fatal'); return; }
      BANK.questions.forEach(function (q) { QMAP[q.id] = q; });
      if (!BANK.subjects || !BANK.subjects.length) {
        var names = [];
        BANK.questions.forEach(function (q) { if (names.indexOf(q.subject) < 0) names.push(q.subject); });
        BANK.subjects = names.map(function (n) {
          var chs = [];
          BANK.questions.forEach(function (q) { if (q.subject === n && chs.indexOf(q.chapter) < 0) chs.push(q.chapter); });
          return { name: n, desc: '', icon: 'book', chapters: chs };
        });
      }
      bindGlobal();
      renderHome();
    };

    try {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', 'questions.json', true);
      xhr.onload = function () {
        try { var j = JSON.parse(xhr.responseText); if (j && j.questions && j.questions.length) BANK = j; } catch (e) {}
        done();
      };
      xhr.onerror = function () { done(); };
      xhr.send();
    } catch (e) { done(); }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
