#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NPC 觉醒 · 单文件点选页生成器

  python -X utf8 scripts/build_quiz_html.py --out npc-demo.html
  python -X utf8 scripts/build_quiz_html.py --verify      # JS 与 Python 引擎对拍（需 node）
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
AXES = ["script", "route", "goal", "voice", "echo", "reset", "serve"]
AXIS_CN = {"script": "台词", "route": "路线", "goal": "目标",
           "voice": "表达", "echo": "回声", "reset": "重置", "serve": "服务"}

TPL = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>NPC 觉醒 · 检测程序</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#f5f6f3; --panel:#ffffff; --card:#ffffff; --panel-hi:#eef1ec;
  --line:#e0e5dd; --line2:#c2ccc0; --track:#e9ece6;
  --fg:#2a332c; --fg-strong:#151d17; --say-fg:#2f3a32; --quote-fg:#1b2a20;
  --quote-bg:#eff4ee; --dim:#7a857c;
  --accent:#15803d; --accent-soft:#e8f4ea;
  --hot:#c2410c; --warn:#a16207; --warn-fg:#7c4a03; --warn-bg:#fdf7e6;
}
/* 系统深色 → 深色终端；用户显式选择优先 */
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
  --bg:#0b0f14; --panel:#10161d; --card:#0d1219; --panel-hi:#131b24;
  --line:#1d2836; --line2:#2a3a4d; --track:#151d27;
  --fg:#c6d4e1; --fg-strong:#dbe7f3; --say-fg:#cddaea; --quote-fg:#e6eef7;
  --quote-bg:#111823; --dim:#63748a;
  --accent:#4ade80; --accent-soft:#0f1a16;
  --hot:#f0883e; --warn:#f0c674; --warn-fg:#f0dfb8; --warn-bg:#161307;
  }
}
:root[data-theme="dark"]{
  --bg:#0b0f14; --panel:#10161d; --card:#0d1219; --panel-hi:#131b24;
  --line:#1d2836; --line2:#2a3a4d; --track:#151d27;
  --fg:#c6d4e1; --fg-strong:#dbe7f3; --say-fg:#cddaea; --quote-fg:#e6eef7;
  --quote-bg:#111823; --dim:#63748a;
  --accent:#4ade80; --accent-soft:#0f1a16;
  --hot:#f0883e; --warn:#f0c674; --warn-fg:#f0dfb8; --warn-bg:#161307;
}
html,body{height:100%}
body{
  background:var(--bg); color:var(--fg);
  font:14px/1.75 ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;
  -webkit-font-smoothing:antialiased;
  padding:20px 16px 48px;
}
#app{max-width:600px;margin:0 auto}
.rule{height:1px;background:var(--line);margin:14px 0}
.top{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--dim);letter-spacing:.08em}
.sys{color:var(--accent)}
.sys .pfx{color:var(--dim)}
.lead{color:var(--fg);line-height:1.9}
.lead .muted{color:var(--dim)}
.qno{color:var(--dim);font-size:12px;letter-spacing:.1em;margin-bottom:6px}
.qtext{font-size:15px;line-height:1.8;margin-bottom:16px;color:var(--fg-strong)}
.opt{
  display:block;width:100%;text-align:left;cursor:pointer;
  background:var(--panel);border:1px solid var(--line);border-radius:8px;
  padding:12px 14px;margin-bottom:9px;color:var(--fg);
  font:inherit;line-height:1.6;transition:border-color .12s,background .12s,transform .08s;
}
.opt:hover{border-color:var(--line2);background:var(--panel-hi)}
.opt:active{transform:scale(.995)}
.opt .k{color:var(--accent);margin-right:8px;font-weight:500}
.opt.sel{border-color:var(--accent);background:var(--accent-soft)}
.opt.sel .k{color:var(--accent)}
.bar{height:2px;background:var(--line);border-radius:2px;overflow:hidden;margin:16px 0 20px}
.bar i{display:block;height:100%;background:var(--accent);width:0;transition:width .25s}
.act{display:flex;gap:10px;margin-top:18px;flex-wrap:wrap}
button.btn{
  cursor:pointer;font:inherit;border-radius:8px;padding:10px 18px;
  background:transparent;border:1px solid var(--line2);color:var(--fg);
  transition:border-color .12s,color .12s;
}
button.btn:hover{border-color:var(--accent);color:var(--accent)}
button.btn.pri{border-color:var(--accent);color:var(--accent)}
button.btn.pri:hover{background:var(--accent-soft)}
button.btn:disabled{opacity:.35;cursor:not-allowed;border-color:var(--line);color:var(--dim)}
.hint{color:var(--dim);font-size:12px;margin-top:14px;line-height:1.7}
.card{border:1px solid var(--line);border-radius:12px;padding:20px 18px;background:var(--card)}
.crow{display:flex;gap:14px;margin-bottom:5px;font-size:13px}
.crow .cl{color:var(--dim);width:38px;flex:none}
.type{font-size:24px;color:var(--accent);letter-spacing:.06em;font-weight:500}
.conc{font-size:13px;color:var(--fg);margin-left:10px}
.coord{color:var(--dim);font-size:12.5px;letter-spacing:.03em;margin-top:6px}
.sec{color:var(--dim);font-size:11.5px;letter-spacing:.14em;margin:18px 0 9px}
.line{color:var(--quote-fg);background:var(--quote-bg);border-left:2px solid var(--accent);
      padding:10px 13px;border-radius:0 6px 6px 0;line-height:1.7}
