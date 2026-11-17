# -*- coding: utf-8 -*-
"""公众号入草稿箱（走后台内部接口，不需要 access_token，也不需要 IP 白名单）。

为什么不用官方 API
------------------
官方 `cgi-bin/draft/add` 要 access_token，而取 token 要求出口 IP 在白名单里；
家用宽带 IP 一换就报 40164。公众号后台自己用的那个接口没有这道门槛：
登录态（cookie）在就能存稿。

用法
----
    # Markdown 正文
    python gzh_save.py --title "文章标题" --md 正文.md --cover ./out/cover_900x383.png \\
           --digest-file 摘要.txt --profile ./gzh-profile --port 9333

    # 已经是微信安全 HTML
    python gzh_save.py --title "文章标题" --html 正文.html --cover ./out/cover_900x383.png

    # 只看会提交什么，不真发（不产生任何请求）
    python gzh_save.py --title "文章标题" --md 正文.md --cover ./out/cover_900x383.png --dry-run

    # 删除某篇草稿（用于测试稿清理）
    python gzh_save.py --delete-appmsgid 100000123 --profile ./gzh-profile --port 9333

成功会打印：DRAFT_OK appmsgid=<数字>

原理（三步）
------------
1. **抓模板**：打开新建文章编辑器，用**真实鼠标坐标**点击「保存为草稿」（JS `.click()`
   不会触发这个按钮），把
   `POST /cgi-bin/operate_appmsg?t=ajax-response&sub=create&type=77` 的完整表单
   （126+ 个字段）抓下来当模板，缓存到 `<profile>/gzh_payload_template.json`，
   之后每次运行直接复用。手工拼字段必报 200002（参数错误），所以必须有模板。
   抓取方式是在页面里给 XMLHttpRequest / fetch / sendBeacon / form.submit 挂钩子
   （实测这个保存请求不会被 Playwright 的网络事件上报），把字段原样抄下来。
   抓完会立刻把这一步产生的占位草稿删掉，不给草稿箱留垃圾。
2. **改字段**：覆盖 `title0` / `content0` / `digest0` / `author0`，并设
   `AppMsgId=""`、`isnew="0"`、`save_type="0"`，同时刷新 `token` 与 `fingerprint`。
   给了摘要还要把 `auto_gen_digest0` 设成 `"0"`，否则服务端会忽略自定义摘要。
3. **建稿**：在页面上下文里用 `fetch(url, {credentials:'include',
   body:new URLSearchParams(fields)})` 提交一次，服务器返回
   `{"appMsgId":...,"ret":"0"}` 即成功。

封面
----
封面走后台素材接口上传（`cgi-bin/filetransfer?action=upload_material&type=image`），
拿到的是 CDN 图片地址，直接写进载荷的 `cdn_url0` / `cdn_235_1_url0`（首图，900×383）
与 `cdn_1_1_url0`（方图，1:1）。这是内部接口的封面字段口径；
`material/add_material`（返 media_id）是官方 API 的口径，需要有 access_token 才用得上，
内部接口这套不需要。封面单张必须小于 2MB，超了脚本会自动用 JPEG 重压。

正文禁止项（会被脚本自检拦下）
------------------------------
`<div>`（会被转成 `<p>` 丢样式）、flex / absolute / grid 布局、`<style>` 块
—— 这些在微信里渲染会错位或掉样式。段落一律是
`<p style="..." data-pm-slice="0 0 []"><span leaf="">文字</span></p>`。
"""

import argparse
import json
import os
import random
import re
import sys
import time
import urllib.parse

DEFAULT_PROFILE = os.path.join(".", "gzh-profile")
DEFAULT_PORT = 9333

MP = "https://mp.weixin.qq.com"
EDITOR_URL = MP + "/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&token=%s&lang=zh_CN"
CREATE_URL = MP + "/cgi-bin/operate_appmsg?t=ajax-response&sub=create&type=77&token=%s&lang=zh_CN"
DELETE_URL = MP + "/cgi-bin/operate_appmsg?t=ajax-response&sub=del&type=77&token=%s&lang=zh_CN"
UPLOAD_URL = (
    MP
    + "/cgi-bin/filetransfer?action=upload_material&type=image&token=%s&lang=zh_CN"
    + "&seq=%d&f=json&writetype=doublewrite&t=iframe-loaddoc&F=m"
)

# 抓模板时写进编辑器的占位标题（抓完这篇占位草稿会被自动删掉）
PLACEHOLDER_TITLE = "模板抓取占位（脚本会自动删除）"

# ---------------------------------------------------------------------------
# 配色（土金板，硬约束）：打底米白/暖白/沙米/浅驼，点睛琥珀金，文字暖黑/深咖/暖灰
# ---------------------------------------------------------------------------
GOLD = "#D4A853"
GOLD2 = "#C9A961"
INK = "#141413"
BODY = "#3D3D3A"
CREAM = "#F5E6D3"
WARM = "#F4F3EE"

