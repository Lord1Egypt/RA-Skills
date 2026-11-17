#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a self-contained single-file MBTI quiz HTML page.

Usage:
    python3 build_quiz_page.py [--version quick|standard|pro] [--lang zh|en]
                               [-o quiz.html]

Reads questions.json, selects the question subset for the requested version
and emits one quiz.html with the question bank embedded as JSON and pure
vanilla JS (zero external dependencies, works offline from file://).
"""

import argparse
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data")

EXIT_DATA_ERROR = 2

# Footer badges (brand colors follow the official landing-page template)
FOOTER_BADGES = [
    # (label, background, text color, url)
    ("微信 木先生iPPT", "#07C160", "#ffffff",
     "https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA"),
    ("小红书 木先生iPPT", "#FF2442", "#ffffff",
     "https://xhslink.com/m/ESxtgUNMdl"),
    ("著作《图解团队管理》", "#BBDDE5", "#1f3a4d",
     "https://item.m.jd.com/product/14547345.html"),
    ("mu-skill集合", "#9E95B7", "#ffffff",
     "https://muippt.github.io/mu-skill-hub/"),
    ("GitHub muippt", "#181717", "#ffffff",
     "https://github.com/muippt"),
]

VERSION_FILTERS = {
    "quick": lambda q: q["version_added"] == 1,
    "standard": lambda q: q["version_added"] <= 2,
    "pro": lambda q: True,
}
EXPECTED_COUNTS = {"quick": 70, "standard": 93, "pro": 144}
VERSION_LABELS = {
    "quick": ("快速版", "Quick"),
    "standard": ("标准版", "Standard"),
    "pro": ("专业版", "Pro"),
}
DIMENSIONS = ["E/I", "S/N", "T/F", "J/P"]
DIM_POLES = {"E/I": ("E", "I"), "S/N": ("S", "N"),
             "T/F": ("T", "F"), "J/P": ("J", "P")}
POLE_LABELS = {
    "E": ("外向", "Extraversion"), "I": ("内向", "Introversion"),
    "S": ("实感", "Sensing"), "N": ("直觉", "Intuition"),
    "T": ("思考", "Thinking"), "F": ("情感", "Feeling"),
    "J": ("判断", "Judging"), "P": ("知觉", "Perceiving"),
}
DIMENSION_TITLES = {
    "E/I": ("能量方向", "Energy Orientation"),
    "S/N": ("信息获取", "Information Gathering"),
    "T/F": ("决策方式", "Decision Making"),
    "J/P": ("生活方式", "Lifestyle Orientation"),
}


def fail(msg, code=EXIT_DATA_ERROR):
    sys.stderr.write("ERROR: %s\n" % msg)
    sys.exit(code)


def main():
    parser = argparse.ArgumentParser(description="Build single-file MBTI quiz page.")
    parser.add_argument("--version", choices=sorted(VERSION_FILTERS), default="quick",
                        help="quiz version (default: quick)")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh",
                        help="initial question language (default: zh)")
    parser.add_argument("-o", "--output", default="quiz.html",
                        help="output HTML path (default: ./quiz.html)")
    args = parser.parse_args()

    qpath = os.path.join(DATA_DIR, "questions.json")
    if not os.path.isfile(qpath):
        fail("question bank not found: %s" % qpath)
    with open(qpath, "r", encoding="utf-8") as fh:
        questions = json.load(fh)
    subset = [q for q in questions if VERSION_FILTERS[args.version](q)]
    expected = EXPECTED_COUNTS[args.version]
    if len(subset) != expected:
        fail("version '%s' selected %d questions, expected %d"
             % (args.version, len(subset), expected))
    subset.sort(key=lambda q: q["id"])

    quiz_data = {
        "version": args.version,
        "lang": args.lang,
        "versionZh": VERSION_LABELS[args.version][0],
        "versionEn": VERSION_LABELS[args.version][1],
        "total": len(subset),
        "dimensions": [
            {"dim": dim,
             "titleZh": DIMENSION_TITLES[dim][0], "titleEn": DIMENSION_TITLES[dim][1],
             "poles": [{"code": p, "zh": POLE_LABELS[p][0], "en": POLE_LABELS[p][1]}
                       for p in DIM_POLES[dim]]}
            for dim in DIMENSIONS
        ],
        "questions": [
            {"id": q["id"], "dimension": q["dimension"],
             "zh": q["question_zh"], "en": q["question_en"],
             "a": {"zh": q["choice_a"]["text_zh"], "en": q["choice_a"]["text_en"]},
             "b": {"zh": q["choice_b"]["text_zh"], "en": q["choice_b"]["text_en"]}}
            for q in subset
        ],
    }
    payload = json.dumps(quiz_data, ensure_ascii=False, separators=(",", ":"))
    # Guard against accidental </script> termination inside the payload.
    payload = payload.replace("</", "<\\/")

    html_text = build_html(quiz_data, payload)
    out_dir = os.path.dirname(os.path.abspath(args.output))
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(html_text)
    print("quiz page written: %s (%d bytes, version=%s, %d questions, lang=%s)"
          % (os.path.abspath(args.output), os.path.getsize(args.output),
             args.version, len(subset), args.lang))


def build_html(cfg, payload):
    title = "MBTI 职业性格测评 / MBTI Personality Quiz"
    css = """
:root { --navy:#8A315F; --blue:#AF4283; --light:#FAEDF3; --line:#E8C6D6;
        --muted:#6b7280; --ok:#2a9d8f; }
* { box-sizing:border-box; -webkit-tap-highlight-color:transparent; }
html,body { margin:0; padding:0; height:100%; }
body { font-family:'PingFang SC','Microsoft YaHei','Noto Sans CJK SC',
       'Hiragino Sans GB','Heiti SC',-apple-system,'Segoe UI',Roboto,sans-serif;
       background:#F9EDF3; color:#22262e; }
#app { max-width:640px; margin:0 auto; min-height:100%;
       display:flex; flex-direction:column; background:#fff; }
header { padding:14px 18px 10px; border-bottom:1px solid var(--line);
         background:var(--light); }
.head-row { display:flex; justify-content:space-between; align-items:center; }
.brand { font-weight:700; color:var(--navy); font-size:15px; }
.brand .sub { font-weight:400; color:var(--muted); font-size:11px; margin-left:6px; }
#langBtn { border:1px solid var(--blue); background:#fff; color:var(--blue);
           border-radius:14px; padding:4px 12px; font-size:12px; cursor:pointer; }
#langBtn:active { background:var(--blue); color:#fff; }
.progress-wrap { margin-top:10px; }
.progress-meta { display:flex; justify-content:space-between; font-size:12px;
                 color:var(--muted); margin-bottom:4px; }
.progress-track { height:8px; background:#EDDDE7; border-radius:4px; overflow:hidden; }
.progress-fill { height:100%; width:0%; background:linear-gradient(90deg,
                 var(--blue), var(--navy)); border-radius:4px;
                 transition:width .25s ease; }
main { flex:1; padding:26px 20px 30px; display:flex; flex-direction:column; }
.q-dim { font-size:12px; color:var(--muted); margin-bottom:8px; }
.q-text { font-size:19px; font-weight:600; line-height:1.5; margin-bottom:26px;
          min-height:64px; }
.choices { display:flex; flex-direction:column; gap:14px; }
.choice { display:block; width:100%; text-align:left; border:2px solid var(--line);
          background:#fff; border-radius:12px; padding:16px 18px; font-size:16px;
          line-height:1.45; cursor:pointer; transition:border-color .15s,
          background .15s; font-family:inherit; }
.choice .tag { display:inline-block; font-size:11px; font-weight:700; color:#fff;
               background:var(--blue); border-radius:4px; padding:1px 7px;
               margin-right:8px; vertical-align:2px; }
.choice:active, .choice:hover { border-color:var(--blue); background:var(--light); }
.choice.selected { border-color:var(--navy); background:var(--light); }
.nav-row { display:flex; justify-content:space-between; margin-top:22px; }
.btn { border:none; border-radius:10px; padding:10px 20px; font-size:14px;
       cursor:pointer; font-family:inherit; }
.btn-secondary { background:#EDDDE7; color:#374151; }
.btn-secondary:disabled { opacity:.4; cursor:default; }
.btn-primary { background:var(--navy); color:#fff; }
#resultView, #summaryView { display:none; }
.summary-card { background:var(--light); border:1px solid var(--line);
                border-radius:12px; padding:16px; margin-bottom:16px; }
.summary-card h3 { margin:0 0 10px; font-size:15px; color:var(--navy); }
.dim-row { margin-bottom:12px; }
.dim-label { display:flex; justify-content:space-between; font-size:13px;
             margin-bottom:4px; }
.bar { display:flex; height:10px; border-radius:5px; overflow:hidden;
       background:#EDDDE7; }
.bar .seg { height:100%; }
.seg.a { background:#D9A5C0; } .seg.b { background:var(--blue); }
.nickname-row { margin:14px 0; }
.nickname-row label { font-size:13px; color:var(--muted); display:block;
                      margin-bottom:6px; }
.nickname-row input { width:100%; border:1px solid var(--line); border-radius:8px;
                      padding:10px 12px; font-size:14px; font-family:inherit; }
.hint { font-size:12px; color:var(--muted); line-height:1.6; margin-top:12px; }
.done-title { text-align:center; font-size:22px; font-weight:700;
              color:var(--navy); margin:10px 0 18px; }
footer { padding:10px 18px 16px; font-size:11px; color:var(--muted);
         text-align:center; border-top:1px solid var(--line); }
.badge-row { display:flex; justify-content:center; flex-wrap:wrap; gap:6px;
             margin-bottom:8px; }
.badge-row a { display:inline-block; font-size:11px; font-weight:600;
               border-radius:10px; padding:2px 9px; text-decoration:none;
               white-space:nowrap; line-height:1.5; }
.badge-row a:active, .badge-row a:hover { opacity:.85; }
@media (max-width:480px) { .q-text { font-size:17px; } main { padding:20px 16px 24px; } }
"""
    script = r"""
(function () {
  'use strict';
  var QUIZ = window.__MBTI_QUIZ__;
  var STORE_KEY = 'mbti_quiz_progress_' + QUIZ.version;
  var state = {
    lang: QUIZ.lang,
    index: 0,
    answers: {},        // question id -> 'A' | 'B'
    submitted: false
  };
  var els = {};

  function $(id) { return document.getElementById(id); }

  function dimTitle(d) {
    var zh = state.lang === 'zh';
    return (zh ? d.titleZh : d.titleEn) + ' / ' + (zh ? d.titleEn : d.titleZh);
  }

  function t(obj) { return obj[state.lang === 'zh' ? 'zh' : 'en']; }

  function saveProgress() {
    try {
      localStorage.setItem(STORE_KEY, JSON.stringify({
        index: state.index, answers: state.answers, submitted: state.submitted
      }));
    } catch (e) { /* storage unavailable: proceed without resume */ }
  }

  function loadProgress() {
    try {
      var raw = localStorage.getItem(STORE_KEY);
      if (!raw) { return null; }
      var data = JSON.parse(raw);
      if (data && typeof data === 'object' && data.answers) { return data; }
    } catch (e) { /* ignore corrupted state */ }
    return null;
  }

  function clearProgress() {
    try { localStorage.removeItem(STORE_KEY); } catch (e) { /* noop */ }
  }

  function render() {
    if (state.submitted) { renderSummary(); return; }
    els.quizView.style.display = 'flex';
    els.resultView.style.display = 'none';
    var q = QUIZ.questions[state.index];
    var answered = Object.keys(state.answers).length;
    els.progressFill.style.width =
      (answered / QUIZ.total * 100).toFixed(1) + '%';
    els.counter.textContent =
      (state.lang === 'zh' ? '第 ' + (state.index + 1) + ' / ' + QUIZ.total + ' 题'
                           : 'Question ' + (state.index + 1) + ' / ' + QUIZ.total);
    var dim = QUIZ.dimensions.filter(function (d) { return d.dim === q.dimension; })[0];
    els.qDim.textContent = '◈ ' + dimTitle(dim);
    els.qText.textContent = t(q);
    ['a', 'b'].forEach(function (key) {
      var btn = key === 'a' ? els.choiceA : els.choiceB;
      btn.querySelector('.choice-text').textContent = t(q[key]);
      var picked = state.answers[q.id] === key.toUpperCase();
      btn.classList.toggle('selected', picked);
    });
    els.prevBtn.disabled = state.index === 0;
    var isLast = state.index === QUIZ.questions.length - 1;
    els.nextBtn.textContent = isLast
      ? (state.lang === 'zh' ? '提交 / Submit' : 'Submit / 提交') : '→';
    els.nextBtn.disabled = false;
    els.nextBtn.style.visibility = isLast ? 'visible' : 'hidden';
  }

  function pick(choice) {
    var q = QUIZ.questions[state.index];
    state.answers[q.id] = choice;
    saveProgress();
    if (state.index < QUIZ.questions.length - 1) {
      state.index += 1;
      render();
    } else {
      render(); // last question: let user press Submit (or re-pick)
    }
  }

  function prev() {
    if (state.index > 0) { state.index -= 1; render(); }
  }

  function next() {
    var unanswered = QUIZ.questions.length - Object.keys(state.answers).length;
    if (unanswered > 0) {
      alert(state.lang === 'zh'
        ? '还有 ' + unanswered + ' 题未作答，请回退补答后再提交。'
        : unanswered + ' question(s) unanswered. Go back and complete them first.');
      return;
    }
    state.submitted = true;
    saveProgress();
    renderSummary();
  }

  function dimCounts() {
    var counts = {};
    QUIZ.questions.forEach(function (q) {
      counts[q.dimension] = counts[q.dimension] || { A: 0, B: 0 };
      counts[q.dimension][state.answers[q.id]] += 1;
    });
    return counts;
  }

  function renderSummary() {
    els.quizView.style.display = 'none';
    els.resultView.style.display = 'block';
    var zh = state.lang === 'zh';
    els.doneTitle.textContent = zh ? '答题完成！' : 'Quiz completed!';
    var html = '';
    var counts = dimCounts();
    QUIZ.dimensions.forEach(function (d) {
      var c = counts[d.dim];
      var total = c.A + c.B;
      var pctA = total ? Math.round(c.A / total * 100) : 50;
      html += '<div class="dim-row"><div class="dim-label">' +
        '<span>◈ ' + dimTitle(d) + '</span>' +
        '<span>A: ' + c.A + ' &nbsp; B: ' + c.B + '</span></div>' +
        '<div class="bar"><div class="seg a" style="width:' + pctA + '%">' +
        '</div><div class="seg b" style="width:' + (100 - pctA) + '%"></div></div></div>';
    });
    els.summaryDims.innerHTML = html;
  }

  function getAnswersDoc() {
    var answers = QUIZ.questions.map(function (q) {
      return { id: q.id, choice: state.answers[q.id] };
    });
    return {
      version: QUIZ.version,
      nickname: (els.nicknameInput.value || '').trim(),
      answers: answers
    };
  }

  function download() {
    var doc = getAnswersDoc();
    var ts = new Date();
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var stamp = ts.getFullYear() + pad(ts.getMonth() + 1) + pad(ts.getDate()) +
      '_' + pad(ts.getHours()) + pad(ts.getMinutes()) + pad(ts.getSeconds());
    var blob = new Blob([JSON.stringify(doc, null, 2)],
                        { type: 'application/json' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'mbti_answers_' + QUIZ.version + '_' + stamp + '.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    els.downloadHint.style.display = 'block';
  }

  function copyAnswers() {
    var doc = getAnswersDoc();
    var text = JSON.stringify(doc);
    var ok = false;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { ok = true; })
        .catch(function () { ok = false; });
    }
    // Fallback: select textarea
    els.copyArea.value = text;
    els.copyArea.style.display = 'block';
    els.copyArea.select();
    els.copyArea.setSelectionRange(0, text.length);
    try {
      document.execCommand('copy');
      ok = true;
    } catch (e) { /* noop */ }
    var zh = state.lang === 'zh';
    els.copyHint.textContent = ok
      ? (zh ? '已复制到剪贴板，直接粘贴给 AI 助手即可'
            : 'Copied to clipboard. Paste it to your AI assistant.')
      : (zh ? '请手动全选下方文本框内容并复制'
            : 'Please manually select and copy the text below.');
    els.copyHint.style.display = 'block';
  }

  function restart() {
    if (!confirm(state.lang === 'zh' ? '重新开始将清除当前进度，确定？'
                                     : 'Restart will clear current progress. OK?')) {
      return;
    }
    clearProgress();
    state.index = 0; state.answers = {}; state.submitted = false;
    render();
  }

  function toggleLang() {
    state.lang = state.lang === 'zh' ? 'en' : 'zh';
    els.langBtn.textContent = state.lang === 'zh' ? 'EN' : '中文';
    render();
  }

  function init() {
    els = {
      quizView: $('quizView'), resultView: $('resultView'),
      progressFill: $('progressFill'), counter: $('counter'),
      qDim: $('qDim'), qText: $('qText'),
      choiceA: $('choiceA'), choiceB: $('choiceB'),
      prevBtn: $('prevBtn'), nextBtn: $('nextBtn'),
      langBtn: $('langBtn'), doneTitle: $('doneTitle'),
      summaryDims: $('summaryDims'), nicknameInput: $('nicknameInput'),
      downloadBtn: $('downloadBtn'), restartBtn: $('restartBtn'),
      downloadHint: $('downloadHint'),
      copyBtn: $('copyBtn'), copyHint: $('copyHint'), copyArea: $('copyArea')
    };
    els.langBtn.addEventListener('click', toggleLang);
    els.langBtn.textContent = state.lang === 'zh' ? 'EN' : '中文';
    els.choiceA.addEventListener('click', function () { pick('A'); });
    els.choiceB.addEventListener('click', function () { pick('B'); });
    els.prevBtn.addEventListener('click', prev);
    els.nextBtn.addEventListener('click', next);
    els.downloadBtn.addEventListener('click', download);
    els.copyBtn.addEventListener('click', copyAnswers);
    els.restartBtn.addEventListener('click', restart);

    var saved = loadProgress();
    if (saved && !saved.submitted &&
        Object.keys(saved.answers || {}).length > 0 &&
        Object.keys(saved.answers || {}).length < QUIZ.total) {
      var msg = state.lang === 'zh'
        ? '检测到未完成的答题进度（已答 ' + Object.keys(saved.answers).length +
          '/' + QUIZ.total + ' 题），是否继续？'
        : 'Unfinished progress detected (' +
          Object.keys(saved.answers).length + '/' + QUIZ.total +
          ' answered). Resume?';
      if (confirm(msg)) {
        state.answers = saved.answers;
        state.index = Math.min(saved.index || 0, QUIZ.total - 1);
      } else {
        clearProgress();
      }
    }
    render();
  }

  document.addEventListener('DOMContentLoaded', init);
})();
"""
    return """<!DOCTYPE html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(title)s</title>
<style>%(css)s</style>
</head>
<body>
<div id="app">
  <header>
    <div class="head-row">
      <div class="brand">MBTI%(sub)s</div>
      <button id="langBtn" type="button">EN</button>
    </div>
    <div class="progress-wrap">
      <div class="progress-meta"><span id="counter"></span><span id="versionLabel">%(version_label)s</span></div>
      <div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
    </div>
  </header>
  <main id="quizView" style="display:flex;flex-direction:column;">
    <div class="q-dim" id="qDim"></div>
    <div class="q-text" id="qText"></div>
    <div class="choices">
      <button class="choice" id="choiceA" type="button"><span class="tag">A</span><span class="choice-text"></span></button>
      <button class="choice" id="choiceB" type="button"><span class="tag">B</span><span class="choice-text"></span></button>
    </div>
    <div class="nav-row">
      <button class="btn btn-secondary" id="prevBtn" type="button">← %(prev)s</button>
      <button class="btn btn-primary" id="nextBtn" type="button" style="visibility:hidden"></button>
    </div>
  </main>
  <main id="resultView">
    <div class="done-title" id="doneTitle"></div>
    <div class="summary-card">
      <h3>%(summary_title)s</h3>
      <div id="summaryDims"></div>
    </div>
    <div class="nickname-row">
      <label for="nicknameInput">%(nick_label)s</label>
      <input id="nicknameInput" type="text" maxlength="40" placeholder="%(nick_ph)s">
    </div>
    <div class="nav-row">
      <button class="btn btn-secondary" id="restartBtn" type="button">%(restart)s</button>
      <button class="btn btn-primary" id="copyBtn" type="button">%(copy)s</button>
      <button class="btn btn-primary" id="downloadBtn" type="button">%(download)s</button>
    </div>
    <div class="hint" id="copyHint" style="display:none;">%(copy_hint)s</div>
    <textarea id="copyArea" readonly style="display:none; width:100%%; height:80px; margin-top:8px; font-size:11px; border:1px solid var(--line); border-radius:8px; padding:6px;"></textarea>
    <div class="hint" id="downloadHint" style="display:none;">%(hint)s</div>
  </main>
  <footer>
    <div class="badge-row">%(badges)s</div>
    MBTI Personality &amp; Career Quiz · %(version_label)s · %(footer)s
  </footer>
</div>
<script>window.__MBTI_QUIZ__ = %(payload)s;</script>
<script>%(script)s</script>
</body>
</html>
""" % {
        "lang": cfg["lang"],
        "title": title,
        "css": css,
        "badges": "".join(
            '<a href="%s" target="_blank" rel="noopener" '
            'style="background:%s;color:%s">%s</a>' % (url, bg, fg, label)
            for label, bg, fg, url in FOOTER_BADGES),
        "payload": payload,
        "script": script,
        "sub": " · %s %s" % (cfg["versionZh"], cfg["versionEn"]),
        "version_label": "%s %s · %d题 / %d items" % (
            cfg["versionZh"], cfg["versionEn"], cfg["total"], cfg["total"]),
        "prev": "上一题 / Prev" if cfg["lang"] == "zh" else "Prev / 上一题",
        "summary_title": ("各维度选项计数 / Choice Counts per Dimension"
                          if cfg["lang"] == "zh" else
                          "Choice Counts per Dimension / 各维度选项计数"),
        "nick_label": ("昵称（可选，会写入答案文件）/ Nickname (optional)"
                       if cfg["lang"] == "zh" else
                       "Nickname (optional, saved into the answers file) / 昵称（可选）"),
        "nick_ph": ("你的昵称 / Your nickname" if cfg["lang"] == "zh"
                    else "Your nickname / 你的昵称"),
        "restart": ("重新开始 / Restart" if cfg["lang"] == "zh"
                    else "Restart / 重新开始"),
        "download": ("下载答案 JSON / Download answers" if cfg["lang"] == "zh"
                     else "Download answers JSON / 下载答案"),
        "copy": ("复制答案给 AI / Copy for AI" if cfg["lang"] == "zh"
                 else "Copy for AI / 复制答案给 AI"),
        "copy_hint": ("点击复制后，把内容直接粘贴给 AI 助手，即可生成 PDF 报告。"
                      if cfg["lang"] == "zh" else
                      "After copying, paste the content directly to your AI "
                      "assistant to generate the PDF report."),
        "hint": ("答案文件已下载（mbti_answers_%s_<时间戳>.json）。"
                 "把此文件交给 AI 助手生成 PDF 报告。"
                 % cfg["version"]
                 if cfg["lang"] == "zh" else
                 "Answers file downloaded (mbti_answers_%s_<timestamp>.json). "
                 "Hand this file to your AI assistant to generate the PDF report."
                 % cfg["version"]),
        "footer": ("此页面为离线单文件版，进度自动保存在本浏览器。"
                   if cfg["lang"] == "zh" else
                   "Offline single-file page; progress is saved in this browser."),
    }


if __name__ == "__main__":
    main()