.say{line-height:2;color:var(--say-fg)}
.say p{margin-bottom:3px}
.ax{display:flex;align-items:center;gap:10px;margin-bottom:7px;font-size:12.5px}
.ax .an{color:var(--dim);width:34px;flex:none}
.ax .at{flex:1;height:5px;background:var(--track);border-radius:3px;overflow:hidden}
.ax .at i{display:block;height:100%;border-radius:3px}
.ax .av{width:30px;text-align:right;color:var(--dim);flex:none}
.quest{display:flex;gap:9px;margin-bottom:11px;line-height:1.8}
.quest .qn{flex:none;width:17px;height:17px;border-radius:50%;background:var(--accent-soft);
  color:var(--accent);font-size:11px;display:flex;align-items:center;justify-content:center;margin-top:4px}
.foot{color:var(--dim);font-size:11.5px;line-height:1.8;margin-top:16px}
.exit{border:1px solid var(--warn);border-radius:10px;padding:16px;margin-top:18px;
  color:var(--warn-fg);line-height:1.9;background:var(--warn-bg)}
.exit .et{color:var(--warn);font-size:11.5px;letter-spacing:.14em;margin-bottom:10px}
.toast{position:fixed;left:50%;bottom:28px;transform:translateX(-50%);
  background:var(--accent-soft);border:1px solid var(--accent);color:var(--accent);
  padding:9px 18px;border-radius:8px;font-size:13px;opacity:0;pointer-events:none;
  transition:opacity .2s}
.toast.on{opacity:1}
.theme{position:fixed;right:14px;bottom:14px;z-index:9;
  cursor:pointer;font:inherit;font-size:11px;letter-spacing:.06em;
  background:var(--panel);border:1px solid var(--line2);color:var(--dim);
  padding:6px 11px;border-radius:6px;transition:color .12s,border-color .12s}
.theme:hover{color:var(--accent);border-color:var(--accent)}
@media(max-width:420px){.type{font-size:21px}.qtext{font-size:14.5px}}
</style>
</head>
<body>
<div id="app"></div>
<button id="theme" class="theme" type="button">☾ 深色</button>
<div class="toast" id="toast"></div>
<script>
const DATA = __DATA__;
const AX = DATA.axes, AC = DATA.axis_cn, Q = DATA.questions, T = DATA.types, M = DATA.meta;
const A = M.calibration.anchors, ST = M.calibration.stats;