P_STYLE = ("font-size:15px;line-height:1.9;color:%s;margin:0 0 16px;letter-spacing:0.3px;" % BODY)
H2_STYLE = (
    "font-size:17px;font-weight:bold;color:%s;border-left:4px solid %s;"
    "padding-left:10px;margin:26px 0 14px;line-height:1.6;letter-spacing:0.5px;" % (INK, GOLD)
)
H3_STYLE = (
    "font-size:16px;font-weight:bold;color:%s;border-left:3px solid %s;"
    "padding-left:9px;margin:22px 0 12px;line-height:1.6;" % (INK, GOLD2)
)
Q_STYLE = (
    "background:%s;border-left:4px solid %s;border-radius:6px;padding:14px 16px;"
    "margin:18px 0;font-size:15px;line-height:1.9;color:%s;letter-spacing:0.3px;" % (CREAM, GOLD, BODY)
)
LI_STYLE = ("font-size:15px;line-height:1.9;color:%s;margin:0 0 10px;padding-left:8px;"
            "letter-spacing:0.3px;" % BODY)
CODE_STYLE = (
    "background:%s;border-radius:6px;padding:14px 16px;margin:16px 0;font-size:13px;"
    "line-height:1.75;color:%s;white-space:pre-wrap;word-break:break-all;"
    "font-family:Consolas,Menlo,monospace;" % (WARM, BODY)
)
HR_STYLE = "text-align:center;color:%s;font-size:13px;letter-spacing:8px;margin:22px 0;" % GOLD2
IMG_WRAP_STYLE = "text-align:center;margin:18px 0;"
IMG_STYLE = "max-width:100%%;height:auto;border-radius:6px;"

# 微信渲染不认的写法，出现在正文里会被自检拦下
FORBIDDEN = (
    "<div",
    "<style",
    "display:flex",
    "display: flex",
    "display:grid",
    "display: grid",
    "position:absolute",
    "position: absolute",
)

BUTTON_SELECTORS = (
    "#js_submit",
    "button:has-text('保存为草稿')",
    "a:has-text('保存为草稿')",
    ".js_submit",
    "button:has-text('保存')",
)


def log(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


# ---------------------------------------------------------------------------
# Markdown → 微信安全 HTML
# ---------------------------------------------------------------------------
def _esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline(t):
    """行内标记：只做加粗/行内码/去链接，先转义再拼，保证标签安全。"""
    t = _esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r'<strong style="color:%s;">\1</strong>' % INK, t)
    t = re.sub(r"`([^`]+)`", r'<code style="background:%s;padding:1px 4px;border-radius:3px;">\1</code>'
               % WARM, t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", t)  # 未认证订阅号放不了外链，只留文字
    return t


def _p(text):
    return '<p style="%s" data-pm-slice="0 0 []"><span leaf="">%s</span></p>' % (P_STYLE, text)


def _h(text, level):
    style = H2_STYLE if level <= 2 else H3_STYLE
    return '<h%d style="%s" data-pm-slice="0 0 []"><span leaf="">%s</span></h%d>' % (
        level, style, text, level)


def _quote(text):
    return '<p style="%s" data-pm-slice="0 0 []"><span leaf="">%s</span></p>' % (Q_STYLE, text)


def _li(text, marker):
    return '<p style="%s" data-pm-slice="0 0 []"><span leaf="">%s %s</span></p>' % (
        LI_STYLE, marker, text)


def _hr():
    return ('<p style="%s" data-pm-slice="0 0 []"><span leaf="">· · ·</span></p>' % HR_STYLE)


def _code(lines):
    body = _esc("\n".join(lines))
    return ('<p style="%s" data-pm-slice="0 0 []"><span leaf="">%s</span></p>' % (CODE_STYLE, body))


def markdown_to_html(md_text, base_dir="."):
    """把 Markdown 转成微信安全 HTML。返回 (html, 待上传图片列表)。

    约定：**每个非空行 = 一个段落**（不做自动合并），这样最贴合中文写作习惯，
    也不会把作者本来分开的段落粘成一大坨。
    """
    lines = md_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    # 去掉 YAML 头信息
    if lines and lines[0].strip() == "---":
        for i in range(1, min(len(lines), 40)):
            if lines[i].strip() == "---":
                lines = lines[i + 1:]
                break

    out, images = [], []
    i = 0
    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        if not s:
            i += 1
            continue

        if s.startswith("```"):
            buf, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append(_code(buf))
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            level = 2 if len(m.group(1)) <= 2 else 3
            out.append(_h(_inline(m.group(2).strip()), level))
            i += 1
            continue

        if re.match(r"^([-*_]\s*){3,}$", s):
            out.append(_hr())
            i += 1
            continue

        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", s)
        if m:
            path = m.group(2).strip()
            if not re.match(r"^https?://", path):
                path = os.path.normpath(os.path.join(base_dir, path))
            images.append(path)
            out.append('<p style="%s" data-pm-slice="0 0 []">'
                       '<img src="{{GZH_IMG_%d}}" style="%s" /></p>' % (IMG_WRAP_STYLE, len(images) - 1, IMG_STYLE))
            i += 1
            continue

        if s.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip())
                i += 1
            out.append(_quote(_inline(" ".join(x for x in buf if x))))
            continue

        m = re.match(r"^(?:[-*+]|\d+[.)])\s+(.*)$", s)
        if m:
            n = 0
            while i < len(lines):
                mm = re.match(r"^(?:[-*+]|\d+[.)])\s+(.*)$", lines[i].strip())
                if not mm:
                    break
                n += 1
                marker = "%d." % n if re.match(r"^\d+[.)]", lines[i].strip()) else "·"
                out.append(_li(_inline(mm.group(1).strip()), marker))
                i += 1
            continue

        out.append(_p(_inline(s)))
        i += 1

    return "\n".join(out), images


