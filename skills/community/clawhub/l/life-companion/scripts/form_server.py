#!/usr/bin/env python3
"""
form_server.py — serve a styled local HTML form, then write the result to the
user's private home (~/.companion) via companion.py.

A pure HTML file can't touch the filesystem, so this runs a tiny localhost server:
it renders the form, opens the browser, and on submit writes the profile/consent
(atomic + consent-gated, reusing companion.py) and drops a `.form_result.json`
marker so the calling model knows it's done. Nothing leaves the machine.

Usage:
  python3 form_server.py --form onboarding [--home ~/.companion] [--port 8760]
  python3 form_server.py --form career     ...
Run it in the background; tell the user to fill the page; then read the profile
(or ~/.companion/.form_result.json) once they submit.

Design: "灯下私人档案" — paper/lamplight (follows OS light/dark), 朱砂 cinnabar as
the single accent, 青玉 jade for confirmations, 五行 five-colour dots as section
marks, 宋体 display + sans body. Consent for birth data is a tactile lock; saving
stamps a 印章.
"""
import argparse
import datetime
import html
import json
import os
import re
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

_HERE = os.path.dirname(os.path.abspath(__file__))
COMPANION = os.path.join(_HERE, "companion.py")
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from companion import resolve_timezone as _resolve_tz, lunar_to_solar as _lunar_to_solar  # noqa: E402
from companion import _consent_granted, _load_yaml, _paths  # noqa: E402


