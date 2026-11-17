/* 本地存储层：所有学习数据仅保存在当前浏览器中，不上传、不联网。 */
(function (global) {
  'use strict';

  var KEY = 'qbank.v1';

  var DEFAULT_STATE = {
    theme: 'light',
    records: {},       // qid -> record
    history: [],       // 最近学习记录（最多50条）
    lastSetup: null,
    // 新增：打卡与设置
    checkins: {},      // 'YYYY-MM-DD' -> { count: number, target: number }
    dailyModalDismissed: {}, // 'subject|YYYY-MM-DD' 或 'global|YYYY-MM-DD' -> true（今日复习弹窗当天不再弹出）
    settings: {
      defaultMode: 'instant',   // 'instant' | 'batch'
      defaultCount: 20,
      dailyTarget: 10,          // 每日打卡目标题量
      dailyModal: 'subject',    // 今日复习弹出频率：'subject' 每科每日 / 'global' 全局每日 / 'off' 关闭自动弹出
      motion: true,             // 界面动效开关（页面切换 / 数字滚动 / 进度条过渡）
      pace: 'normal'            // 复习节奏：'steady' 稳扎稳打 / 'normal' 标准 / 'fast' 快速推进
    }
  };

  var VALID_DAILY_MODAL = ['subject', 'global', 'off'];
  var VALID_PACE = ['steady', 'normal', 'fast'];

  function defaultRecord() {
    return {
      correct: 0,
      wrong: 0,
      seen: 0,
      lastAt: 0,
      lastResult: '',
      due: 0,
      stage: 0,
      interval: 0,
      ease: 2.5,          // 记忆强度：随答题表现渐进升降，驱动自适应间隔
      fav: false,
      everWrong: false,
      mastered: false
    };
  }

  var state = null;
  var available = true;

  function load() {
    try {
      var raw = global.localStorage.getItem(KEY);
      if (!raw) return JSON.parse(JSON.stringify(DEFAULT_STATE));
      var obj = JSON.parse(raw);
      if (!obj || typeof obj !== 'object') throw new Error('bad');
      obj.theme = obj.theme === 'dark' ? 'dark' : 'light';
      obj.records = obj.records && typeof obj.records === 'object' ? obj.records : {};
      obj.history = Array.isArray(obj.history) ? obj.history : [];
      obj.checkins = obj.checkins && typeof obj.checkins === 'object' ? obj.checkins : {};
      if (!obj.settings || typeof obj.settings !== 'object') obj.settings = {};
      var s = obj.settings;
      // 旧数据可能含已废弃的 accent 字段，静默忽略
      if ('accent' in obj) delete obj.accent;
      if (typeof s.defaultMode !== 'string') s.defaultMode = 'instant';
      if (typeof s.defaultCount !== 'number' || s.defaultCount < 1) s.defaultCount = 20;
      if (typeof s.dailyTarget !== 'number' || s.dailyTarget < 1) s.dailyTarget = 10;
      if (VALID_DAILY_MODAL.indexOf(s.dailyModal) < 0) s.dailyModal = 'subject';
      if (typeof s.motion !== 'boolean') s.motion = true;
      if (VALID_PACE.indexOf(s.pace) < 0) s.pace = 'normal';
      obj.dailyModalDismissed = obj.dailyModalDismissed && typeof obj.dailyModalDismissed === 'object' ? obj.dailyModalDismissed : {};
      // 清理非今天的记录，避免无限增长
      var tk = todayKey();
      Object.keys(obj.dailyModalDismissed).forEach(function (k) {
        if (k.indexOf(tk) < 0) delete obj.dailyModalDismissed[k];
      });
      return obj;
    } catch (e) {
      return JSON.parse(JSON.stringify(DEFAULT_STATE));
    }
  }

  function save() {
    if (!available) return;
    try {
      global.localStorage.setItem(KEY, JSON.stringify(state));
    } catch (e) {
      available = false;
    }
  }

  /* ---------- 打卡 ---------- */
  function todayKey() {
    var d = new Date();
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
  }
  function p(n) { return n < 10 ? '0' + n : '' + n; }

  /* ---------- 设置 ---------- */
  function getSettings() {
    return state.settings || DEFAULT_STATE.settings;
  }

  var Store = {
    init: function () {
      try {
        global.localStorage.setItem(KEY + '.probe', '1');
        global.localStorage.removeItem(KEY + '.probe');
      } catch (e) {
        available = false;
      }
      state = load();
      return state;
    },
    isAvailable: function () { return available; },
    all: function () { return state; },
    getTheme: function () { return state.theme; },
    setTheme: function (t) { state.theme = (t === 'dark' ? 'dark' : 'light'); save(); },
    getMotion: function () { return !!(state.settings && state.settings.motion); },
    setMotion: function (v) {
      if (!state.settings) state.settings = {};
      state.settings.motion = !!v;
      save();
    },

    /* ----- 题目记录 ----- */
    rec: function (qid) { return state.records[qid] || defaultRecord(); },
    recW: function (qid) { if (!state.records[qid]) state.records[qid] = defaultRecord(); return state.records[qid]; },
    commit: save,
    toggleFav: function (qid) { var r = this.recW(qid); r.fav = !r.fav; save(); return r.fav; },
    setMastered: function (qid, v) { var r = this.recW(qid); r.mastered = !!v; save(); },
    pushHistory: function (entry) { state.history.unshift(entry); if (state.history.length > 50) state.history.length = 50; save(); },
    saveSetup: function (setup) { state.lastSetup = setup; save(); },
    getSetup: function () { return state.lastSetup; },
    defaultRecord: defaultRecord,

    /* ----- 打卡 ----- */
    todayKey: todayKey,
    getCheckin: function (key) { key = key || todayKey(); return state.checkins[key] || null; },
    recordCheckin: function (count) {
      var key = todayKey();
      var prev = state.checkins[key] || { count: 0, target: this.getDailyTarget() };
      prev.count += (count || 0);
      state.checkins[key] = prev;
      save();
      return prev;
    },
    isCheckedInToday: function () { return !!state.checkins[todayKey()]; },
    getCheckinDays: function (yearMonth) {
      // 返回该月所有已打卡日期数组 [1, 3, 5, ...]
      var out = [];
      var prefix = yearMonth + '-';
      Object.keys(state.checkins).forEach(function (k) {
        if (k.indexOf(prefix) === 0) out.push(parseInt(k.slice(8), 10));
      });
      return out.sort(function (a, b) { return a - b; });
    },
    getYesterdayStats: function () {
      var d = new Date();
      d.setDate(d.getDate() - 1);
      var key = d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
      var c = state.checkins[key];
      if (!c) return { count: 0, correct: 0, total: 0, rate: 0 };
      // 从 history 中找昨天的练习记录统计正确率
      var dayStart = new Date(key + 'T00:00:00').getTime();
      var dayEnd = dayStart + 86400000;
      var h = state.history.filter(function (x) { return x.at >= dayStart && x.at < dayEnd; });
      var tc = 0, tr = 0;
      h.forEach(function (x) { tc += x.total; tr += x.correct; });
      return { count: c.count, correct: tr, total: tc, rate: tc ? Math.round(tr * 100 / tc) : 0 };
    },
    suggestDailyTarget: function () {
      var y = this.getYesterdayStats();
      var base = this.getDailyTarget();
      if (y.total === 0) return base;
      // 答对率 >=70% → 目标+5；<50% → 目标-3；否则不变
      if (y.rate >= 70) return Math.min(base + 5, 50);
      if (y.rate < 50) return Math.max(base - 3, 5);
      return base;
    },

    /* 某一天的练习详情（用于日历点选日期总览） */
    getDayDetail: function (dateKey) {
      var dayStart = new Date(dateKey + 'T00:00:00').getTime();
      var dayEnd = dayStart + 86400000;
      var sessions = state.history.filter(function (x) { return x.at >= dayStart && x.at < dayEnd; });
      var bySubject = {};
      var total = 0, correct = 0, qids = [];
      sessions.forEach(function (s) {
        total += s.total; correct += s.correct;
        bySubject[s.subject] = (bySubject[s.subject] || 0) + s.total;
        if (Array.isArray(s.qids)) qids = qids.concat(s.qids);
      });
      return {
        date: dateKey,
        sessions: sessions,
        bySubject: bySubject,
        total: total,
        correct: correct,
        rate: total ? Math.round(correct * 100 / total) : 0,
        qids: qids,
        checked: !!state.checkins[dateKey]
      };
    },

    /* ----- 设置 ----- */
    getSettings: getSettings,
    getSetting: function (k) { return getSettings()[k]; },
    setSetting: function (k, v) {
      if (!state.settings) state.settings = {};
      state.settings[k] = v;
      save();
    },
    getDailyTarget: function () { return (getSettings().dailyTarget || 10); },
    getDefaultMode: function () { return getSettings().defaultMode || 'instant'; },
    getDefaultCount: function () { return getSettings().defaultCount || 20; },

    /* ----- 今日复习弹出频率 ----- */
    getDailyModalSetting: function () {
      var d = (state.settings && state.settings.dailyModal) || 'subject';
      return VALID_DAILY_MODAL.indexOf(d) >= 0 ? d : 'subject';
    },
    setDailyModalSetting: function (v) {
      if (VALID_DAILY_MODAL.indexOf(v) >= 0) { state.settings.dailyModal = v; save(); }
    },
    // 是否应当自动弹出今日复习模态（受频率设置 + 当天已关闭记录控制）
    shouldShowDailyModal: function (subject) {
      var mode = this.getDailyModalSetting();
      if (mode === 'off') return false;
      var key = todayKey();
      var k = mode === 'global' ? ('global|' + key) : (subject + '|' + key);
      return !state.dailyModalDismissed[k];
    },
    // 记录该科目/全局今天已关闭/已处理，当天不再自动弹出
    dismissDailyModal: function (subject) {
      var mode = this.getDailyModalSetting();
      var key = todayKey();
      var k = mode === 'global' ? ('global|' + key) : (subject + '|' + key);
      state.dailyModalDismissed[k] = true;
      save();
    },
    clearAll: function () {
      state.records = {};
      state.history = [];
      state.checkins = {};
      state.dailyModalDismissed = {};
      save();
    }
  };

  global.Store = Store;
})(window);