def forbidden_hits(html):
    """返回正文里命中的禁用写法（应为空列表）。"""
    low = html.lower()
    return [f for f in FORBIDDEN if f.lower() in low]


# ---------------------------------------------------------------------------
# 载荷模板
# ---------------------------------------------------------------------------
def parse_payload(raw):
    """解析一次真实保存请求的 body：multipart 与 urlencoded 都支持。"""
    raw = (raw or "").replace("\r\r\n", "\r\n")
    fields = {}
    if "form-data" in raw or "WebKitFormBoundary" in raw:
        m = re.search(r"-{4,}[-\w]+", raw)
        if m:
            for part in raw.split(m.group(0)):
                mm = re.search(r'name="([^"]+)"', part)
                if not mm:
                    continue
                if "\r\n\r\n" in part:
                    body = part.split("\r\n\r\n", 1)[1]
                elif "\n\n" in part:
                    body = part.split("\n\n", 1)[1]
                else:
                    body = ""
                fields[mm.group(1)] = body.rstrip("\r\n-")
            return fields
    for k, v in urllib.parse.parse_qsl(raw, keep_blank_values=True):
        fields[k] = v
    return fields


# 页内网络探针。
# 后台的「保存为草稿」走的是 XMLHttpRequest，实测这个请求不会被 Playwright 的网络事件
# 上报（page.on('request') / CDP Network 域都看不到，但草稿确实存进去了）。
# 所以改成在页面里给网络 API 挂钩子，把这一次保存的完整字段原样抄下来当模板。
NET_PROBE = r"""
(() => {
  window.__GZH_CAP = [];
  const hit = (u) => u && String(u).indexOf('operate_appmsg') >= 0
                 && String(u).indexOf('sub=create') >= 0;
  const parts = (b) => {
    try {
      if (!b) return '';
      if (typeof b === 'string') return b;
      if (typeof URLSearchParams !== 'undefined' && b instanceof URLSearchParams) return b.toString();
      if (typeof FormData !== 'undefined' && b instanceof FormData) {
        const p = new URLSearchParams();
        b.forEach((v, k) => { if (typeof v === 'string') p.append(k, v); });
        return p.toString();
      }
      return '';
    } catch (e) { return ''; }
  };
  const rec = (u, b, kind) => {
    try { if (hit(u)) window.__GZH_CAP.push({url: String(u), kind: kind, body: parts(b)}); } catch (e) {}
  };
  const _open = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (m, u) { this.__gzh_u = u; return _open.apply(this, arguments); };
  const _send = XMLHttpRequest.prototype.send;
  XMLHttpRequest.prototype.send = function (b) { rec(this.__gzh_u, b, 'xhr'); return _send.apply(this, arguments); };
  const _fetch = window.fetch;
  if (_fetch) {
    window.fetch = function (u, o) { rec(u && u.url ? u.url : u, o && o.body, 'fetch'); return _fetch.apply(this, arguments); };
  }
  if (navigator.sendBeacon) {
    const _b = navigator.sendBeacon.bind(navigator);
    navigator.sendBeacon = function (u, d) { rec(u, d, 'beacon'); return _b(u, d); };
  }
  const _submit = HTMLFormElement.prototype.submit;
  HTMLFormElement.prototype.submit = function () {
    try { rec(this.getAttribute('action') || this.action, new URLSearchParams(new FormData(this)).toString(), 'form'); } catch (e) {}
    return _submit.apply(this, arguments);
  };
})();
"""