# ---------------------------------------------------------------------------
CSS = """
:root{
  --paper:#F3EDE1; --paper-2:#EDE5D6; --ink:#2A251E; --ink-soft:#7A7063;
  --line:#E0D7C6; --cinnabar:#B23A2E; --cinnabar-soft:#c9695f; --jade:#3E7C67;
  --field:#FBF8F1; --shadow:0 1px 2px rgba(42,37,30,.05),0 10px 30px rgba(42,37,30,.06);
  --wood:#6E8B67; --fire:#B23A2E; --earth:#C9A15A; --metal:#9AA0A6; --water:#4B6B86;
}
@media (prefers-color-scheme:dark){
  :root{
    --paper:#181410; --paper-2:#1F1A14; --ink:#EFE7D8; --ink-soft:#A99E8C;
    --line:#2E2820; --cinnabar:#D9634F; --cinnabar-soft:#e08573; --jade:#6FB59A;
    --field:#221C16; --shadow:0 1px 2px rgba(0,0,0,.3),0 18px 40px rgba(0,0,0,.35);
    --earth:#C9A15A; --metal:#B7BDC4; --water:#7FA6C4; --wood:#8FB187;
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; color:var(--ink); background:var(--paper);
  font:16px/1.6 -apple-system,"PingFang SC","Microsoft YaHei",system-ui,"Segoe UI",sans-serif;
  background-image:radial-gradient(120% 80% at 50% -10%, var(--paper-2), var(--paper) 60%);
  min-height:100vh; padding:48px 20px 80px;
}
.wrap{max-width:600px;margin:0 auto}
.serif{font-family:"Songti SC","Noto Serif SC",Georgia,"Times New Roman",serif}
.eyebrow{font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink-soft);
  display:flex;align-items:center;gap:9px;margin:0 0 14px}
.dot{width:9px;height:9px;border-radius:50%;display:inline-block;flex:none;
  box-shadow:0 0 0 3px color-mix(in srgb, currentColor 16%, transparent)}
header{margin-bottom:8px}
h1{font-size:30px;line-height:1.25;margin:.1em 0 .15em;font-weight:600;letter-spacing:.01em}
.lede{color:var(--ink-soft);margin:0 0 6px;font-size:15px}
.seal-line{display:inline-flex;align-items:center;gap:8px;color:var(--jade);font-size:13px;margin-top:10px}
.seal-line svg{width:15px;height:15px}
section.card{background:var(--field);border:1px solid var(--line);border-radius:16px;
  padding:22px 22px 8px;margin:22px 0;box-shadow:var(--shadow)}
.q{margin-bottom:20px}
.q > label.lab, .q .lab{display:block;font-weight:600;margin-bottom:4px}
.hint{color:var(--ink-soft);font-size:13px;margin:0 0 10px}
input[type=text],input[type=date],input[type=time],select{
  width:100%;padding:11px 13px;border:1px solid var(--line);border-radius:10px;
  background:var(--paper);color:var(--ink);font:inherit}
input:focus,select:focus,.opt:focus-within{outline:none;border-color:var(--cinnabar);
  box-shadow:0 0 0 3px color-mix(in srgb,var(--cinnabar) 22%,transparent)}
.opts{display:grid;gap:9px}
.opts.row{grid-template-columns:repeat(auto-fit,minmax(120px,1fr))}
.opt{position:relative;display:flex;flex-direction:column;gap:2px;cursor:pointer;
  border:1px solid var(--line);border-radius:12px;padding:12px 14px;background:var(--paper);
  transition:border-color .15s,background .15s,transform .05s}
.opt:hover{border-color:var(--cinnabar-soft)}
.opt input{position:absolute;opacity:0;inset:0}
.opt .t{font-weight:600}
.opt .d{font-size:12.5px;color:var(--ink-soft)}
.opt:has(input:checked){border-color:var(--cinnabar);
  background:color-mix(in srgb,var(--cinnabar) 8%,var(--paper))}
.opt:has(input:checked)::after{content:"";position:absolute;top:12px;right:12px;width:8px;height:8px;
  border-radius:50%;background:var(--cinnabar)}
.lock{display:flex;align-items:flex-start;gap:12px;padding:14px;border:1px dashed var(--line);
  border-radius:12px;background:var(--paper);cursor:pointer}
.lock input{margin-top:3px;accent-color:var(--cinnabar);width:18px;height:18px}
.lock .t{font-weight:600}
.lock .d{font-size:12.5px;color:var(--ink-soft)}
.vault{max-height:0;overflow:hidden;opacity:.4;transition:max-height .4s ease,opacity .3s}
.vault.open{max-height:640px;opacity:1;margin-top:14px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
@media(max-width:440px){.grid2{grid-template-columns:1fr}}
.checkline{display:flex;gap:11px;align-items:flex-start;padding:11px 0}
.checkline input{margin-top:3px;accent-color:var(--jade);width:18px;height:18px}
.checkline .d{font-size:12.5px;color:var(--ink-soft)}
button.save{width:100%;margin-top:6px;padding:15px;border:none;border-radius:13px;
  background:var(--cinnabar);color:#fff;font:600 16px/1 inherit;letter-spacing:.06em;cursor:pointer;
  box-shadow:0 6px 18px color-mix(in srgb,var(--cinnabar) 35%,transparent);transition:transform .06s,filter .15s}
button.save:hover{filter:brightness(1.05)}
button.save:active{transform:translateY(1px)}
.footer{color:var(--ink-soft);font-size:12.5px;text-align:center;margin-top:22px;line-height:1.7}
.footer b{color:var(--ink);font-weight:600}
.likert{display:grid;grid-template-columns:1fr auto;gap:10px 14px;align-items:center}
.likert .stmt{font-size:15px}
.scale{display:flex;gap:6px}
.scale label{cursor:pointer}
.scale input{position:absolute;opacity:0}
.scale .pip{width:26px;height:26px;border-radius:50%;border:1px solid var(--line);display:grid;
  place-items:center;font-size:11px;color:var(--ink-soft);background:var(--paper);transition:all .12s}
.scale label:has(input:checked) .pip{border-color:var(--cinnabar);background:var(--cinnabar);color:#fff}
.scale label:has(input:focus-visible) .pip{box-shadow:0 0 0 3px color-mix(in srgb,var(--cinnabar) 22%,transparent)}
.item{padding:14px 0;border-top:1px solid var(--line)}
.item:first-child{border-top:none}
.typemark{font:600 11px/1 inherit;letter-spacing:.12em;color:var(--ink-soft)}
/* seal stamp (success) */
.stamp-wrap{display:grid;place-items:center;padding:20px 0}
.stamp{width:118px;height:118px;border:3px solid var(--cinnabar);border-radius:14px;
  display:grid;place-items:center;color:var(--cinnabar);transform:rotate(-7deg);
  box-shadow:inset 0 0 0 3px color-mix(in srgb,var(--cinnabar) 25%,transparent)}
.stamp .zi{font-size:34px;font-weight:700;letter-spacing:.12em;line-height:1}
@keyframes press{0%{opacity:0;transform:rotate(-7deg) scale(1.6)}60%{opacity:1}100%{transform:rotate(-7deg) scale(1)}}
.stamp{animation:press .5s cubic-bezier(.2,.8,.3,1) both}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}
  .vault{transition:none}}
"""

FIVE = {"wood": "var(--wood)", "fire": "var(--fire)", "earth": "var(--earth)",
        "metal": "var(--metal)", "water": "var(--water)"}


def page(title, body):
    return (f"<!doctype html><html lang='zh'><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(title)}</title><style>{CSS}</style></head>"
            f"<body><div class='wrap'>{body}</div></body></html>")


def eyebrow(text, phase):
    return f"<p class='eyebrow'><span class='dot' style='color:{FIVE[phase]}'></span>{html.escape(text)}</p>"


def opt(name, value, title, desc, checked=False):
    c = " checked" if checked else ""
    d = f"<span class='d'>{html.escape(desc)}</span>" if desc else ""
    return (f"<label class='opt'><input type='radio' name='{name}' value='{html.escape(value)}'{c}>"
            f"<span class='t'>{html.escape(title)}</span>{d}</label>")