/* ---------- 引擎（与 npc.py 同源） ---------- */
function rawScores(picks){
  const r = {}; AX.forEach(k => r[k] = 0);
  picks.forEach((oi, i) => {
    const w = Q[i].options[oi].weights;
    for (const k in w) r[k] += w[k];
  });
  return r;
}
function normalize(r){
  const o = {};
  AX.forEach(k => {
    const a = A[k], span = Math.max(a.high - a.low, 1);
    o[k] = Math.max(0, Math.min(100, (r[k] - a.low) / span * 100));
  });
  return o;
}
function discScores(s){
  const o = {};
  T.types.forEach(t => {
    let sum = 0, n = 0;
    for (const k in t.disc){ sum += t.disc[k] * (s[k] - ST[k].mean) / ST[k].std; n++; }
    o[t.key] = sum / n;
  });
  return o;
}
function classify(s){
  const c = T.rare.condition;
  if (s.goal < c.goal && s.voice < c.voice && s.echo < c.echo) return T.rare;
  const ds = discScores(s);
  let bk = null, bv = -1e18;
  T.types.forEach(t => { if (ds[t.key] > bv){ bv = ds[t.key]; bk = t.key; } });
  return T.types.find(t => t.key === bk);
}
function concentration(s){
  const v = AX.map(k => s[k]);
  const avg = v.reduce((a,b)=>a+b,0) / v.length;
  return Math.round(0.6 * avg + 0.4 * Math.max.apply(null, v));
}
const CRCT = (function(){
  const t = [];
  for (let i = 0; i < 256; i++){
    let c = i;
    for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    t[i] = c >>> 0;
  }
  return t;
})();
function crc32(str){
  const b = new TextEncoder().encode(str);
  let c = 0xFFFFFFFF;
  for (let i = 0; i < b.length; i++) c = CRCT[(c ^ b[i]) & 0xFF] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}