def type_placeholder_title(page, text):
    """往「标题」编辑区真实敲字（返回是否成功）。

    标题是 contenteditable（ProseMirror），直接改 textarea 的 value 不会生效；
    而标题和正文都空的时候，后台会拦住保存，提示「请先输入一段正文（或者标题）」。
    """
    box = None
    try:
        box = page.evaluate("""() => {
          const out = [];
          document.querySelectorAll('[contenteditable="true"], .ProseMirror').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.width > 200 && r.height >= 20 && r.top > 60 && r.top < 400) {
              out.push({x: r.x, y: r.y, w: r.width, h: r.height});
            }
          });
          out.sort((a, b) => a.y - b.y);
          return out.length ? out[0] : null;
        }""")
    except Exception:
        box = None
    if not box:
        return False
    try:
        page.mouse.click(box["x"] + box["w"] / 2.0, box["y"] + box["h"] / 2.0)
        time.sleep(0.5)
        page.keyboard.insert_text(text)
        time.sleep(1.5)
        return True
    except Exception as e:
        log("填写占位标题失败：%s" % e)
        return False


def read_probe(page):
    """读页内探针抄下来的保存请求。"""
    try:
        caps = page.evaluate("() => window.__GZH_CAP || []")
    except Exception:
        return None
    for c in caps or []:
        if c.get("body"):
            return c
    return None


def click_and_read(page):
    click_save(page)
    for _ in range(20):
        time.sleep(1)
        hit = read_probe(page)
        if hit:
            return hit
    return None


def capture_template(page, token):
    """打开新建文章编辑器，真实点击「保存为草稿」，抄下这一次的完整字段当模板。

    这一步会在草稿箱里留下一篇占位草稿（后台保存按钮不接受两样都空），
    所以抓完会立刻按 appmsgid 把它删掉，不给使用者的草稿箱留垃圾。
    """
    captured = {}
    page.add_init_script(NET_PROBE)
    page.goto(EDITOR_URL % token, wait_until="domcontentloaded", timeout=60000)
    time.sleep(8)
    type_placeholder_title(page, PLACEHOLDER_TITLE)
    time.sleep(1.5)
    hit = click_and_read(page)
    if not hit:
        log("第一次点击没抓到，隔 3 秒再点一次…")
        time.sleep(3)
        hit = click_and_read(page)
    if not hit:
        return {}

    url = hit["url"]
    if url.startswith("/"):
        url = MP + url
    captured["url"] = url
    captured["body"] = hit["body"]
    captured["kind"] = hit.get("kind", "")
    # 保存成功后页面会跳到编辑页，URL 里才带上 appmsgid；等它出现，好把占位草稿删掉
    for _ in range(15):
        m = re.search(r"appmsgid=(\d+)", page.url or "")
        if m:
            captured["junk_appmsgid"] = m.group(1)
            break
        time.sleep(1)
    log("抓完后的页面地址：%s" % (page.url or "")[:160])
    return captured


LIST_DRAFTS_JS = """async ([tk, n]) => {
  const r = await fetch(`/cgi-bin/appmsg?begin=0&count=${n}&type=77&action=list_card&token=${tk}&lang=zh_CN&f=json&ajax=1`,
                        {credentials: 'include'});
  const j = await r.json();
  const items = (j.app_msg_info && j.app_msg_info.item) || j.item || [];
  return items.map(i => ({
    id: String(i.app_id || i.appmsgid || ''),
    t: (i.title || (i.multi_item && i.multi_item[0] && i.multi_item[0].title) || '')
  }));
}"""


def list_drafts(page, token, count=20):
    """列草稿箱（标题 + id）。这个接口有速率限制，空了就等一会儿重试。"""
    for _ in range(5):
        try:
            items = page.evaluate(LIST_DRAFTS_JS, [token, count])
        except Exception:
            items = None
        if items:
            return items
        time.sleep(5)
    return []


def find_draft_by_title(page, token, title):
    """按标题找草稿 id（只用来删抓模板时留下的那篇占位草稿）。"""
    for it in list_drafts(page, token):
        if (it.get("t") or "").strip() == title:
            return it.get("id")
    return None


def rebuild_post_url(base_url, token):
    """把模板里的保存地址换成当前 token（缓存下来的模板会带着旧 token）。"""
    if not base_url:
        return CREATE_URL % token
    url = re.sub(r"token=\d+", "token=%s" % token, base_url)
    if "token=" not in url:
        url += ("&" if "?" in url else "?") + "token=%s&lang=zh_CN" % token
    return url


def click_save(page):
    """用真实鼠标坐标点保存按钮（JS .click() 不触发保存）。"""
    for owner in [page] + list(page.frames):
        for sel in BUTTON_SELECTORS:
            try:
                el = owner.query_selector(sel)
            except Exception:
                el = None
            if not el:
                continue
            try:
                box = el.bounding_box()
            except Exception:
                box = None
            if not box or box["width"] < 2 or box["height"] < 2:
                continue
            x = box["x"] + box["width"] / 2.0
            y = box["y"] + box["height"] / 2.0
            try:
                page.mouse.click(x, y)
            except Exception as e:
                log("点击保存按钮失败：%s" % e)
                continue
            log("已用真实坐标 (%.0f, %.0f) 点击保存按钮 %s" % (x, y, sel))
            return True
    log("没找到保存按钮（可能后台改版），将尝试直接构造请求")
    return False