# ---------------------------------------------------------------------------
def render_onboarding(profile, consent=None):
    ident = profile.get("identity", {}) or {}
    prefs = profile.get("preferences", {}) or {}
    # What was already allowed and entered opens pre-filled, so a re-submit to change one
    # thing doesn't read as withdrawing the rest. read-profile withholds birth data whose
    # consent isn't granted, and nothing withheld is shown.
    consent = consent or {}
    birth_allowed, mood_allowed = consent.get("birth") is True, consent.get("mood") is True
    birth = profile.get("birth") if isinstance(profile.get("birth"), dict) else {}
    if not birth_allowed or birth.get("_withheld"):
        birth = {}

    def filled(v):
        return "" if v in (None, "") else f" value='{html.escape(str(v))}'"
    b_acc = birth.get("time_accuracy") or "exact"
    b_gender = birth.get("gender")
    b_win = birth.get("time_window_min") or 60
    windows = [(30, "±30 分钟"), (60, "±1 小时"), (120, "±2 小时")]
    if b_win not in dict(windows):
        windows.append((b_win, f"±{b_win} 分钟"))
    window_opts = "".join(f"<option value='{w}'{' selected' if w == b_win else ''}>{t}</option>"
                          for w, t in windows)
    name = html.escape(ident.get("name") or "")
    locale = ident.get("locale")
    tone = prefs.get("tone")
    tz = ident.get("timezone")
    region = {"Asia/Shanghai": "cn", "Europe/Amsterdam": "nl"}.get(tz, "")

    langs = [("zh", "中文", "命理术语保留中文，配大白话"),
             ("en", "English", "BaZi terms kept, with a gloss"),
             ("bilingual", "中英双语", "关键结论中英对照")]
    tones = [("warm-direct", "温暖直接", "贴心又不绕弯子"),
             ("light-playful", "轻松俏皮", "多一点轻松、幽默"),
             ("concise", "简洁克制", "少寒暄，直奔重点")]
    regions = [("cn", "中国大陆", "Asia/Shanghai"),
               ("nl", "荷兰 NL", "Europe/Amsterdam"),
               ("other", "其他 / 稍后", "之后再补")]

    body = f"""
    <header>
      {eyebrow('私人档案 · 只存在你本机', 'earth')}
      <h1 class='serif'>先让我认识你</h1>
      <p class='lede'>花一分钟。这些只用来让往后的每一次陪伴更贴你，全部留在这台机器上。</p>
      <span class='seal-line'>{_lock_svg()} 本地保存 · 随时可删</span>
    </header>
    <form method='post' action='/submit'>

      <section class='card'>
        {eyebrow('称呼与语气', 'wood')}
        <div class='q'><label class='lab' for='name'>我该怎么称呼你？</label>
          <p class='hint'>随便填，或留空也行。</p>
          <input id='name' name='name' type='text' value='{name}' placeholder='比如：小澄 / Leo'></div>
        <div class='q'><span class='lab'>用什么语言跟你聊？</span>
          <div class='opts row'>{''.join(opt('locale',v,t,d,locale==v) for v,t,d in langs)}</div></div>
        <div class='q'><span class='lab'>你喜欢的语气？</span>
          <div class='opts row'>{''.join(opt('tone',v,t,d,tone==v) for v,t,d in tones)}</div></div>
      </section>

      <section class='card'>
        {eyebrow('所在地区', 'water')}
        <div class='q'><span class='lab'>你现在大致在哪里？</span>
          <p class='hint'>用于每日时辰计算，也用于万一需要时给你<b>本地</b>的求助渠道。</p>
          <div class='opts row'>{''.join(opt('region',v,t,d,region==v) for v,t,d in regions)}</div>
          <div style='margin-top:10px'><input name='city' type='text' placeholder='城市（选“其他”时填，如 柏林）'></div></div>
      </section>

      <section class='card'>
        {eyebrow('生辰 · 命理与运势要用', 'fire')}
        <label class='lock'>
          <input type='checkbox' name='birth_consent' id='bc'{' checked' if birth_allowed else ''} onchange="document.getElementById('vault').classList.toggle('open',this.checked)">
          <span><span class='t'>我同意把生辰存在本机</span>
          <span class='d'>用来起八字命盘、算每日运势。不填也能用日记和职业模块。随时可删。</span></span>
        </label>
        <div class='vault{' open' if birth_allowed else ''}' id='vault'>
          <div class='grid2'>
            <div class='q'><span class='lab'>出生日期</span>
              <div class='opts row'>{opt('birth_calendar','solar','公历','',True)}{opt('birth_calendar','lunar','农历','')}</div>
              <input id='bd' name='birth_date' type='date' aria-label='公历出生日期'{filled(birth.get('date'))}>
              <p class='hint'>只记得农历就选「农历」，填这三格，我来换算：</p>
              <div style='display:flex;gap:8px;flex-wrap:wrap'>
                <input name='birth_lunar_year' type='number' min='1901' max='2099' placeholder='农历年，如 1993' style='max-width:10em'>
                <input name='birth_lunar_month' type='number' min='1' max='12' placeholder='月 1–12' style='max-width:6em'>
                <input name='birth_lunar_day' type='number' min='1' max='30' placeholder='日 1–30' style='max-width:6em'>
              </div>
              <label class='checkline'><input type='checkbox' name='birth_lunar_leap'>
                <span>是闰月<span class='d'>比如「闰四月」。拿不准就别勾，我会核对那一年有没有闰月。</span></span></label></div>
            <div class='q'><label class='lab' for='bt'>出生时间</label>
              <input id='bt' name='birth_time' type='time'{filled(birth.get('time'))}>
              <div class='opts row'>{opt('birth_time_accuracy','exact','准确','出生证明上写的，或记得很清楚',b_acc=='exact')}{opt('birth_time_accuracy','approx','大概','比如「九点左右」',b_acc=='approx')}{opt('birth_time_accuracy','unknown','不知道','八字照样能起，只是少了时柱',b_acc=='unknown')}</div>
              <label class='lab' for='btw' style='margin-top:8px'>选了「大概」的话，前后可能差多少？</label>
              <select id='btw' name='birth_time_window'>{window_opts}</select></div>
          </div>
          <div class='grid2'>
            <div class='q'><label class='lab' for='bp'>出生地</label>
              <input id='bp' name='birth_place' type='text' placeholder='如 北京 / Beijing'{filled(birth.get('place'))}></div>
            <div class='q'><span class='lab'>性别<span class='d' style='font-weight:400'>（定大运方向）</span></span>
              <div class='opts row'>{opt('gender','male','男','',b_gender=='male')}{opt('gender','female','女','',b_gender=='female')}</div></div>
          </div>
        </div>
      </section>

      <section class='card'>
        {eyebrow('一个可选的许可', 'metal')}
        <label class='checkline'><input type='checkbox' name='mood_consent'{' checked' if mood_allowed else ''}>
          <span><span style='font-weight:600'>允许记录心情分（0–10）</span>
          <span class='d'>只用来看日记里的情绪趋势。不勾就只存文字。</span></span></label>
      </section>

      <button class='save' type='submit'>保存到本机</button>
      <p class='footer'><b>算出来的是事实，读出来的是镜子。</b><br>
        你的一切只在这台机器上，从不上传；想删随时对我说一声。</p>
    </form>
    """
    return page("Life Companion · 建档", body)


