/* 复习排程：自适应间隔重复（Adaptive Spaced Repetition）。

   与固定阶梯（1/3/7/14/30）不同，这里每道题都带一个专属的「记忆强度」ease，
   随你的答题表现渐进升降，间隔由 ease 动态推算 —— 同一天开始学的两道题，
   一道你次次秒答、一道你反复卡壳，几轮之后复习节奏会完全分开。

   规则概要：
   - good（答对且掌握）：stage +1，间隔按 ease 拉长
   - easy（很轻松）    ：ease +0.18，间隔额外 ×1.4
   - hard（勉强答对）  ：ease −0.15，stage −1，间隔缩到上次的一半（至少 1 天）
   - again（答错/不熟）：ease −0.20，stage 归零，当天重来

   边界与可控性：
   - ease 恒定夹在 [1.3, 3.0]，间隔恒定夹在 [1, 180] 天，不会失控
   - 间隔 ≥ 4 天时加 ±15% 模糊偏移，避免大量题目堆在同一天到期
   - 用户可在设置中选择复习节奏（稳扎稳打 ×0.8 / 标准 ×1.0 / 快速推进 ×1.3）
*/
(function (global) {
  'use strict';

  var EASE_START = 2.5;   // 新题初始记忆强度
  var EASE_MIN = 1.3;     // 下限：再难的题也不会陷入每天重刷
  var EASE_MAX = 3.0;     // 上限：再简单的题也不会一次跳太远
  var MAX_DAYS = 180;     // 单次间隔上限
  var FUZZ = 0.15;        // 到期日模糊偏移幅度
  var DAY = 24 * 60 * 60 * 1000;

  // 复习节奏系数（用户可在设置中调整）
  var PACE_FACTORS = { steady: 0.8, normal: 1.0, fast: 1.3 };
  var paceFactor = 1.0;
  var fuzzEnabled = true;

  /** 设置复习节奏：'steady' | 'normal' | 'fast' */
  function setPace(key) {
    paceFactor = PACE_FACTORS[key] || 1.0;
  }

  /** 关闭到期日模糊偏移（供自动化测试得到确定结果） */
  function setFuzz(on) {
    fuzzEnabled = !!on;
  }

  function clamp(v, lo, hi) {
    return Math.min(hi, Math.max(lo, v));
  }

  function startOfDay(ts) {
    var d = new Date(ts);
    d.setHours(0, 0, 0, 0);
    return d.getTime();
  }

  function addDays(days) {
    return startOfDay(Date.now()) + days * DAY;
  }

  /** 读取一条记录的记忆强度（旧数据没有该字段时回落到初始值） */
  function easeOf(rec) {
    var e = (rec && typeof rec.ease === 'number') ? rec.ease : EASE_START;
    return clamp(e, EASE_MIN, EASE_MAX);
  }

  /** 到期日模糊偏移：短间隔不动，避免 1 天被抖成 0 天 */
  function fuzzy(days) {
    if (!fuzzEnabled || days < 4) return days;
    var v = days * (1 + (Math.random() * 2 - 1) * FUZZ);
    return clamp(Math.round(v), 1, MAX_DAYS);
  }

  /**
   * 推算下一次间隔（天）。不修改记录，可用于预览「下次什么时候再见到这题」。
   * 调用方若要体现本次评分对 ease 的影响，应先更新 rec.ease 再调用。
   */
  function nextIntervalDays(rec, grade) {
    if (grade === 'again') return 0;

    var prev = (rec && rec.interval) || 0;
    if (grade === 'hard') {
      return prev ? Math.max(1, Math.round(prev * 0.5)) : 1;
    }

    var ease = easeOf(rec);
    var stage = (rec && rec.stage) || 0;
    var days;
    if (stage <= 0) days = 1;                          // 第 1 次答对：明天
    else if (stage === 1) days = 3;                    // 第 2 次：3 天后
    else if (stage === 2) days = Math.round(3 * ease); // 第 3 次：约 4~9 天，开始分化
    else days = Math.round(Math.max(prev, 1) * ease);  // 之后完全由记忆强度驱动

    if (grade === 'easy') days = Math.round(days * 1.4);
    days = Math.round(days * paceFactor);
    return clamp(days, 1, MAX_DAYS);
  }

  /**
   * 更新一条复习记录。
   * grade: 'good'（答对且掌握）| 'easy'（很轻松）| 'hard'（勉强/关键词匹配一般）| 'again'（答错或不熟悉）
   * isRight: 客观题判定结果，用于统计正确/错误次数；简答题按自评折算。
   */
  function apply(rec, grade, isRight) {
    var now = Date.now();
    rec.seen = (rec.seen || 0) + 1;
    rec.lastAt = now;
    if (typeof rec.ease !== 'number') rec.ease = EASE_START;

    if (isRight) {
      rec.correct = (rec.correct || 0) + 1;
      rec.lastResult = 'right';
    } else {
      rec.wrong = (rec.wrong || 0) + 1;
      rec.everWrong = true;
      rec.mastered = false;
      rec.lastResult = 'wrong';
    }

    if (grade === 'again') {
      rec.ease = clamp(rec.ease - 0.20, EASE_MIN, EASE_MAX);
      rec.stage = 0;
      rec.interval = 0;
      rec.due = startOfDay(now);       // 当天再来
      return rec;
    }

    if (grade === 'hard') {
      rec.ease = clamp(rec.ease - 0.15, EASE_MIN, EASE_MAX);
      var hd = nextIntervalDays(rec, 'hard');
      rec.stage = Math.max(0, (rec.stage || 0) - 1);
      rec.interval = hd;
      rec.due = addDays(hd);
      return rec;
    }

    if (grade === 'easy') rec.ease = clamp(rec.ease + 0.18, EASE_MIN, EASE_MAX);
    var d = fuzzy(nextIntervalDays(rec, grade));
    rec.stage = (rec.stage || 0) + 1;
    rec.interval = d;
    rec.due = addDays(d);
    return rec;
  }

  /** 该题今天是否需要复习 */
  function isDue(rec, now) {
    now = now || Date.now();
    if (!rec || !rec.seen) return false;
    if (!rec.due) return false;
    return rec.due <= startOfDay(now) + DAY - 1;
  }

  /** 用通俗语言描述下次复习时间 */
  function dueText(rec) {
    if (!rec || !rec.due) return '未安排';
    var today = startOfDay(Date.now());
    var diff = Math.round((rec.due - today) / DAY);
    if (diff <= 0) return '今天';
    if (diff === 1) return '明天';
    return diff + ' 天后';
  }

  global.SRS = {
    EASE_START: EASE_START,
    EASE_MIN: EASE_MIN,
    EASE_MAX: EASE_MAX,
    MAX_DAYS: MAX_DAYS,
    PACE_FACTORS: PACE_FACTORS,
    setPace: setPace,
    setFuzz: setFuzz,
    easeOf: easeOf,
    nextIntervalDays: nextIntervalDays,
    apply: apply,
    isDue: isDue,
    dueText: dueText,
    startOfDay: startOfDay
  };
})(window);