def set_title(page, text):
    """往标题输入区填入文字（JS 赋值，只对 textarea 生效；contenteditable 用 type_placeholder_title）。"""
    js = """(t) => {
      const cands = [document.querySelector('#title'), document.querySelector('textarea.js_title'),
                     document.querySelector('input[name=title]'), document.querySelector('#js_title'),
                     document.querySelector('.js_title_elem')];
      for (const el of cands) {
        if (!el) continue;
        el.value = t;
        el.dispatchEvent(new Event('input', {bubbles: true}));
        el.dispatchEvent(new Event('change', {bubbles: true}));
        el.dispatchEvent(new Event('blur', {bubbles: true}));
        return true;
      }
      return false;
    }"""
    try:
        return bool(page.evaluate(js, text))
    except Exception:
        return False


# ---------------------------------------------------------------------------
# 浏览器侧
# ---------------------------------------------------------------------------
def attach(port):
    from playwright.sync_api import sync_playwright

    p = sync_playwright().start()
    try:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:%d" % port)
    except Exception as e:
        p.stop()
        raise SystemExit(
            "错误：连不上端口 %d 上的浏览器实例（%s）。\n"
            "请先运行：python gzh_login.py --profile ./gzh-profile --port %d" % (port, e, port))
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    page = ctx.new_page()
    return p, browser, ctx, page


def open_backend(page):
    """打开公众平台首页，取 token 与 fingerprint；未登录直接报错退出。"""
    page.goto(MP + "/", wait_until="domcontentloaded", timeout=60000)
    token = None
    for _ in range(8):
        time.sleep(2)
        m = re.search(r"token=(\d+)", page.url or "")
        if m:
            token = m.group(1)
            break
        try:
            body = page.inner_text("body")
        except Exception:
            body = ""
        if body and ("扫一扫" in body or "使用账号登录" in body):
            raise SystemExit("错误：登录态已失效，请重新运行 gzh_login.py 扫码登录。")
    if not token:
        try:
            m2 = re.search(r"token=(\d+)", page.content() or "")
            token = m2.group(1) if m2 else None
        except Exception:
            token = None
    if not token:
        raise SystemExit("错误：页面上取不到 token，请确认浏览器里已登录公众号后台。")
    fingerprint = page.evaluate(
        "() => { const m = document.cookie.match(/fingerprint=([^;]+)/); return m ? m[1] : ''; }")
    return token, (fingerprint or "")


def upload_image(page, token, path, name=None):
    """上传一张图，返回 CDN 地址（正文图与封面都用这个接口）。"""
    if not path or not os.path.exists(path):
        log("缺文件，跳过上传：%s" % path)
        return ""
    data = open(path, "rb").read()
    name = name or os.path.basename(path)
    mime = "image/png" if name.lower().endswith(".png") else "image/jpeg"
    url = UPLOAD_URL % (token, int(time.time() * 1000))
    referer = EDITOR_URL % token
    r = page.request.post(
        url,
        headers={"Referer": referer, "Origin": MP},
        multipart={
            "file": {"name": name, "mimeType": mime, "buffer": data},
            "file_size": str(len(data)),
            "subtype": "image",
            "material_id": "0",
        },
    )
    txt = r.text()
    try:
        j = json.loads(txt)
    except Exception:
        log("  上传 %s 返回无法解析：%s" % (name, txt[:200]))
        return ""
    u = j.get("cdn_url") or j.get("url") or ""
    log("  上传 %s：%s" % (name, ("成功 " + u[:70]) if u else ("失败 " + txt[:180])))
    return u


def prepare_cover(path, limit_mb=1.9):
    """封面必须小于 2MB；超了用 JPEG 重压。返回 (可上传路径, 是否是临时文件)。"""
    size = os.path.getsize(path)
    if size <= limit_mb * 1024 * 1024:
        return path, False
    from PIL import Image

    im = Image.open(path).convert("RGB")
    tmp = os.path.join(os.path.dirname(os.path.abspath(path)), "_cover_compressed.jpg")
    for q in (90, 85, 80, 72, 64):
        im.save(tmp, "JPEG", quality=q, optimize=True)
        if os.path.getsize(tmp) <= limit_mb * 1024 * 1024:
            break
    log("封面 %.2fMB 超过限制，已重压为 %.2fMB（JPEG q=%d）" % (
        size / 1048576.0, os.path.getsize(tmp) / 1048576.0, q))
    return tmp, True