def _lock_svg():
    return ("<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' "
            "stroke-linecap='round'><rect x='4' y='11' width='16' height='9' rx='2'/>"
            "<path d='M8 11V8a4 4 0 0 1 8 0v3'/></svg>")


def success_page(msg):
    body = f"""
    <header>{eyebrow('已存档', 'earth')}<h1 class='serif'>都记好了</h1></header>
    <div class='stamp-wrap'><div class='stamp'><span class='zi serif'>已<br>存档</span></div></div>
    <p class='lede' style='text-align:center'>{html.escape(msg)}</p>
    <p class='footer'>你可以关掉这个页面，回到对话继续。<br>想改或想删，随时对我说一声。</p>
    """
    return page("已存档", body)


# ---------------------------------------------------------------------------
def _run_companion(home, *args):
    """Run companion.py, and when it refuses, raise with what it said: a bare
    CalledProcessError told the person only "returned non-zero exit status 1"."""
    r = subprocess.run([sys.executable, COMPANION, "--home", home, *args],
                       capture_output=True, text=True)
    if r.returncode:
        said = (r.stdout.strip() or r.stderr.strip())[-400:]
        raise RuntimeError(f"companion.py {args[0]} exited {r.returncode}: {said}")


def _current_state(home):
    """(profile, consent) the onboarding form opens with. The profile comes through
    read-profile, which withholds birth data whose consent isn't granted; consent is
    {category: granted}."""
    prof = json.loads(subprocess.run(
        [sys.executable, COMPANION, "--home", home, "read-profile", "--json"],
        capture_output=True, text=True).stdout or "{}")
    stored = _load_yaml(_paths(home)["consent"])
    return prof, {c: _consent_granted(stored, c) for c in ("birth", "relationships", "mood")}