function pseudo(seed, salt, lo, hi){
  let h = (Math.imul(seed, 1103515245) + Math.imul(salt, 12345) + 1013904223) >>> 0;
  h = h % 2147483647;
  return lo + h % (hi - lo + 1);
}
function fillNums(s, seed){
  const n1 = pseudo(seed, 1, 180, 340);
  const n2 = Math.floor(n1 * pseudo(seed, 2, 84, 93) / 100);
  const p1 = pseudo(seed, 3, 4, 11);
  return s.split('{n1}').join(n1.toLocaleString('en-US'))
          .split('{n2}').join(n2.toLocaleString('en-US'))
          .split('{p1}').join(String(p1));
}
function coordOf(s, stance){
  const c = crc32(s);
  return M.zones[c % M.zones.length] + ' · 第 ' + String(c % 10000 + 1).padStart(4,'0') + ' 号刷新点 · ' + stance;
}
function esc(s){ return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

/* ---------- 主题 ---------- */
function systemTheme(){
  return (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
    ? 'dark' : 'light';
}
function activeTheme(){
  return document.documentElement.getAttribute('data-theme') || systemTheme();
}
function syncThemeBtn(){
  const b = document.getElementById('theme');
  if (b) b.textContent = activeTheme() === 'dark' ? '☀ 浅色' : '☾ 深色';
}
function setTheme(t){
  document.documentElement.setAttribute('data-theme', t);
  try { localStorage.setItem('npc-theme', t); } catch(e){}
  syncThemeBtn();
}
try {
  const saved = localStorage.getItem('npc-theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);
} catch(e){}
document.getElementById('theme').onclick = function(){
  setTheme(activeTheme() === 'dark' ? 'light' : 'dark');
};
syncThemeBtn();

/* ---------- 渲染 ---------- */
const app = document.getElementById('app');
let cur = 0, ans = new Array(Q.length).fill(-1), last = null;

function rule(){ return '<div class="rule"></div>'; }
function topBar(right){
  return '<div class="top"><span>NPC 觉醒 · 检测程序 v1.0</span><span>' + right + '</span></div>';
}
function renderIntro(){
  app.innerHTML = topBar('READY') + rule() +
    M.opening.map(s => {
      const i = s.indexOf(']');
      return '<div class="sys"><span class="pfx">' + esc(s.slice(0, i + 1)) + '</span>' + esc(s.slice(i + 1)) + '</div>';
    }).join('') +
    rule() +
    '<div class="lead">' + Q.length + ' 道题。没有正确答案，只有你的日志。<br>' +
    '<span class="muted">一屏一题，点选即记，可以回退。</span></div>' +
    '<div class="act"><button class="btn pri" id="go">开始检测</button></div>' +
    '<div class="hint">本检测不联网、不上传、不留档。你答完，结果只在你手里。</div>';
  document.getElementById('go').onclick = () => { cur = 0; renderQ(); };
}
function renderQ(){
  const q = Q[cur];
  app.innerHTML = topBar(String(cur + 1).padStart(2,'0') + ' / ' + Q.length) + rule() +
    '<div class="qno">Q' + String(cur + 1).padStart(2,'0') + '</div>' +
    '<div class="qtext">' + esc(q.text) + '</div>' +
    q.options.map((o, i) =>
      '<button class="opt' + (ans[cur] === i ? ' sel' : '') + '" data-i="' + i + '">' +
      '<span class="k">' + o.id + '</span>' + esc(o.text) + '</button>').join('') +
    '<div class="bar"><i style="width:' + (cur / Q.length * 100) + '%"></i></div>' +
    '<div class="act">' +
      '<button class="btn" id="prev"' + (cur === 0 ? ' disabled' : '') + '>上一题</button>' +
      (cur === Q.length - 1
        ? '<button class="btn pri" id="sub"' + (ans[cur] < 0 ? ' disabled' : '') + '>提交判定</button>'
        : '<button class="btn" id="next"' + (ans[cur] < 0 ? ' disabled' : '') + '>下一题</button>') +
    '</div>';
  app.querySelectorAll('.opt').forEach(b => b.onclick = () => {
    ans[cur] = +b.dataset.i;
    if (cur < Q.length - 1){ setTimeout(() => { cur++; renderQ(); }, 170); }
    else { renderQ(); }
  });
  const p = document.getElementById('prev');
  if (p) p.onclick = () => { if (cur > 0){ cur--; renderQ(); } };
  const n = document.getElementById('next');
  if (n) n.onclick = () => { if (ans[cur] >= 0 && cur < Q.length - 1){ cur++; renderQ(); } };
  const s = document.getElementById('sub');
  if (s) s.onclick = () => { if (ans.every(v => v >= 0)) renderCard(); };
}
function renderCard(){
  const picks = ans.slice();
  const s = normalize(rawScores(picks));
  const t = classify(s);
  const conc = concentration(s);
  const seed = crc32(picks.map((oi, i) => Q[i].options[oi].id).join(''));
  const isRare = t.key === 'not_npc';
  last = {s: s, t: t, conc: conc, seed: seed, isRare: isRare, picks: picks};

  let h = rule() + '<div class="card">';
  h += '<div class="top"><span>NPC 觉醒 · 检测报告</span><span>卷 01</span></div>' + rule();
  h += '<div class="crow"><span class="cl">类型</span><span class="type">' + t.name + '</span>' +
       (isRare ? '' : '<span class="conc">NPC 浓度 <b style="color:var(--accent)">' + conc + '%</b></span>') + '</div>';
  h += '<div class="coord">' + esc(coordOf(picks.map((oi, i) => Q[i].options[oi].id).join(''), t.stance)) + '</div>';
  h += rule();
  if (!isRare && t.line && t.line !== '——'){
    h += '<div class="sec">固 定 台 词</div><div class="line">' + esc(t.line) + '</div>';
  }
  h += '<div class="sec">系 统 留 言</div><div class="say">' +
       t.verdict.map(x => '<p>' + esc(fillNums(x, seed)) + '</p>').join('') + '</div>';
  h += rule() + '<div class="sec">参 数 面 板</div>' + AX.map(k => {
    const v = s[k], hot = v >= 60;
    return '<div class="ax"><span class="an">' + AC[k] + '</span>' +
      '<span class="at"><i style="width:' + v.toFixed(0) + '%;background:' +
      (hot ? 'var(--hot)' : 'var(--dim)') + '"></i></span>' +
      '<span class="av">' + v.toFixed(0) + '</span></div>';
  }).join('');
  h += rule() + '<div class="sec">破 局 支 线</div>' +
       t.quests.map((x, i) => '<div class="quest"><span class="qn">' + (i + 1) + '</span><span>' +
         esc(fillNums(x, seed + i + 1)) + '</span></div>').join('');
  h += rule();
  h += '<div class="foot">' + (isRare
        ? '你不是 NPC。这张卡很少出，记一下日期。'
        : '不是性格标签，是机制诊断。<br>要动的不是你自己，是上面那几条参数。') + '</div>';
  h += '<div class="foot" style="margin-top:10px;opacity:.75">' + esc(M.disclaimer) + '</div>';
  h += '</div>';

  if (!isRare && conc >= M.exit_rule.concentration_min && s.echo >= M.exit_rule.echo_min){
    h += '<div class="exit"><div class="et">系 统 收 起 玩 笑 了</div>' +
         M.exit_text.map(x => '<p>' + esc(x.replace(/^\[系统\]\s*/, '')) + '</p>').join('') + '</div>';
  }

  h += '<div class="act"><button class="btn pri" id="cp">复制完整卡</button>' +
       '<button class="btn" id="again">再测一次</button></div>' +
       '<div class="hint">这张卡的判定由你的答案确定性生成——同样的答案，永远得到同一张卡。</div>';

  app.innerHTML = h;
  window.scrollTo(0, 0);
  document.getElementById('again').onclick = () => {
    ans = new Array(Q.length).fill(-1); cur = 0; renderIntro();
  };
  document.getElementById('cp').onclick = copyCard;
}
function textCard(){
  const L = last, w = 48;
  const R = '─'.repeat(w + 6);
  const num = L.picks.map((oi, i) => Q[i].options[oi].id).join('');
  let o = [R, pad('NPC 觉醒 · 检测报告'), R];
  o.push(' 类型    ' + L.t.name);
  if (!L.isRare) o.push(' 浓度    ' + L.conc + '%');
  o.push(' 坐标    ' + coordOf(num, L.t.stance));
  o.push(R);
  if (!L.isRare && L.t.line && L.t.line !== '——'){ o.push(' 固定台词'); o.push('   ' + L.t.line); o.push(R); }
  o.push(' 系统留言');
  L.t.verdict.forEach(x => wrap(fillNums(x, L.seed), w - 3).forEach(l => o.push('   ' + l)));
  o.push(R, ' 参数面板');
  AX.forEach(k => {
    const v = L.s[k], f = Math.max(0, Math.min(10, Math.round(v / 10)));
    o.push(' ' + AC[k] + '  ' + '█'.repeat(f) + '░'.repeat(10 - f) + '  ' + String(Math.round(v)).padStart(3));
  });
  o.push(R, ' 破局支线');
  L.t.quests.forEach((x, i) => {
    const ls = wrap(fillNums(x, L.seed + i + 1), w - 6);
    o.push(' ' + (i + 1) + '. ' + ls[0]);
    ls.slice(1).forEach(l => o.push('    ' + l));
    o.push('');
  });
  o.push(R);
  o.push(L.isRare ? ' 你不是 NPC。这张卡很少出，记一下日期。'
                  : ' 不是性格标签，是机制诊断。要动的不是你自己，是上面那几条参数。');
  o.push(R);
  wrap(M.disclaimer, w - 2).forEach(l => o.push(' ' + l));
  if (!L.isRare && L.conc >= M.exit_rule.concentration_min && L.s.echo >= M.exit_rule.echo_min){
    o.push('', R);
    M.exit_text.forEach(x => wrap(x.replace(/^\[系统\]\s*/, ''), w - 2).forEach(l => o.push(' ' + l)));
  }
  return o.join('\n');
}
function dw(s){ let n = 0; for (const c of s) n += c.charCodeAt(0) > 0x2E80 ? 2 : 1; return n; }
function pad(s, w){ w = w || 54; const p = Math.max(0, w - dw(s)); return ' '.repeat(Math.floor(p / 2)) + s; }
function wrap(s, w){
  const hard = '，。、）」』】》！？：；…—·!?,.;:)';
  const out = []; let line = '', cw = 0;
  const push = x => { const t = x.replace(/\s+$/, ''); if (t) out.push(t); };
  for (const ch of s){
    const c = ch.charCodeAt(0) > 0x2E80 ? 2 : 1;
    if (cw + c > w && line){
      if (hard.indexOf(ch) >= 0){ out.push(line + ch); line = ''; cw = 0; continue; }
      if (ch === ' '){ push(line); line = ''; cw = 0; continue; }
      if (c === 1 && line.endsWith(' ')){ push(line + ch); line = ''; cw = 0; continue; }
      push(line); line = ch; cw = c;
    } else { line += ch; cw += c; }
  }
  push(line);
  return out;
}
function copyCard(){
  const txt = textCard();
  const done = () => {
    const el = document.getElementById('toast');
    el.textContent = '已复制。去发给一个会回你话的人。';
    el.classList.add('on');
    setTimeout(() => el.classList.remove('on'), 1900);
  };
  if (navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(txt).then(done).catch(() => fallback(txt, done));
  } else fallback(txt, done);
}
function fallback(txt, done){
  const ta = document.createElement('textarea');
  ta.value = txt; ta.style.position = 'fixed'; ta.style.opacity = '0';
  document.body.appendChild(ta); ta.select();
  try { document.execCommand('copy'); done(); } catch(e){ alert(txt); }
  document.body.removeChild(ta);
}
renderIntro();
</script>
</body>
</html>
"""


def _payload():
    q = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))
    t = json.loads((DATA / "types.json").read_text(encoding="utf-8"))
    m = json.loads((DATA / "meta.json").read_text(encoding="utf-8"))
    return {
        "axes": AXES,
        "axis_cn": AXIS_CN,
        "questions": q["questions"],
        "types": {"types": t["types"], "rare": t["rare"]},
        "meta": {
            "zones": m["zones"],
            "opening": m["opening"],
            "disclaimer": m["disclaimer"],
            "exit_rule": m["exit_rule"],
            "exit_text": m["exit_text"],
            "calibration": m["calibration"],
        },
    }


def build(out_path):
    html = TPL.replace("__DATA__", json.dumps(_payload(), ensure_ascii=False))
    Path(out_path).write_text(html, encoding="utf-8")
    return out_path, len(html)


def verify():
    """抽出 JS 引擎，用 node 跑 200 组随机答案，与 Python 逐一对拍。"""
    q = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))
    t = json.loads((DATA / "types.json").read_text(encoding="utf-8"))
    m = json.loads((DATA / "meta.json").read_text(encoding="utf-8"))
    sys.path.insert(0, str(ROOT / "scripts"))
    import npc as N

    js_engine = json.dumps(_payload(), ensure_ascii=False)
    # 引擎段 = AX 常量 → 主题段之前（主题/渲染含 DOM 调用，不进对拍）
    body = TPL[TPL.index("const AX = DATA.axes"):TPL.index("/* ---------- 主题 ---------- */")]

    cases = []
    seed = 20260921
    for i in range(200):
        picks = []
        for x in q["questions"]:
            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
            picks.append(seed % len(x["options"]))
        cases.append(picks)

    js = (
        "const DATA = " + js_engine + ";\n"
        + body
        + "const cases = " + json.dumps(cases) + ";\n"
        + "const out = cases.map(p => {\n"
        + "  const s = normalize(rawScores(p));\n"
        + "  const t = classify(s);\n"
        + "  const ids = p.map((oi,i)=>Q[i].options[oi].id).join('');\n"
        + "  return [t.key, Math.round(concentration(s)), coordOf(ids, t.stance),\n"
        + "          AX.map(k=>Math.round(s[k])).join(','), crc32(ids)];\n"
        + "});\n"
        + "console.log(JSON.stringify(out));\n"
    )
    tmp = Path(tempfile.gettempdir()) / "_npc_verify.js"
    tmp.write_text(js, encoding="utf-8")
    try:
        res = subprocess.run(["node", str(tmp)], capture_output=True, text=True,
                             encoding="utf-8", timeout=60)
    except FileNotFoundError:
        print("[skip] 未找到 node，跳过对拍")
        return 0
    if res.returncode != 0:
        print("[ERROR] node 执行失败：\n" + (res.stderr or "")[:1500])
        return 1
    js_out = json.loads(res.stdout.strip().splitlines()[-1])

    bad = 0
    for i, picks in enumerate(cases):
        ids = [q["questions"][j]["options"][oi]["id"] for j, oi in enumerate(picks)]
        raw = N.raw_scores(q["questions"], ids)
        s = N.normalize(raw, m["calibration"]["anchors"])
        ty = N.classify(s, t, m["calibration"]["stats"])
        conc = N.concentration(s)
        coord = N.coord_of("".join(ids), m, ty["stance"])
        axes = ",".join(str(round(s[k])) for k in AXES)
        import zlib
        crc = zlib.crc32("".join(ids).encode("utf-8")) & 0xFFFFFFFF
        want = [ty["key"], conc, coord, axes, crc]
        got = js_out[i]
        if want != got:
            bad += 1
            if bad <= 3:
                print(f"[差异] #{i} picks={picks}\n  py={want}\n  js={got}")
    if bad:
        print(f"[ERROR] 对拍失败 {bad}/200 组")
        return 1
    print("[ok] JS 与 Python 引擎对拍通过（200/200：类型 / 浓度 / 坐标 / 七轴 / CRC32）")
    return 0


def smoke(html_path):
    """真机冒烟：用真实 Chromium 内核加载产物，抓 mock 环境测不出的错
    （如 `function top(){}` 撞 window.top 导致整页全黑）。"""
    node = shutil.which("node")
    if not node:
        for c in (r"C:\Users\yangduo\.workbuddy\binaries\node\versions\22.22.2-3\node.exe",):
            if Path(c).exists():
                node = c
                break
    if not node:
        print("[SKIP] 未找到 node，真机冒烟未执行")
        return 0
    js = ROOT / "scripts" / "smoke.js"
    if not js.exists():
        print("[SKIP] 缺少 scripts/smoke.js")
        return 0
    r = subprocess.run([node, str(js), str(html_path)],
                       capture_output=True, text=True, encoding="utf-8")
    print((r.stdout or "").strip())
    if r.returncode != 0:
        err = (r.stderr or "").strip()
        if err:
            print(err)
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "npc-demo.html"))
    ap.add_argument("--verify", action="store_true", help="JS 与 Python 引擎对拍")
    ap.add_argument("--smoke", action="store_true", help="只跑真机冒烟测试")
    ap.add_argument("--no-smoke", action="store_true", help="生成后跳过真机冒烟")
    args = ap.parse_args()
    if args.verify:
        return verify()
    p, n = build(args.out)
    print(f"已生成 {p}（{n / 1024:.1f} KB，单文件、零依赖）")
    if args.smoke or not args.no_smoke:
        # 默认跑：全黑这类 bug 只有真机才抓得到
        return smoke(p)
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