def split_master(path):
    """1283×383 母版 = 左 900×383 首图 + 右 383×383 方图，自动切两张。"""
    from PIL import Image

    im = Image.open(path)
    if im.width < 1281 or not (370 <= im.height <= 400):
        return None, None
    base = os.path.splitext(os.path.abspath(path))[0]
    first = base + "_first_900x383.png"
    square = base + "_square_383x383.png"
    im.crop((0, 0, 900, im.height)).save(first)
    im.crop((900, 0, min(im.width, 900 + im.height), im.height)).resize((383, 383), Image.LANCZOS).save(square)
    log("检测到 %dx%d 母版，已自动切成首图 + 方图" % (im.width, im.height))
    return first, square


def delete_draft(page, token, fingerprint, appmsgid):
    """删除一篇草稿（只用于清理测试稿）。返回是否成功。"""
    fields = {
        "token": token, "lang": "zh_CN", "f": "json", "ajax": "1",
        "random": str(random.random()), "fingerprint": fingerprint or "",
        "AppMsgId": str(appmsgid), "count": "1", "data_seq": "0",
    }
    res = post_fields(page, DELETE_URL % token, fields)
    log("删除响应：%s" % res["text"][:300])
    aid, ret = extract_result(res["text"])
    return str(ret) == "0"


def center_square(path):
    """把封面首图居中裁成 1:1，给「方图」位兜底。

    平台会校验方图是不是真的 1:1（返回 cover_check_info.err_format="1:1"），
    所以不能把 2.35:1 的首图直接塞进方图位。已经是方的就返回 None（不用裁）。
    """
    from PIL import Image

    im = Image.open(path)
    if abs(im.width - im.height) <= 2:
        return None
    side = min(im.width, im.height)
    left = (im.width - side) // 2
    out = os.path.splitext(os.path.abspath(path))[0] + "_square_1x1.png"
    im.crop((left, 0, left + side, side)).save(out)
    log("没给单独方图，已把首图居中裁成 %dx%d 当方图（想要更好效果请用 --square-cover）" % (side, side))
    return out


def extract_result(text):
    """从响应里取 (appmsgid, ret)。"""
    ret, aid = None, None
    try:
        j = json.loads(text)
        for k, v in j.items():
            if k.lower() == "appmsgid":
                aid = str(v)
        br = j.get("base_resp") or {}
        ret = str(j.get("ret", br.get("ret", "")))
    except Exception:
        pass
    if not aid:
        m = re.search(r'"appmsgid"\s*:\s*"?(\d+)"?', text)
        aid = m.group(1) if m else None
    if ret is None:
        m = re.search(r'"ret"\s*:\s*"?(-?\d+)"?', text)
        ret = m.group(1) if m else None
    return aid, ret


POST_JS = """async ([url, fields]) => {
  const sp = new URLSearchParams();
  for (const [k, v] of Object.entries(fields)) sp.append(k, v);
  const r = await fetch(url, {method: 'POST', credentials: 'include',
      headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
      body: sp.toString()});
  return {status: r.status, text: (await r.text()).slice(0, 4000)};
}"""