def write_onboarding(home, form):
    def g(k, d=""):
        v = form.get(k, [d])
        return v[0] if isinstance(v, list) else v

    # identity.timezone drives daily timing AND which crisis helpline this person is
    # offered. The two quick-pick regions cover the common cases; for anyone else we
    # resolve the city they actually typed instead of throwing it away (which is what
    # this used to do — a Berlin user got timezone:null and a dead `location` field).
    region = g("region")
    city = g("city").strip()
    tz = {"cn": "Asia/Shanghai", "nl": "Europe/Amsterdam"}.get(region)
    tz_note = None
    if tz is None and city:
        cands = _resolve_tz(city)
        # Only one clear answer is stored: alone at the top, and 0.95 or above. A lone partial
        # match used to be stored as if certain ("Victoria, BC" became Australia/Victoria), and
        # so did the first of a tie (中國香港 became Asia/Shanghai).
        top = cands[0]["score"] if cands else 0
        if top >= 0.95 and sum(c["score"] == top for c in cands) == 1:
            tz = cands[0]["timezone"]
        elif cands:
            tz_note = ("「%s」对不上唯一一个时区（候选：%s）—— 跟本人确认一个再存。"
                       % (city, "、".join(c["timezone"] for c in cands[:3])))
        else:
            tz_note = ("没能从「%s」认出时区。问一个附近的大城市或国家再存 "
                       "identity.timezone —— 别猜：它决定每日时辰，也决定万一需要时给"
                       "哪个国家的求助热线。" % city)
    elif tz is None and region == "other":
        tz_note = "所在地留空了。timezone 还是 null，日运时辰和本地求助渠道都会受影响。"

    identity = {"locale": g("locale") or None, "timezone": tz}
    if g("name").strip():
        identity["name"] = g("name").strip()
    if city:
        identity["location"] = city          # the raw words they used; see profile-schema.md

    patch = {"identity": identity,
             "preferences": {"tone": g("tone") or "warm-direct"},
             "onboarding_complete": True}

    birth_ok = bool(g("birth_consent"))
    mood_ok = bool(g("mood_consent"))
    consent_before = _load_yaml(_paths(home)["consent"])
    stored = _load_yaml(_paths(home)["profile"])
    stored_birth = (stored.get("birth") if isinstance(stored, dict)
                    and isinstance(stored.get("birth"), dict) else {})
    merged_birth = dict(stored_birth)
    lunar_note = None
    if birth_ok:
        # 准确 / 大概 / 不知道. "大概九点" used to be stored as an exact 09:00, so every pillar
        # computed from it looked certain. The old checkbox still counts as 不知道.
        accuracy = g("birth_time_accuracy") or ("unknown" if g("birth_time_unknown") else "exact")
        # An empty field means "not given this time", never "erase": a re-submit used to blank
        # the stored date, time and place. 不知道 still clears the time on purpose, and a first
        # submit without a time still records it as unknown.
        keep_time = not g("birth_time") and accuracy != "unknown" and bool(stored_birth.get("time"))
        time_unknown = accuracy == "unknown" or not g("birth_time")
        birth_date, date_input = g("birth_date") or None, None
        if g("birth_calendar") == "lunar":
            # Converted here, never by hand: leap months and 29-day months are where a
            # hand conversion goes wrong, and an impossible date must not be stored.
            try:
                y, m, d = (int(g(f"birth_lunar_{k}")) for k in ("year", "month", "day"))
            except ValueError:
                birth_date = None
                lunar_note = ("选了农历，但年/月/日没填全。没有存出生日期，问清楚后用 "
                              "companion.py lunar-to-solar 换算再存。")
            else:
                leap = bool(g("birth_lunar_leap"))
                solar, why = _lunar_to_solar(y, m, d, leap)
                label = f"农历 {y} 年{'闰' if leap else ''}{m}月{d}日"
                date_input = {"calendar": "lunar", "lunar": f"{y:04d}-{m:02d}-{d:02d}",
                              "leap": leap}
                birth_date = solar
                lunar_note = (f"{label}换算不了：{why}。没有存出生日期，跟本人核对后再存。" if why
                              else f"{label}已按中国历法换算成公历 {solar}。出生在海外、时间又"
                                   "贴近午夜的，日期可能差一天，跟本人确认一下。")
        window = None
        if accuracy == "approx" and not time_unknown:
            try:
                window = max(1, min(240, int(g("birth_time_window") or 60)))
            except ValueError:
                window = 60
        given = {"date": birth_date, "gender": g("gender") or None,
                 "place": g("birth_place").strip() or None}
        patch["birth"] = {k: v for k, v in given.items() if v is not None or not stored_birth.get(k)}
        if not keep_time:
            patch["birth"].update({
                "time": None if time_unknown else g("birth_time"),
                "time_known": not time_unknown,
                "time_accuracy": "unknown" if time_unknown else accuracy,
                "time_window_min": window,
            })
        if date_input and birth_date is not None:
            patch["birth"]["date_input"] = date_input
        merged_birth.update(patch["birth"])
    # Record consent BEFORE writing anything it gates. The form collects the birth
    # checkbox and the birth fields in one submission, and this used to write the
    # profile first — which is backwards semantically (consent precedes collection) and
    # now fails outright, since companion.py enforces the gate instead of trusting the
    # caller. Order matters; keep consent first.
    # It grants what is ticked and never revokes. Every submit used to write birth=no and
    # mood=no for an unticked box, so re-submitting to change the tone withdrew consent while
    # the data stayed on disk, withheld, and nobody was told. Withdrawing goes through
    # `consent --set X=no`, which says what is still stored.
    grants = [f"{c}=yes" for c, ticked in (("birth", birth_ok), ("mood", mood_ok)) if ticked]
    if grants:
        _run_companion(home, "consent", "--set", *grants)
    _run_companion(home, "set-profile", "--merge-json", json.dumps(patch, ensure_ascii=False))

    # Anything the form could NOT fill goes in `todo`, so the model finishes the job
    # instead of discovering the hole later (or never). A form that silently returns a
    # half-filled profile is worse than one that says what's missing.
    todo = []
    if tz_note:
        todo.append(tz_note)
    if lunar_note:
        todo.append(lunar_note)
    kept = [label for c, label, ticked in (("birth", "生辰", birth_ok), ("mood", "心情分", mood_ok))
            if not ticked and _consent_granted(consent_before, c)]
    if kept:
        todo.append(f"这次表单没勾「{'」「'.join(kept)}」，但之前已经同意过：表单不会撤回同意，存着的"
                    "数据也没动。如果本人是想撤回，确认后用 companion.py consent --set birth=no（或 "
                    "mood=no），它会说明还存着什么、怎么删。")
    if birth_ok and merged_birth.get("time_window_min"):
        w = merged_birth["time_window_min"]
        todo.append(f"出生时间是大概的（±{w} 分钟）：起八字时加 --time-window {w}，把这段时间里"
                    "可能的柱都列出来，变动的柱按不确定来读。")
    if birth_ok and merged_birth.get("place") and not merged_birth.get("lat"):
        todo.append("生辰地点有了，但 birth.lat/lon/tz_at_birth 还是空的 —— 由城市推出来并"
                    "用 set-profile 存上（onboarding.md Tier 1），否则星盘永远算不出上升和宫位。")
    if birth_ok and not merged_birth.get("gender"):
        todo.append("没填性别 —— 八字大运的顺逆行需要它，问一下再起盘。")

    summary = {"status": "onboarded", "form": "onboarding",
               "name": identity.get("name"), "locale": identity.get("locale"),
               "tone": patch["preferences"]["tone"], "timezone": tz,
               "location": identity.get("location"),
               "birth_consent": birth_ok,
               "birth_date": (str(merged_birth["date"]) if birth_ok and merged_birth.get("date")
                              else None),
               "mood_consent": mood_ok,
               "todo": todo,
               "ts": datetime.datetime.now().isoformat(timespec="seconds")}
    # The marker only has to say that a submit happened. It used to carry the birth date,
    # which then outlived `forget --birth` in a file nobody thought of as birth data.
    marker = {k: v for k, v in summary.items() if k != "birth_date"}
    with open(os.path.join(home, ".form_result.json"), "w", encoding="utf-8") as f:
        json.dump(marker, f, ensure_ascii=False)
    return summary, "档案已建好——语言、语气、所在地都记下了。" + (
        "生辰也存好了，随时可以起命盘。" if birth_ok else
        "生辰之前存过，这次没动。" if _consent_granted(consent_before, "birth") else
        "想看命盘的话，之后补上生辰就行。")


ITEMS_PATH = os.path.join(_HERE, "..", "data", "career", "assessment_items.json")
ZH_VALUES = {"Achievement": ("成就感", "发挥能力、看到实在的成果"),
             "Independence": ("自主", "自己定方法、自己定问题"),
             "Recognition": ("被认可", "晋升、地位、被尊重与看见"),
             "Relationships": ("人际关系", "友善的同事、帮助他人"),
             "Support": ("支持/保障", "有靠山、制度公平一致"),
             "Working Conditions": ("工作条件", "稳定、薪酬、舒适、环境")}
LIKERT = [(0, "很不喜欢"), (1, "不喜欢"), (2, "一般"), (3, "喜欢"), (4, "很喜欢")]
TYPE_ZH = {"R": "动手", "I": "钻研", "A": "创造", "S": "助人", "E": "影响", "C": "条理"}


def render_career(profile):
    data = json.load(open(ITEMS_PATH, encoding="utf-8"))
    items = data["interest_items"]
    ctx = (profile.get("context", {}) or {}).get("career", "")

    rows = []
    for it in items:
        pips = "".join(
            f"<label title='{html.escape(zh)}'><input type='radio' name='q{it['id']}' "
            f"value='{v}'><span class='pip'>{v}</span></label>" for v, zh in LIKERT)
        rows.append(
            f"<div class='item'><div class='likert'><span class='stmt'>{html.escape(it['zh'])}"
            f"<br><span class='typemark'>{TYPE_ZH.get(it['type'],'')}</span></span>"
            f"<span class='scale'>{pips}</span></div></div>")

    vrows = []
    for v in data["optional_work_values"]["values"]:
        key = v["value"]; zh, desc = ZH_VALUES.get(key, (key, v.get("en", "")[:24]))
        opts = "".join(f"<option value='{n}'>{n}</option>" for n in range(1, 7))
        vrows.append(
            f"<div class='q' style='display:flex;gap:12px;align-items:center'>"
            f"<select name='val_{html.escape(key)}' style='width:64px' required>"
            f"<option value='' selected disabled>·</option>{opts}</select>"
            f"<span><b>{zh}</b> <span class='d' style='color:var(--ink-soft);font-size:12.5px'>{html.escape(desc)}</span></span></div>")

    body = f"""
    <header>
      {eyebrow('职业契合 · 兴趣小测', 'metal')}
      <h1 class='serif'>你会喜欢做哪类事</h1>
      <p class='lede'>这是一个基于 Holland/RIASEC 的<b>兴趣小测</b>，不是正式量表。按你会<b>“喜欢”</b>来选，
        不是“擅长”或“应该”。答完我用真实职业库算契合度——只给低/中/高，不给假百分比。</p>
    </header>
    <form method='post' action='/submit'>
      <section class='card'>
        {eyebrow('兴趣 · 21 题', 'wood')}
        <p class='hint'>每题选一个：0 很不喜欢 → 4 很喜欢。</p>
        {''.join(rows)}
      </section>
      <section class='card'>
        {eyebrow('工作价值观 · 排个序', 'water')}
        <p class='hint'>给这六项<b>排名次</b>（1=最重要 … 6=最不重要），每个名次只用一次——强制取舍，权衡才真实。</p>
        {''.join(vrows)}
      </section>
      <section class='card'>
        {eyebrow('你现在与想去的方向（可选）', 'earth')}
        <div class='q'><label class='lab' for='cj'>现在的工作/方向</label>
          <input id='cj' name='current_job' type='text' value='{html.escape(ctx)}' placeholder='如 医学影像重建研究'></div>
        <div class='q'><label class='lab' for='aj'>想去的方向/岗位（如果有）</label>
          <input id='aj' name='aspiration_job' type='text' placeholder='如 工业界算法研究员'></div>
      </section>
      <button class='save' type='submit'>保存测评并算契合度</button>
      <p class='footer'><b>兴趣是起点，不是判决。</b><br>这些只存在你本机；结果只给方向和档位，不预测你能不能拿到某份工作。</p>
    </form>
    """
    return page("Life Companion · 职业测评", body)