def post_fields(page, url, fields):
    return page.evaluate(POST_JS, [url, fields])


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="把一篇图文存进公众号草稿箱（后台内部接口，免 access_token / IP 白名单）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--title", help="文章标题")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--md", help="Markdown 正文文件")
    src.add_argument("--html", help="已是微信安全 HTML 的正文文件")
    ap.add_argument("--cover", help="封面首图（900×383；给 1283×383 母版会自动切两张）")
    ap.add_argument("--square-cover", help="封面方图（1:1），不给则用首图或从母版切")
    ap.add_argument("--digest", help="摘要文字（与 --digest-file 二选一）")
    ap.add_argument("--digest-file", help="摘要文件")
    ap.add_argument("--author", default="", help="作者署名（默认留空，用后台账号默认值）")
    ap.add_argument("--profile", default=DEFAULT_PROFILE, help="浏览器数据目录（默认 ./gzh-profile）")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT, help="远程调试端口（默认 9333）")
    ap.add_argument("--payload-template", help="预先抓好的保存请求 body 文件（multipart 或 urlencoded）")
    ap.add_argument("--template-cache", help="模板缓存路径（默认 <profile>/gzh_payload_template.json）")
    ap.add_argument("--dry-run", action="store_true", help="只打印将要提交的内容，不发任何请求")
    ap.add_argument("--delete-appmsgid", help="删除指定草稿后退出（只用于清理测试稿）")
    args = ap.parse_args()

    profile = os.path.abspath(args.profile)
    cache_path = args.template_cache or os.path.join(profile, "gzh_payload_template.json")

    # ---- 单独删除草稿的分支 ----
    if args.delete_appmsgid:
        p, browser, ctx, page = attach(args.port)
        try:
            token, fingerprint = open_backend(page)
            if delete_draft(page, token, fingerprint, args.delete_appmsgid):
                print("DRAFT_DELETED appmsgid=%s" % args.delete_appmsgid)
                return 0
            print("DELETE_FAILED appmsgid=%s" % args.delete_appmsgid)
            return 1
        finally:
            page.close()  # 只关自己的标签页，不关浏览器

    if not args.title:
        raise SystemExit("错误：缺少 --title（标题不能为空）。")
    if not (args.md or args.html):
        raise SystemExit("错误：正文必须给 --md 或 --html 之一。")
    if not args.cover:
        raise SystemExit("错误：缺少 --cover（封面必填）。")

    digest = args.digest or ""
    if args.digest_file:
        digest = open(args.digest_file, encoding="utf-8").read().strip()

    # ---- 正文转换 ----
    images = []
    if args.md:
        md_text = open(args.md, encoding="utf-8").read()
        content, images = markdown_to_html(md_text, os.path.dirname(os.path.abspath(args.md)))
    else:
        html = open(args.html, encoding="utf-8").read()
        m = re.search(r"<body[^>]*>(.*?)</body>", html, re.S)
        content = (m.group(1) if m else html).strip()

    hits = forbidden_hits(content)
    if hits:
        raise SystemExit("错误：正文里出现微信渲染不支持的写法：%s\n"
                         "（<div> 会被转成 <p> 丢样式；flex/absolute/grid 会错位；<style> 块会被剥掉）" % hits)

    cover_first, cover_square = args.cover, args.square_cover
    if not os.path.exists(cover_first):
        raise SystemExit("错误：找不到封面文件 %s" % cover_first)
    sf, sq = split_master(cover_first)
    if sf and not cover_square:
        cover_first, cover_square = sf, sq
    if not cover_square:
        cover_square = center_square(cover_first) or cover_first

    img_note = "、".join(os.path.basename(x) for x in images) or "无"
    log("标题：%s" % args.title)
    log("正文：%d 字符 / 内嵌图片 %d 张（%s）" % (len(content), len(images), img_note))
    log("摘要：%d 字符（%s）" % (len(digest), "自定义" if digest else "交给平台自动生成"))
    log("封面：%s" % os.path.basename(cover_first))

    # ---- 预演 ----
    if args.dry_run:
        fields = {}
        source = ""
        if args.payload_template and os.path.exists(args.payload_template):
            fields = parse_payload(open(args.payload_template, encoding="utf-8", errors="replace").read())
            source = args.payload_template
        elif os.path.exists(cache_path):
            try:
                cached = json.load(open(cache_path, encoding="utf-8"))
            except Exception:
                cached = {}
            if isinstance(cached, dict) and "fields" in cached:
                fields = cached.get("fields") or {}
            else:
                fields = cached if isinstance(cached, dict) else {}
            source = cache_path
        overrides = ["AppMsgId", "isnew", "save_type", "random", "token", "fingerprint",
                     "title0", "content0", "digest0", "author0",
                     "cdn_url0", "cdn_235_1_url0", "cdn_1_1_url0", "auto_gen_digest0"]
        print("===== 预演（dry-run）：不会发起任何请求 =====")
        print("标题          : %s" % args.title)
        print("正文字符数    : %d" % len(content))
        print("正文图片数    : %d" % len(images))
        print("禁用写法自检  : 通过（无 div / flex / absolute / grid / <style>）")
        print("摘要          : %d 字符" % len(digest))
        print("封面首图      : %s (%d 字节)" % (cover_first, os.path.getsize(cover_first)))
        print("封面方图      : %s (%d 字节)" % (cover_square, os.path.getsize(cover_square)))
        if fields:
            print("载荷字段数    : %d（模板来源：%s）" % (len(fields), source))
            print("字段名前 20 个: %s" % ", ".join(list(fields.keys())[:20]))
        else:
            print("载荷字段数    : 模板尚未就绪（首次真实运行时会现场抓取一次，约 127 个字段）")
        print("将覆盖字段    : %s" % ", ".join(overrides))
        print("未发起 POST。")
        return 0

    # ---- 附着浏览器 ----
    p, browser, ctx, page = attach(args.port)
    try:
        token, fingerprint = open_backend(page)
        log("token=%s fingerprint=%s" % (token, (fingerprint[:8] + "…") if fingerprint else "无"))

        # 模板：参数文件 > 本地缓存 > 现场抓取
        template, post_url = {}, ""
        if args.payload_template and os.path.exists(args.payload_template):
            template = parse_payload(open(args.payload_template, encoding="utf-8", errors="replace").read())
            log("已从文件加载载荷模板：%s（%d 字段）" % (args.payload_template, len(template)))
        elif os.path.exists(cache_path):
            try:
                cached = json.load(open(cache_path, encoding="utf-8"))
            except Exception as e:
                cached = {}
                log("模板缓存读不出来（%s），将重新抓取。" % e)
            if isinstance(cached, dict) and "fields" in cached:
                template = cached.get("fields") or {}
                post_url = cached.get("captured_url") or ""
            elif isinstance(cached, dict):
                template = cached
            if template:
                log("已从缓存加载载荷模板：%s（%d 字段）" % (cache_path, len(template)))
        if len(template) < 20:
            log("没有可用模板，打开编辑器现场抓一次（会留下一篇占位草稿，抓完自动删除）…")
            captured = capture_template(page, token)
            if not captured.get("body"):
                raise SystemExit(
                    "错误：没能抓到保存请求的模板。\n"
                    "请手动抓一次：打开新建文章编辑器 → F12 → Network → 点「保存为草稿」→\n"
                    "右键该请求 → Copy → Copy as cURL，把 body 存成文件后用 --payload-template 传入。")
            template = parse_payload(captured["body"])
            post_url = captured.get("url") or ""
            log("抓到模板：%d 个字段（传输方式 %s）" % (len(template), captured.get("kind") or "?"))
            if len(template) < 20:
                raise SystemExit("错误：抓到的模板字段数异常（%d），请检查后台是否改版。" % len(template))
            tidy_fields = dict(template)
            tidy_fields["token"] = ""
            tidy_fields["fingerprint"] = ""
            tidy_url = re.sub(r"token=\d+", "token=", post_url)
            cache_dir = os.path.dirname(os.path.abspath(cache_path))
            if cache_dir and not os.path.isdir(cache_dir):
                os.makedirs(cache_dir, exist_ok=True)
            json.dump({"captured_url": tidy_url, "fields": tidy_fields},
                      open(cache_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            log("模板已缓存到 %s（token/fingerprint 已清空，每次运行会重新取）" % cache_path)
            # 把抓模板时留下的占位草稿删掉：优先用 URL 上的 appmsgid，找不到就按标题捞
            junk = captured.get("junk_appmsgid")
            if not junk:
                junk = find_draft_by_title(page, token, PLACEHOLDER_TITLE)
            if junk:
                ok = delete_draft(page, token, fingerprint, junk)
                log("占位草稿 %s：%s" % (junk, "已删除" if ok else "删除失败，请到草稿箱手动删掉"))
            else:
                log("没能定位到抓模板留下的占位草稿，若草稿箱里出现「%s」请手动删除" % PLACEHOLDER_TITLE)
        post_url = rebuild_post_url(post_url, token)

        # 正文图上传
        for idx, local in enumerate(images):
            url = upload_image(page, token, local)
            if not url:
                raise SystemExit("错误：正文图片上传失败，已中止（避免存进一篇裂图的草稿）。")
            content = content.replace("{{GZH_IMG_%d}}" % idx, url)

        # 封面上传
        c1, tmp1 = prepare_cover(cover_first)
        c2, tmp2 = prepare_cover(cover_square)
        u_first = upload_image(page, token, c1, os.path.basename(c1))
        u_square = upload_image(page, token, c2, os.path.basename(c2))
        for f, tmp in ((c1, tmp1), (c2, tmp2)):
            if tmp:
                try:
                    os.remove(f)
                except Exception:
                    pass

        # 组装字段
        fields = dict(template)
        fields["token"] = token
        if fingerprint:
            fields["fingerprint"] = fingerprint
        fields["title0"] = args.title
        fields["content0"] = content
        fields["author0"] = args.author
        fields["AppMsgId"] = ""
        fields["isnew"] = "0"
        fields["save_type"] = "0"
        fields["random"] = str(random.random())
        if digest:
            fields["digest0"] = digest
            fields["auto_gen_digest0"] = "0"  # 不给 0，服务端会忽略自定义摘要
        if u_first:
            fields["cdn_url0"] = u_first
            fields["cdn_235_1_url0"] = u_first   # 首图 2.35:1
        if u_square:
            fields["cdn_1_1_url0"] = u_square    # 方图 1:1
        if not u_first or not u_square:
            raise SystemExit("错误：封面没上传成功，已中止（封面为空时存不进草稿箱）。")

        log("提交 %d 个字段到 %s…" % (len(fields), post_url.split("?")[0]))
        res = post_fields(page, post_url, fields)
        log("HTTP %s" % res["status"])
        log("响应：%s" % res["text"][:600])
        aid, ret = extract_result(res["text"])
        if aid and str(ret) in ("0", "None", ""):
            print("DRAFT_OK appmsgid=%s" % aid)
            return 0
        print("DRAFT_FAILED ret=%s appmsgid=%s" % (ret, aid))
        return 1
    finally:
        try:
            page.close()
        except Exception:
            pass
        try:
            p.stop()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