def write_career(home, form):
    def g(k, d=""):
        v = form.get(k, [d]); return v[0] if isinstance(v, list) else v
    data = json.load(open(ITEMS_PATH, encoding="utf-8"))
    # Only answers the scale has are stored, and the page says what it left out: q1=9 used to be
    # saved while the page said the check was received, and a letter crashed the submit.
    answers, dropped = {}, []
    for it in data["interest_items"]:
        val = str(g(f"q{it['id']}")).strip()
        if val == "":
            continue
        if re.fullmatch(r"[0-4]", val):
            answers[str(it["id"])] = int(val)
        else:
            dropped.append(f"q{it['id']}")
    # A ranking is six places used once each. Repeated or missing places used to be stored and
    # scored as if they were a ranking.
    ranks = {v["value"]: str(g(f"val_{v['value']}")).strip()
             for v in data["optional_work_values"]["values"]}
    values_rank, values_note = {}, None
    if any(ranks.values()):
        if sorted(ranks.values()) == [str(n) for n in range(1, len(ranks) + 1)]:
            values_rank = {name: int(r) for name, r in ranks.items()}
        else:
            values_note = ("价值观排序要把六项各排一个名次（1 到 6 各用一次）；这次有重复或空着的，"
                           "没有存，打分时只看兴趣。")
    intake = {"answers": answers, "values_rank": values_rank,
              "current_job": g("current_job").strip(), "aspiration_job": g("aspiration_job").strip(),
              "answered": len(answers), "dropped": dropped, "values_note": values_note,
              "ts": datetime.datetime.now().isoformat(timespec="seconds")}
    _run_companion(home, "cache", "--module", "career_intake",
                   "--merge-json", json.dumps({"latest": intake}, ensure_ascii=False))
    with open(os.path.join(home, ".form_result.json"), "w", encoding="utf-8") as f:
        json.dump({"status": "career_intake", "form": "career", **intake}, f, ensure_ascii=False)
    notes = ""
    if dropped:
        notes += f"有 {len(dropped)} 题的回答不在 0–4 之间，没存（{'、'.join(dropped)}）。"
    if values_note:
        notes += values_note
    return intake, (f"测评收好了（{len(answers)}/21 题" + (" + 价值观排序" if values_rank else "")
                    + "）。" + notes + "回到对话，我就用真实职业库给你算契合度。")


# ---------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    home = None
    form_type = "onboarding"
    done = threading.Event()

    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        b = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def log_message(self, *a):
        pass

    def do_GET(self):
        if urlparse(self.path).path not in ("/", ""):
            self._send(404, page("404", "<p>Not found</p>")); return
        prof, consent = _current_state(self.home)
        html_out = (render_career(prof) if self.form_type == "career"
                    else render_onboarding(prof, consent))
        self._send(200, html_out)

    def do_POST(self):
        if urlparse(self.path).path != "/submit":
            self._send(404, page("404", "<p>Not found</p>")); return
        length = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(length).decode("utf-8"))
        try:
            if self.form_type == "career":
                summary, msg = write_career(self.home, form)
            else:
                summary, msg = write_onboarding(self.home, form)
            print("SUBMITTED " + json.dumps(summary, ensure_ascii=False), flush=True)
            self._send(200, success_page(msg))
            Handler.done.set()
        except Exception as e:  # pragma: no cover
            self._send(500, page("出错了", f"<p>保存时出错：{html.escape(str(e))}。"
                                 f"可以回到对话，用聊天方式建档。</p>"))


def _bind(port, tries=10):
    """Bind 127.0.0.1:port, walking forward if it's taken.

    A stale server from an earlier run is the NORMAL failure here (this used to be
    started with `&` and never stopped), and it used to surface as a raw
    `OSError: Address already in use` traceback. Walk to the next free port instead,
    and if none is free say what to do about it.
    """
    last = None
    for p in range(port, port + tries):
        try:
            return ThreadingHTTPServer(("127.0.0.1", p), Handler), p
        except OSError as e:
            last = e
    print(f"[life-companion] could not bind any port in {port}..{port + tries - 1}: {last}\n"
          f"  probably a form server left running from an earlier turn.\n"
          f"  fix: pkill -f form_server.py   (or pass a different --port)\n"
          f"  or skip the form entirely and collect the same fields in chat "
          f"(references/onboarding.md).", file=sys.stderr)
    sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--form", default="onboarding", choices=["onboarding", "career"])
    ap.add_argument("--home", default=None)
    ap.add_argument("--port", type=int, default=8760)
    ap.add_argument("--no-open", action="store_true")
    ap.add_argument("--timeout", type=int, default=900,
                    help="exit if nothing is submitted within N seconds (default 900). "
                         "0 = wait forever (you must kill it yourself).")
    ap.add_argument("--keep-alive", action="store_true",
                    help="stay up after a submit instead of shutting down")
    args = ap.parse_args()

    home = os.path.abspath(args.home or os.environ.get("COMPANION_HOME")
                           or os.path.expanduser("~/.companion"))
    os.makedirs(home, exist_ok=True)
    Handler.home = home
    Handler.form_type = args.form

    srv, port = _bind(args.port)
    url = f"http://127.0.0.1:{port}/"
    print(f"SERVING {url} (form={args.form}, home={home}, "
          f"auto-exit={'on submit' if not args.keep_alive else 'never'}"
          f"{f', timeout={args.timeout}s' if args.timeout else ''})", flush=True)
    if not args.no_open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()

    # Serve in a background thread so the main thread can own the lifecycle: this
    # process must NOT outlive the task. It writes private data, and no harness other
    # than Claude Code reliably lets an agent kill a background job on a later turn —
    # so it stops itself, on submit or on timeout.
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        if args.keep_alive:
            Handler.done.wait()
            submitted = True
        else:
            submitted = Handler.done.wait(timeout=args.timeout or None)
    except KeyboardInterrupt:
        submitted = Handler.done.is_set()
    if submitted and not args.keep_alive:
        time.sleep(1.5)  # let the browser finish fetching the success page
    srv.shutdown()
    if submitted:
        print("DONE form submitted; server stopped. Read the profile / intake and "
              "continue with what they came for.", flush=True)
    else:
        print(f"TIMEOUT nothing submitted within {args.timeout}s; server stopped. "
              f"Ask if they'd rather just do it in chat (references/onboarding.md) "
              f"— that path is fully supported.", flush=True)
        sys.exit(3)


if __name__ == "__main__":
    main()
