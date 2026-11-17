#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""juejin-publisher：掘金全自动发布 + 知乎 CDP 半自动（Markdown → 平台）

2026-09 逆向实测口径（真实账号全链路验证过）：
  * 所有 api.juejin.cn 请求带 ?aid=2608&uuid=<19位>
  * 建草稿响应里 article_id 恒为 "0"（未发布语义），真实草稿 ID 在 data.id
  * 每篇文章最多 2 个标签（err 4031）；标签搜索 = tag_api/v1/query_tag_list {key_word}
  * 发布体 = {"draft_id","sync_to_org":false,"column_ids":[...],"theme_ids":[],
              "origin_word_count","encrypted_word_count"}，专栏靠 column_ids
  * 专栏挂载靠 column_ids；封面（掘金 192×128 / 知乎 1200×675 / 专栏 16:9）PIL 自动生成并上传
  * 专栏管理 API（2026-09-17 实测）：column/publish 无 column_id=新建（data 返回新 id）、
    带 column_id=更新（title/content/cover）；column/delete {column_id} 删除
  * 分类：人工智能 6809637773935378440（可在 frontmatter category_id 覆盖）

用法（uv run 或任意 python3.10+；依赖 websockets、pillow）：

  uv run publish.py login                 # 浏览器扫码：掘金抓 Cookie + 知乎顺手登录
  uv run publish.py whoami                # 校验 Cookie / 显示账号，并记住 user_id
  uv run publish.py preview 文章.md     # 离线校验（摘要 50~100、checklist 剥离、标签映射）
  uv run publish.py tags <关键词>          # 搜掘金标签 ID
  uv run publish.py columns               # 列出我的专栏；--use <id> 切换默认专栏
  uv run publish.py column-new 标题        # 新建专栏（纯 API），--intro 简介 --use 设为默认
  uv run publish.py column-cover          # 专栏上 PIL 封面（16:9），--column <id> 指定专栏
  uv run publish.py draft  文章.md      # 建掘金草稿（含分类+双标签+摘要+专栏不挂）
  uv run publish.py publish 文章.md     # 全自动发布：草稿→挂专栏→发布→返回链接
  uv run publish.py cover  文章.md      # PIL 生成 192×128 封面并经编辑器上传（草稿需先建）
  uv run publish.py zhihu  文章.md      # CDP：知乎写文章页自动填标题正文，人工点发布
  uv run publish.py zhihu  文章.md --auto   # 同上，且自动点「发布」（一键直发，实测 2026-09-18）
  uv run publish.py html   文章.md      # 调试：预览知乎粘贴用 HTML

体例（强制）：HTML 注释（内部 checklist）剥离；掘金 title_juejin / 知乎 title_zhihu；
摘要 50~100 字；接口间隔 ≥2.5 秒。
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POSTS = ROOT / "posts"
WF = ROOT / "_wf"
ENV_FILE = ROOT / ".juejin.env"
META_FILE = WF / "juejin_meta.json"
TAG_CACHE = WF / "juejin_tag_cache.json"
CDP_PROFILE = ROOT / ".cdp-profile"

API = "https://api.juejin.cn"
CREATE_URL = f"{API}/content_api/v1/article_draft/create"
PUBLISH_URLS = [
    f"{API}/content_api/v1/article/publish",
    f"{API}/content_api/v1/article_draft/publish",
]
USER_URL = f"{API}/user_api/v1/user/get"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
CALL_GAP_SECONDS = 2.5
AID = "2608"

CDP_PORT = 9222
CDP_HTTP = f"http://127.0.0.1:{CDP_PORT}"

# 已验证的掘金标签（2026-09-13 实测解析）
KNOWN_TAGS = {
    "人工智能": "6809640642101116936",
    "面试": "6809640404791590919",
    "架构": "6809640501776482317",
    "团队管理": "6809641183699009550",
    "程序员": "6809640482725953550",
    "AI编程": "7467857238494019610",
}
# frontmatter 标签名 → 掘金真实标签（掘金没有的映射到最近义；None=丢弃）
TAG_FALLBACK = {
    "AI": "人工智能", "人工智能": "人工智能",
    "职业发展": "程序员", "转型": "程序员", "行业观察": "程序员",
    "求职面试": "面试", "面试": "面试",
    "企业管理": "团队管理", "项目管理": "团队管理", "商业模式": "团队管理",
    "系统架构": "架构", "能力模型": "架构",
    "企业服务": None, "工业互联网": None,
}


def die(msg: str) -> None:
    print(f"✗ {msg}", file=sys.stderr)
    sys.exit(1)


# ------------------------------------------------------------------- meta

def load_meta() -> dict:
    if META_FILE.exists():
        try:
            return json.loads(META_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def save_meta(meta: dict) -> None:
    WF.mkdir(exist_ok=True)
    META_FILE.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def device_uuid() -> str:
    meta = load_meta()
    if not meta.get("uuid"):
        meta["uuid"] = str(random.randint(10 ** 18, 10 ** 19 - 1))
        save_meta(meta)
    return meta["uuid"]


# ---------------------------------------------------------------- frontmatter

def parse_post(path: Path) -> dict:
    """解析 frontmatter + 剥离 HTML 注释后的正文。"""
    if not path.exists():
        die(f"文件不存在：{path}")
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", raw, flags=re.S)
    if not m:
        die(f"{path.name} 缺 frontmatter（--- 区块）")
    meta, body = m.group(1), m.group(2)

    fields: dict[str, str] = {}
    for line in meta.splitlines():
        km = re.match(r"^([A-Za-z_]+)\s*:\s*(.*)$", line.strip())
        if km:
            fields[km.group(1)] = km.group(2).strip().strip('"').strip("'")

    # 内部 checklist 等一切 HTML 注释绝不外发
    clean_body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    clean_body = re.sub(r"\n{3,}", "\n\n", clean_body).strip() + "\n"

    return {
        "file": path,
        "title_juejin": fields.get("title_juejin", ""),
        "title_zhihu": fields.get("title_zhihu", ""),
        "description": fields.get("description", ""),
        "category_id": fields.get("category_id", "6809637773935378440"),
        "tags": [t.strip() for t in fields.get("tags", "").split(",") if t.strip()],
        "tag_ids": [t.strip() for t in fields.get("tag_ids", "").split(",") if t.strip()],
        "cover_image": fields.get("cover", ""),
        "body": clean_body,
    }


def check_brief(desc: str) -> tuple[str, list[str]]:
    """掘金硬限制：摘要 50~100 字。"""
    warns = []
    brief = desc.strip()
    n = len(brief)
    if n < 50:
        die(f"摘要仅 {n} 字，低于掘金 50 字下限——请扩写 frontmatter description")
    if n > 100:
        brief = brief[:100]
        warns.append(f"摘要 {n} 字超上限，已截断为 100 字")
    return brief, warns


# ------------------------------------------------------------------- http

def load_cookie() -> str:
    cookie = os.environ.get("JUEJIN_COOKIE", "")
    if not cookie and ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUEJIN_COOKIE="):
                cookie = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not cookie:
        die("未配置 Cookie——先跑 `uv run publish.py login` 扫码登录")
    if "=" not in cookie:
        cookie = f"sessionid={cookie}"
    return cookie


def http_json(url: str, payload: dict | None = None, cookie: str | None = None) -> dict:
    headers = {"User-Agent": UA, "Referer": "https://juejin.cn/"}
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        headers["Origin"] = "https://juejin.cn"
        body = json.dumps(payload).encode("utf-8")
    if cookie:
        headers["Cookie"] = cookie
    # 掘金网关要求 aid/uuid（实测缺省会报「请求路由不存在」）
    if "api.juejin.cn" in url and "aid=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}aid={AID}&uuid={device_uuid()}"
    req = urllib.request.Request(url, data=body, headers=headers,
                                 method="POST" if payload is not None else "GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def api(path: str, payload: dict | None, cookie: str | None = None) -> dict:
    """带异常包装与退避重试的掘金 API 调用（path 接受 /xxx 相对路径或完整 URL）。"""
    url = path if path.startswith("http") else f"{API}{path}"
    last_exc: Exception | None = None
    for attempt in range(3):
        try:
            return http_json(url, payload, cookie)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300]
            if e.code in (401, 403):
                die(f"HTTP {e.code}：Cookie 失效或被风控——重跑 `uv run publish.py login`。响应：{detail}")
            die(f"HTTP {e.code}：{detail}")
        except (urllib.error.URLError, json.JSONDecodeError, OSError) as e:
            last_exc = e
            time.sleep(3 * (attempt + 1))          # WAF 对密集握手敏感，退避重试
    die(f"网络错误（已重试三次）：{last_exc}\n"
        f"  若持续 SSL 断连，多为设备 uuid 被风控——跑一次 `login` 让工具记录浏览器 uuid")


# --------------------------------------------------------------------- tags

def load_tag_cache() -> dict:
    if TAG_CACHE.exists():
        try:
            return json.loads(TAG_CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_tag_cache(cache: dict) -> None:
    WF.mkdir(exist_ok=True)
    TAG_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def search_tags(keyword: str, cookie: str) -> list[dict]:
    """标签搜索（实测口径：query_tag_list，名字嵌套在 tag.tag_name）。"""
    r = api("/tag_api/v1/query_tag_list",
            {"cursor": "0", "key_word": keyword, "limit": 8, "sort_type": 1}, cookie)
    data = r.get("data")
    if isinstance(data, dict):
        data = data.get("data")
    out = []
    for it in data or []:
        if isinstance(it, dict) and it.get("tag_id"):
            name = (it.get("tag") or {}).get("tag_name") or str(it.get("tag_id"))
            out.append({"id": str(it["tag_id"]), "title": name})
    return out[:8]


def resolve_tag_ids(post: dict, cookie: str, interactive: bool = True) -> list[str]:
    """frontmatter tag_ids 优先；否则经 FALLBACK 映射 + 缓存 + 搜索解析。
    硬约束：掘金每篇最多 2 个标签，至少 1 个。"""
    if post["tag_ids"]:
        return post["tag_ids"][:2]
    cache = dict(KNOWN_TAGS)
    cache.update(load_tag_cache())
    resolved: list[str] = []
    missing = []
    for name in post["tags"]:
        target = TAG_FALLBACK.get(name, name)
        if target is None:
            continue
        if target in cache:
            tid = cache[target]
        else:
            found = search_tags(target, cookie)
            if not found:
                missing.append(f"{name}→{target}")
                continue
            tid = found[0]["id"]
            if interactive and len(found) > 1:
                print(f"  「{target}」多个候选：")
                for i, f in enumerate(found):
                    print(f"    [{i}] {f['title']}  {f['id']}")
                sel = input(f"  选择 [0-{len(found)-1}]，回车默认 0：").strip()
                tid = found[int(sel)]["id"] if sel.isdigit() and int(sel) < len(found) else tid
            time.sleep(CALL_GAP_SECONDS)
        if tid not in resolved:
            resolved.append(tid)
    if len(resolved) == 1 and cache.get("人工智能") and cache["人工智能"] not in resolved:
        resolved.append(cache["人工智能"])          # 只解析到一个时，补人工智能凑双标签
    if not resolved:
        die(f"一个标签都没解析到（{','.join(post['tags'])}）——用 `tags` 命令查 ID 后写进 frontmatter tag_ids")
    if missing:
        print(f"⚠ 以下标签掘金不存在、已按映射丢弃：{'、'.join(missing)}")
    return resolved[:2]


# ------------------------------------------------------------------ 掘金发布

def create_draft(post: dict, brief: str, tag_ids: list[str], cookie: str) -> str:
    payload = {
        "category_id": str(post["category_id"]),
        "tag_ids": tag_ids,
        "title": post["title_juejin"],
        "brief_content": brief,
        "edit_type": 10,               # Markdown 模式
        "mark_content": post["body"],
        "cover_image": post["cover_image"],
        "html_content": "deprecated",
        "link_url": "",
        "theme_ids": [],
    }
    r = api(CREATE_URL, payload, cookie)
    if r.get("err_no") != 0:
        die(f"建草稿失败：[{r.get('err_no')}] {r.get('err_msg')}")
    data = r.get("data") or {}
    # 掘金返回的 article_id 恒为 "0"（未发布语义），真实草稿 ID 在 id 字段
    draft_id = str(data.get("id") or "")
    if draft_id in ("", "0"):
        die(f"建草稿返回异常：{json.dumps(r, ensure_ascii=False)[:300]}")
    return draft_id


def column_id_from_meta() -> str | None:
    meta = load_meta()
    if meta.get("column_id"):
        return meta["column_id"]
    cookie = load_cookie()
    uid = meta.get("user_id")
    if not uid:
        uid = str((api(USER_URL, None, cookie).get("data") or {}).get("user_id") or "")
        if uid:
            meta = load_meta(); meta["user_id"] = uid; save_meta(meta)
    if not uid:
        return None
    r = api("/content_api/v1/column/self_center_list",
            {"user_id": uid, "cursor": "0", "keyword": "", "limit": 20}, cookie)
    data = r.get("data")
    items = data if isinstance(data, list) else (data or {}).get("data") or []
    if len(items) == 1:                      # 只有一个专栏时直接用它
        c = items[0].get("column") or {}
        meta = load_meta(); meta["column_id"] = c.get("column_id"); save_meta(meta)
        return c.get("column_id")
    return None                              # 多个/零个专栏：让用户 columns --use 指定


def publish_draft(draft_id: str, cookie: str, word_count: int,
                  column_id: str | None) -> str:
    """发布（实测 schema：column_ids 挂专栏，word_count 双字段）。"""
    payload = {
        "draft_id": draft_id,
        "sync_to_org": False,
        "column_ids": [column_id] if column_id else [],
        "theme_ids": [],
        "origin_word_count": word_count,
        "encrypted_word_count": word_count,
    }
    last_err = ""
    for url in PUBLISH_URLS:
        r = api(url, payload, cookie)
        if r.get("err_no") == 0:
            data = r.get("data") or {}
            article_id = str(data.get("article_id") or data.get("id") or draft_id)
            print(f"✓ 已发布：https://juejin.cn/post/{article_id}"
                  + ("（已收录默认专栏）" if column_id else ""))
            time.sleep(CALL_GAP_SECONDS)
            hint = article_status_hint(article_id, cookie)
            if hint:
                print(f"· 状态：{hint}")
            return article_id
        last_err = f"[{r.get('err_no')}] {r.get('err_msg')}"
        time.sleep(CALL_GAP_SECONDS)
    die(f"发布失败（草稿 {draft_id} 已保留，可到掘金后台手动发布）：{last_err}")


def article_status_hint(article_id: str, cookie: str) -> str:
    """发布后自查：先看 audit_status（驳回时 status 仍是 0，别误读成审核中）。"""
    try:
        r = api("/content_api/v1/article/detail", {"article_id": article_id, "forbid_count": True}, cookie)
        info = ((r.get("data") or {}).get("article_info") or {})
        st = info.get("status")
        if info.get("audit_status") == -1:
            return ("已被驳回（audit_status=-1）——常见触发：标题/正文含招聘语汇＋钱数组合"
                    "（高薪、招聘、求职、猎头 + 金额数字）或招聘平台 URL。清理后删旧文重发")
        if st == 0:
            return ("审核中——前台暂不可见属正常（含外链/招聘薪资类内容易触发人审，"
                    "一般几分钟到几小时；创作者中心→内容管理可看进度）")
        if st in (1, 2):
            return "已上线，前台可见"
        return f"status={st}"
    except SystemExit:
        return ""


def cmd_status(args) -> None:
    cookie = load_cookie()
    print(article_status_hint(args.article_id, cookie) or "查询失败")


def cmd_cleanup(args) -> None:
    """关闭 CDP 浏览器里堆积的标签（保留一个保活；--all 连知乎写作页一起清）。"""
    ensure_browser()
    tabs = list_tabs()
    if not tabs:
        print("（浏览器没有页面标签）")
        return
    keep_zhihu = not getattr(args, "all", False)
    doomed = [t for t in tabs
              if not (keep_zhihu and "zhuanlan.zhihu.com/write" in t.get("url", ""))]
    if len(doomed) == len(tabs):
        doomed = doomed[:-1]              # 至少留一个标签保活，否则窗口退出、CDP 断线
    closed = 0
    for t in doomed:
        try:
            tab = Tab(t["webSocketDebuggerUrl"])
            tab.call("Target.closeTarget", targetId=t["id"])
            tab.close()
            closed += 1
        except Exception:
            continue
    print(f"✓ 已关闭 {closed}/{len(tabs)} 个标签（保留 {len(tabs) - closed} 个保活）")


# ---------------------------------------------------------------------- CDP

BROWSER_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    Path.home() / r"AppData\Local\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def find_browser() -> str:
    for c in BROWSER_CANDIDATES:
        if Path(c).exists():
            return str(c)
    die("未找到 Chrome/Edge——请安装任一 Chromium 系浏览器")


def cdp_alive() -> bool:
    try:
        with urllib.request.urlopen(f"{CDP_HTTP}/json/version", timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


def ensure_browser(url: str = "about:blank") -> None:
    if cdp_alive():
        return
    exe = find_browser()
    args = [exe, f"--remote-debugging-port={CDP_PORT}",
            f"--user-data-dir={CDP_PROFILE}",
            "--no-first-run", "--no-default-browser-check", "--restore-last-session=false",
            url]
    subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        if cdp_alive():
            return
        time.sleep(0.2)
    die("浏览器调试端口未就绪——手动检查 9222 端口是否被占用")


class Tab:
    """对一个页面 target 的同步 CDP 会话。"""

    def __init__(self, ws_url: str):
        from websockets.sync.client import connect as ws_connect
        # websockets 17：connect() 必须走上下文管理器，直连会触发弃用告警
        self._cm = ws_connect(ws_url, open_timeout=10, close_timeout=5)
        self.ws = self._cm.__enter__()
        self._id = 0
        self.target_id: str | None = None   # 页面 target，close_page 用
        self.requests: list[dict] = []      # Network.requestWillBeSent 事件缓存

    def close(self) -> None:
        try:
            self._cm.__exit__(None, None, None)
        except Exception:
            pass

    def close_page(self) -> None:
        """连 WebSocket 一起把页面标签关掉——长期驻留的 CDP 浏览器不关页会标签堆积卡死。"""
        if self.target_id:
            try:
                self.call("Target.closeTarget", targetId=self.target_id)
            except Exception:
                pass
        self.close()

    def _handle_event(self, msg: dict) -> None:
        if msg.get("method") == "Network.requestWillBeSent":
            req = msg.get("params", {}).get("request", {})
            self.requests.append({
                "url": req.get("url", ""),
                "method": req.get("method", ""),
                "post": (req.get("postData") or "")[:300],
            })

    def pump(self, seconds: float) -> None:
        """等待并持续接收事件 seconds 秒，期间的网络请求记入 self.requests。"""
        deadline = time.time() + seconds
        while time.time() < deadline:
            try:
                msg = json.loads(self.ws.recv(timeout=1))
            except TimeoutError:
                continue
            if msg.get("id") is None:
                self._handle_event(msg)

    def call(self, method: str, **params) -> dict:
        self._id += 1
        self.ws.send(json.dumps({"id": self._id, "method": method, "params": params}))
        deadline = time.time() + 30
        while time.time() < deadline:
            msg = json.loads(self.ws.recv(timeout=max(1, deadline - time.time())))
            if msg.get("id") == self._id:
                if "error" in msg:
                    raise RuntimeError(f"CDP {method}: {msg['error']}")
                return msg.get("result", {})
            self._handle_event(msg)
        raise TimeoutError(f"CDP {method} 超时")

    def evaluate(self, js: str) -> object:
        r = self.call("Runtime.evaluate", expression=js, returnByValue=True)
        if r.get("exceptionDetails"):
            raise RuntimeError(f"页面脚本异常：{r['exceptionDetails'].get('text')}")
        return r.get("result", {}).get("value")

    def navigate(self, url: str) -> None:
        self.call("Page.navigate", url=url)

    def cookies(self, urls: list[str]) -> list[dict]:
        r = self.call("Network.getCookies", urls=urls)
        return r.get("cookies", [])


def list_tabs() -> list[dict]:
    try:
        with urllib.request.urlopen(f"{CDP_HTTP}/json", timeout=5) as r:
            return [t for t in json.loads(r.read().decode("utf-8")) if t.get("type") == "page"]
    except Exception:
        return []


def open_tab(url: str, reuse_prefix: str | None = None) -> Tab:
    """打开页面标签；给 reuse_prefix 时优先复用现有页（防长期运行的浏览器标签堆积）。"""
    if reuse_prefix:
        for t in list_tabs():
            if t.get("url", "").startswith(reuse_prefix) and t.get("webSocketDebuggerUrl"):
                tab = Tab(t["webSocketDebuggerUrl"])
                tab.target_id = t["id"]
                return tab
    for method in ("PUT", "GET"):     # Chrome 111+ 要求 PUT
        try:
            req = urllib.request.Request(
                f"{CDP_HTTP}/json/new?{urllib.parse.quote(url, safe=':/%?=&')}", method=method)
            with urllib.request.urlopen(req, timeout=5) as r:
                target = json.loads(r.read().decode("utf-8"))
            if target.get("webSocketDebuggerUrl"):
                tab = Tab(target["webSocketDebuggerUrl"])
                tab.target_id = target.get("id")
                return tab
        except urllib.error.HTTPError:
            continue
    die("无法新建标签页——浏览器可能弹了确认框，点一下再重试")


def wait_page(tab: Tab, js_probe: str, timeout: int = 30, interval: float = 1.0,
              desc: str = "页面就绪") -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if tab.evaluate(js_probe):
                return
        except Exception:
            pass
        time.sleep(interval)
    die(f"等待{desc}超时——浏览器窗口里可能需要人工处理（登录/验证码）")


def cookie_header(cookies: list[dict], want: list[str]) -> tuple[str, list[str]]:
    pairs = [f"{c['name']}={c['value']}" for c in cookies if c.get("name") and c.get("value")]
    names = {c["name"] for c in cookies}
    return "; ".join(pairs), [w for w in want if w not in names]


def save_env(cookie_header_str: str) -> None:
    ENV_FILE.write_text(f"JUEJIN_COOKIE={cookie_header_str}\n", encoding="utf-8")


def harvest_uuid(tab: Tab) -> str | None:
    """从页面请求的 query 里收割真实设备 uuid（WAF 校验，随机值会被掐连接）。"""
    for r in reversed(tab.requests):
        m = re.search(r"[?&]uuid=(\d{15,})", r["url"])
        if m:
            return m.group(1)
    return None


def cmd_login(args) -> None:
    ensure_browser()
    tab = open_tab("https://juejin.cn")
    tab.call("Network.enable")
    print("· 已打开掘金——请扫码/登录（独立 profile，不影响日常 Chrome；已登录过则自动跳过）")
    print("· 等待掘金登录态…（最长 5 分钟，检测到 sessionid 自动继续）")
    deadline = time.time() + 300
    while time.time() < deadline:
        try:
            cs = tab.cookies(["https://juejin.cn", "https://api.juejin.cn"])
            sid = next((c for c in cs if c["name"] == "sessionid"), None)
            if sid:
                header, _ = cookie_header(cs, ["sessionid"])
                save_env(header)
                exp = sid.get("expires", 0)
                exp_s = time.strftime("%Y-%m-%d", time.localtime(exp)) if exp else "约 30 天"
                print(f"✓ 掘金 sessionid 已写入 {ENV_FILE.name}（有效期至 {exp_s}）")
                duuid = harvest_uuid(tab)
                if duuid:
                    meta = load_meta()
                    meta["uuid"] = duuid
                    save_meta(meta)
                    print(f"✓ 设备 uuid 已记录（{duuid[:6]}…）")
                break
        except Exception:
            pass
        time.sleep(3)
    else:
        tab.close_page()
        die("5 分钟内未检测到掘金登录——确认扫码成功后重跑 login")
    tab.close_page()

    ztab = open_tab("https://www.zhihu.com/signin?next=%2Fwrite")
    print("· 已打开知乎登录页——顺手扫码（zhihu 命令要用；现在不想登可 Ctrl+C 跳过，或等 3 分钟自动跳过）")
    try:
        zdeadline = time.time() + 180
        while time.time() < zdeadline:
            try:
                zc = ztab.cookies(["https://www.zhihu.com", "https://zhuanlan.zhihu.com"])
                if any(c["name"] in ("z_c_y", "SESSIONID") for c in zc):
                    print("✓ 知乎登录态已就绪——zhihu 命令可直用")
                    break
            except Exception:
                pass
            time.sleep(3)
        else:
            print("· 未检测到知乎登录——之后跑 zhihu 命令时会再等一次，不影响掘金通道")
    except KeyboardInterrupt:
        print("· 已跳过知乎登录")
    ztab.close_page()
    print("→ 全部就绪：draft/publish 走掘金 API，zhihu 走浏览器注入")


def cmd_whoami(args) -> None:
    cookie = load_cookie()
    r = api(USER_URL, None, cookie)   # 浏览器口径为 GET
    if r.get("err_no") != 0:
        die(f"Cookie 无效或过期（[{r.get('err_no')}] {r.get('err_msg')}）——重跑 login")
    u = r.get("data") or {}
    meta = load_meta()
    if u.get("user_id"):
        meta["user_id"] = str(u["user_id"])
        save_meta(meta)
    print(f"✓ Cookie 有效：{u.get('user_name')}（掘金 ID {u.get('user_id')}）")


# --------------------------------------------------------- Markdown → HTML

def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    return s


def md_to_html(md: str) -> str:
    """把系列 Markdown（标题/加粗/行内码/列表/引用/表格/代码块/链接/分隔线）转成
    知乎编辑器可粘贴的 HTML 片段。覆盖 posts/*.md 用到的全部语法。"""
    out: list[str] = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):                                  # 围栏代码块
            lang = s[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i]); i += 1
            i += 1
            out.append(f'<pre><code data-lang="{esc(lang)}">{esc(chr(10).join(code))}</code></pre>')
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)                   # 标题
        if m:
            out.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>")
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,})$", s):                    # 分隔线
            out.append("<hr>")
            i += 1
            continue
        if s.startswith(">"):                                   # 引用块（含 > 嵌套行）
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i].strip()))
                i += 1
            inner: list[str] = []
            for q in quote:
                qm = re.match(r"^(#{1,6})\s+(.*)$", q.strip())
                inner.append(f"<p><strong>{inline(qm.group(2))}</strong></p>" if qm
                             else f"<p>{inline(q)}</p>")
            out.append("<blockquote>" + "".join(inner) + "</blockquote>")
            continue
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|?$", lines[i + 1].strip()):
            rows = [s]                                          # 表格
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip()); i += 1
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
            thead = "".join(f"<th>{inline(c)}</th>" for c in cells[0])
            trs = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:])
            out.append(f"<table><thead><tr>{thead}</tr></thead><tbody>{trs}</tbody></table>")
            continue
        if re.match(r"^[-*]\s+", s):                            # 无序列表
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].strip()):
                txt = re.sub(r"^[-*]\s+", "", lines[i].strip())
                items.append(f"<li>{inline(txt)}</li>")
                i += 1
            out.append(f"<ul>{''.join(items)}</ul>")
            continue
        if re.match(r"^\d+[.、]\s+", s):                        # 有序列表
            items = []
            while i < len(lines) and re.match(r"^\d+[.、]\s+", lines[i].strip()):
                txt = re.sub(r"^\d+[.、]\s+", "", lines[i].strip())
                items.append(f"<li>{inline(txt)}</li>")
                i += 1
            out.append(f"<ol>{''.join(items)}</ol>")
            continue
        out.append(f"<p>{inline(s)}</p>")                      # 普通段落
        i += 1
    return "\n".join(out)


# -------------------------------------------------------------------- 知乎

ZHIHU_WRITE = "https://zhuanlan.zhihu.com/write"


def make_cover_zhihu(post: dict) -> Path:
    """知乎封面：1200×675（16:9），深底 + 系列名 + 篇名。"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        die("缺 PIL——`uv add pillow` 后重试")
    w, h = 1200, 675
    img = Image.new("RGB", (w, h), "#121217")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 18], fill="#2e6cff")
    font = small = None
    for fp in FONT_CANDIDATES:
        if Path(fp).exists():
            try:
                font = ImageFont.truetype(fp, 88)
                small = ImageFont.truetype(fp, 40)
                mid = ImageFont.truetype(fp, 56)
                break
            except Exception:
                continue
    if font is None:
        die("找不到中文字体（msyh/simhei）——封面生成失败")
    brand = re.sub(r"[《》\s]", "", post.get("cover_text") or post["title_zhihu"])[:8] or "BLOG"
    d.text((72, 150), brand, font=font, fill="#ffffff")
    sub = re.sub(r"[《》]", "", post["title_zhihu"])[:22]
    d.text((72, 420), sub, font=mid, fill="#c8cdd8")
    d.text((72, 560), (post.get("cover_text") or "")[:24], font=small, fill="#6b7280")
    out = WF / f"cover_zhihu_{post['file'].stem}.png"
    img.save(out)
    return out


def zhihu_cover(tab: Tab, post: dict) -> bool:
    """在编辑页底部「发布设置」区上传封面（UploadPicture-input 已实测存在）。失败不致命。"""
    png = make_cover_zhihu(post)
    print(f"· 知乎封面已生成：{png.name}")
    try:
        found = tab.evaluate("""(() => {
          const f = document.querySelector('input.UploadPicture-input');
          if (!f) return false;
          f.id = '__tool_zhihu_cover';
          f.closest('.UploadPicture-wrapper')?.scrollIntoView({block: 'center'});
          return true;
        })()""")
        if not found:
            print("⚠ 未找到封面上传控件（input.UploadPicture-input）——手动在发布设置区传")
            return False
        doc = tab.call("DOM.getDocument")["root"]["nodeId"]
        node = tab.call("DOM.querySelector", nodeId=doc, selector="#__tool_zhihu_cover").get("nodeId")
        if not node:
            print("⚠ 封面 input 定位失败——手动传")
            return False
        tab.call("DOM.setFileInputFiles", files=[str(png.resolve())], nodeId=node)
        tab.evaluate("""(() => {
          const f = document.querySelector('#__tool_zhihu_cover');
          if (f) { f.dispatchEvent(new Event('input', {bubbles: true})); f.dispatchEvent(new Event('change', {bubbles: true})); }
        })()""")
        tab.pump(8)
        # 预览判定：占位文案消失即上传成功（知乎预览 DOM 类名不稳定，实测截图已验证）
        gone = tab.evaluate("""(() => {
          const w = document.querySelector('.UploadPicture-wrapper');
          return w ? !(w.innerText || '').includes('添加文章封面') : false;
        })()""")
        if gone:
            print("✓ 封面已上传（发布设置区可见预览）")
            return True
        print("⚠ 封面预览探针未见（探针不可靠，/edit 态常误报）——以浏览器实际显示为准；真缺再手动传")
        return False
    except Exception as e:
        print(f"⚠ 封面上传失败（{str(e)[:60]}）——手动传")
        return False


def zhihu_fill(tab: Tab, title: str, body_md: str) -> None:
    html = md_to_html(body_md)

    def js_quote(x: str) -> str:
        return json.dumps(x, ensure_ascii=False)

    wait_page(tab, "!!(document.querySelector('textarea') && document.querySelector('[contenteditable=\"true\"]'))",
              timeout=20, desc="知乎编辑器加载")

    ok = tab.evaluate(f"""
    (() => {{
      const ta = document.querySelector('textarea');
      if (!ta) return 'no-title';
      const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
      setter.call(ta, {js_quote(title)});
      ta.dispatchEvent(new Event('input', {{bubbles: true}}));
      return 'ok';
    }})()
    """)
    if ok != "ok":
        die("标题框未找到——知乎页面结构可能变了，手动填一下标题")

    r = tab.evaluate(f"""
    (() => {{
      const ed = document.querySelector('[contenteditable="true"]');
      if (!ed) return 'no-editor';
      ed.focus();
      // 防重贴：编辑器里若有旧内容先全选清空（复用标签页/重试场景）
      const s0 = window.getSelection();
      if ((ed.innerText || '').trim().length > 0) {{
        s0.selectAllChildren(ed);
        document.execCommand('delete');
      }}
      const sel = window.getSelection();
      sel.removeAllRanges();
      const range = document.createRange();
      range.selectNodeContents(ed);
      range.collapse(false);
      sel.addRange(range);
      const dt = new DataTransfer();
      dt.setData('text/html', {js_quote(html)});
      dt.setData('text/plain', {js_quote(body_md)});
      ed.dispatchEvent(new ClipboardEvent('paste', {{clipboardData: dt, bubbles: true, cancelable: true}}));
      return ed.innerText.length;
    }})()
    """)
    if r == "no-editor":
        die("正文编辑器未找到——知乎页面结构可能变了，手动粘贴正文")
    print(f"✓ 标题已填、正文已注入编辑器（当前正文约 {r} 字）")


def zhihu_auto_publish(tab: Tab) -> str | None:
    """点「发布」直达发布——知乎会记住此前的创作声明等设置，实测一键直发（2026-09-18）。
    若新环境弹出设置弹窗（要求选创作声明），降级提示人工补选。"""
    clicked = tab.evaluate("""(() => {
      const btns = [...document.querySelectorAll('button')]
        .filter(b => (b.innerText || '').trim() === '发布');
      if (!btns.length) return false;
      btns[btns.length - 1].click();       // 顶栏主按钮取最末一个
      return true;
    })()""")
    if not clicked:
        print("⚠ 没找到「发布」按钮——请手动点发布")
        return None
    for _ in range(20):                    # 等结果：跳转 /p/<id>（非 /edit）或出现「发布成功」
        tab.pump(1)
        try:
            href = str(tab.evaluate("location.href") or "")
            if "/p/" in href and "/edit" not in href:
                tab.evaluate("""(() => {   // 尽力关掉分享弹窗（失败不致命）
                  document.body.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape', keyCode: 27, bubbles: true}));
                  const x = document.querySelector('[class*=Modal] [class*=close], [aria-label*="关闭"]');
                  if (x) x.click();
                })()""")
                return href
            if tab.evaluate("((document.body.innerText||'').includes('发布成功'))"):
                tab.pump(2)
                return str(tab.evaluate("location.href") or "")
        except Exception:
            continue                       # 跳转/重渲染中求值会炸——发布进行中的正常现象，继续等
    modal = tab.evaluate("""(() => {       // 超时：可能弹了设置弹窗（新环境首次发布）
      const m = [...document.querySelectorAll('[class*=Modal],[class*=modal]')]
        .filter(e => e.offsetParent !== null && (e.innerText || '').length > 10);
      return m.length ? (m[m.length - 1].innerText || '').slice(0, 120) : '';
    })()""")
    if modal:
        print(f"⚠ 弹出了设置弹窗（{modal[:60]}…）——请在浏览器里补选创作声明后点确认")
    else:
        print("⚠ 等待发布结果超时——到浏览器窗口确认")
    return None


def cmd_zhihu(args) -> None:
    post = parse_post(Path(args.file))
    if not post["title_zhihu"]:
        die("frontmatter 缺 title_zhihu")
    try:
        ensure_browser()
        tab = open_tab(ZHIHU_WRITE, reuse_prefix="https://zhuanlan.zhihu.com")
        # 复用的标签页可能停在上一篇文章（/p/xxx）——强制回到写文章页
        if "/write" not in str(tab.evaluate("location.href") or ""):
            tab.navigate(ZHIHU_WRITE)
        wait_page(tab, "location.href.includes('/write')", timeout=30, desc="进入写文章页")
        if tab.evaluate("location.href.includes('signin') || location.href.includes('login')"):
            print("· 检测到知乎未登录——请在刚打开的浏览器窗口里登录，登录后自动继续（最长 5 分钟）")
            try:
                wait_page(tab, "location.href.includes('/write')", timeout=300, interval=3, desc="登录后回到编辑器")
            except SystemExit:
                die("等待登录超时")
        zhihu_fill(tab, post["title_zhihu"], post["body"])
        zhihu_cover(tab, post)          # 发布设置区自动传封面，失败不致命
        note = post.get("zhihu_note") or post["description"]
        print(f"· 建议创作导语（若发布弹窗有导语栏，粘贴这句）：{note[:60]}…")
        if getattr(args, "auto", False):
            url = zhihu_auto_publish(tab)
            if url:
                print(f"✓ 知乎已自动发布：{url}")
            return
        print("→ 核对专栏归属/话题/封面，然后手动点「发布」")
    except (RuntimeError, OSError) as e:
        print(f"⚠ CDP 通道不可用（{e}），退回剪贴板模式")
        zhihu_clipboard(post)


def zhihu_clipboard(post: dict) -> None:
    out = WF / f"zhihu_发布_{post['file'].stem}.md"
    content = f"# {post['title_zhihu']}\n\n{post['body']}"
    out.write_text(content, encoding="utf-8")
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             f"Get-Content -LiteralPath '{out}' -Raw -Encoding UTF8 | Set-Clipboard"],
            check=True, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        print("✓ 正文（知乎版标题 + 干净正文）已复制到剪贴板")
    except subprocess.CalledProcessError:
        print(f"⚠ 剪贴板写入失败，请手动打开：{out}")
    webbrowser.open(ZHIHU_WRITE)
    print(f"→ 在写文章页粘贴（Ctrl+V），标题用 {post['title_zhihu']!r}，核对后手动发布。原文件：{out}")


# -------------------------------------------------------------------- 封面

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyh.ttf",
    r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\simsun.ttc",
]


def make_cover(post: dict) -> Path:
    """生成 192×128 信息流封面（掘金建议尺寸）：深底 + 系列名 + 篇名截断。"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        die("缺 PIL——`uv add pillow` 后重试")
    w, h = 192, 128
    img = Image.new("RGB", (w, h), "#121217")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 6], fill="#2e6cff")
    font = None
    for fp in FONT_CANDIDATES:
        if Path(fp).exists():
            try:
                font = ImageFont.truetype(fp, 26)
                small = ImageFont.truetype(fp, 14)
                break
            except Exception:
                continue
    if font is None:
        die("找不到中文字体（msyh/simhei）——封面生成失败")
    brand_j = re.sub(r"[《》\s]", "", post.get("cover_text") or post["title_juejin"])[:6] or "JUEJIN"
    d.text((12, 26), brand_j, font=font, fill="#ffffff")
    sub = re.sub(r"[《》]", "", post["title_zhihu"])[:14]
    d.text((12, 84), sub, font=small, fill="#9aa0b0")
    out = WF / f"cover_{post['file'].stem}.png"
    img.save(out)
    return out


def upload_cover(post: dict, draft_id: str) -> bool:
    """生成封面并经编辑器上传到草稿（gen_token→TOS→Commit→草稿保存）。失败不致命。"""
    png = make_cover(post)
    print(f"· 封面已生成：{png.name}")
    try:
        ensure_browser()
        tab = open_tab(f"https://juejin.cn/editor/drafts/{draft_id}")
        tab.call("Network.enable")
        tab.pump(10)
        tab.evaluate("""(() => {
          const b = [...document.querySelectorAll('button')].find(x => (x.innerText || '').trim() === '发布');
          if (b) b.click();
        })()""")
        tab.pump(3)
        found = tab.evaluate("""(() => {
          // 封面 input 无 class，挂在 .coverselector_container 下（.file-input 是导入文章的，别碰）
          const f = [...document.querySelectorAll('input[type=file]')]
            .find(i => i.closest('.coverselector_container'));
          if (f) f.id = '__tool_cover_input';
          return !!f;
        })()""")
        doc = tab.call("DOM.getDocument")["root"]["nodeId"]
        node = (tab.call("DOM.querySelector", nodeId=doc, selector="#__tool_cover_input").get("nodeId")
                if found else None)
        if node:
            tab.call("DOM.setFileInputFiles", files=[str(png.resolve())], nodeId=node)
            # 裸 CDP 不派发事件，React 需要手动补 input/change（Puppeteer 同款做法）
            tab.evaluate("""(() => {
              const f = document.querySelector('#__tool_cover_input');
              if (f) {
                f.dispatchEvent(new Event('input', {bubbles: true}));
                f.dispatchEvent(new Event('change', {bubbles: true}));
              }
            })()""")
            print("· 上传中（gen_token → TOS → CommitImageUpload → 草稿保存）…")
            tab.pump(10)
            cover_url = tab.evaluate("""(() => {
              const img = document.querySelector('.coverselector_container .preview-box img');
              return img ? img.src.split('?')[0] : '';
            })()""")
            tab.close_page()
            if cover_url:
                print(f"✓ 封面已保存进草稿：…{cover_url[-40:]}")
                return True
        else:
            tab.close_page()
    except Exception as e:
        print(f"⚠ 封面上传失败（{str(e)[:60]}）——发布不带封面，可稍后 `cover <md>` 手动补")
    return False


def cmd_cover(args) -> None:
    """手动补封面：生成 192×128 并上传到草稿。"""
    post = parse_post(Path(args.file))
    meta = load_meta()
    draft_id = getattr(args, "draft", None) or meta.get(f"draft_{post['file'].stem}")
    if not draft_id:
        die("未找到草稿 ID——先跑 draft/publish，或用 --draft <id> 指定")
    if not upload_cover(post, draft_id):
        print("⚠ 未检测到封面预览——到掘金后台草稿确认，失败就手动传")


# ------------------------------------------------------------------ 子命令

def url_guard(post: dict) -> None:
    """掘金机审会把招聘平台 URL/域名字符串按「推广类·招聘」驳回（辩一实测教训）。"""
    hits = re.findall(r"https?://\S+|[\w-]+\.(?:com|cn|net|org|io)\b", post["body"])
    if hits:
        print(f"⚠ 正文含 {len(hits)} 处 URL/域名字符串（掘金机审可能按推广类驳回），前几个：")
        for h in hits[:5]:
            print(f"    {h}")
        print("  建议降为纯文字描述（如「BOSS 直聘搜 XXX 可复核」）——publish 不会因此中断")


RECRUIT_WORDS = re.compile(r"高薪|猎头|招聘|求职|在招|招人")


def audit_guard(post: dict) -> None:
    """推广类驳回预警（真实账号实测）：招聘语汇撞上钱数就高危，标题里的「高薪」必雷。"""
    risky = []
    for seg in [post["title_juejin"], *post["body"].splitlines()]:
        for m in RECRUIT_WORDS.finditer(seg):
            ctx = seg[max(0, m.start() - 20):m.end() + 20]
            if m.group(0) in ("高薪", "猎头") or re.search(r"\d", ctx):
                risky.append(ctx.strip()[:50])
    if risky:
        print(f"⚠ 招聘语汇×钱数组合 {len(risky)} 处（推广类驳回高发区），建议改写：")
        for r in risky[:5]:
            print(f"    …{r}…")
        print("  改法参考：高薪招→真金白银请、招聘预算→预算、求职者→看机会的读者——不中断")


def cmd_preview(args) -> None:
    post = parse_post(Path(args.file))
    brief, warns = check_brief(post["description"])
    n_chars = len(re.sub(r"\s", "", post["body"]))
    print(f"《{post['title_juejin']}》（掘金）｜《{post['title_zhihu']}》（知乎）")
    print(f"正文：{n_chars} 字（不含空白）｜摘要：{len(brief)} 字｜分类：{post['category_id']}")
    names = []
    for name in post["tags"]:
        t = TAG_FALLBACK.get(name, name)
        names.append(f"{name}→{t}" if t != name else name)
    print(f"标签：{('、'.join(names)) or '（未配）'}（掘金上限 2 个）")
    if re.search(r"<!--", post["body"]):
        die("剥离后正文仍含 HTML 注释——请检查")
    if "<!--" in Path(args.file).read_text(encoding="utf-8"):
        print("✓ 检测到内部 checklist，已剥离（不会发布）")
    for w in warns:
        print(f"⚠ {w}")
    print("✓ 校验通过")


def cmd_tags(args) -> None:
    cookie = load_cookie()
    found = search_tags(args.keyword, cookie)
    if not found:
        die(f"「{args.keyword}」无结果——换个关键词（掘金标签库有限，如 职业发展 不存在）")
    cache = load_tag_cache()
    for f in found:
        print(f"  {f['title']}  {f['id']}")
    cache.setdefault(args.keyword, found[0]["id"])
    save_tag_cache(cache)
    print(f"✓ 默认取第一条，已记入缓存 {TAG_CACHE.relative_to(ROOT)}")


def cmd_columns(args) -> None:
    cookie = load_cookie()
    meta = load_meta()
    uid = meta.get("user_id")
    if not uid:
        u = api(USER_URL, None, cookie).get("data") or {}
        uid = str(u.get("user_id") or "")
        if uid:
            meta["user_id"] = uid
            save_meta(meta)
    if not uid:
        die("拿不到 user_id——先跑 whoami")
    r = api("/content_api/v1/column/self_center_list",
            {"user_id": uid, "cursor": "0", "keyword": "", "limit": 20}, cookie)
    data = r.get("data")
    items = data if isinstance(data, list) else (data or {}).get("data") or []
    if not items:
        print("（还没有专栏——`column-new <标题>` 直接建一个，一次即可）")
    for it in items:
        c, v = it.get("column") or {}, it.get("column_version") or {}
        mark = " ←当前默认" if c.get("column_id") == meta.get("column_id") else ""
        print(f"  {c.get('column_id')}  {v.get('title')}（{c.get('article_cnt', 0)} 篇）{mark}")
    if getattr(args, "use", None):
        meta = load_meta()
        meta["column_id"] = args.use
        save_meta(meta)
        print(f"✓ 默认专栏已切换为 {args.use}")
    elif not meta.get("column_id") and items:
        print("→ 用 `columns --use <id>` 设为发布默认专栏（不设则发布不挂专栏）")


COLUMN_MGMT_URL = "https://juejin.cn/creator/content/column?status=all"


def fetch_columns(cookie: str, uid: str) -> list[dict]:
    r = api("/content_api/v1/column/self_center_list",
            {"user_id": uid, "cursor": "0", "keyword": "", "limit": 20}, cookie)
    data = r.get("data")
    return data if isinstance(data, list) else (data or {}).get("data") or []


def cmd_column_new(args) -> None:
    """新建专栏（纯 API）：column/publish 不带 column_id = 创建，data 返回新 id。"""
    cookie = load_cookie()
    intro = getattr(args, "intro", None) or "新专栏，简介待补充。"
    r = api("/content_api/v1/column/publish",
            {"title": args.title, "content": intro, "cover": ""}, cookie)
    if r.get("err_no") != 0:
        die(f"建专栏失败：[{r.get('err_no')}] {r.get('err_msg')}")
    cid = str(r.get("data") or "")
    if not cid.isdigit():
        die(f"建专栏返回异常：{json.dumps(r, ensure_ascii=False)[:200]}")
    print(f"✓ 专栏已创建：{args.title}")
    print(f"  column_id = {cid}")
    print(f"  专栏页：https://juejin.cn/column/{cid}")
    if getattr(args, "use", False):
        meta = load_meta(); meta["column_id"] = cid; save_meta(meta)
        print("✓ 已设为默认专栏（后续 publish 自动挂载）")
    print(f"→ 补封面：uv run publish.py column-cover --column {cid}")


def make_cover_column(title: str, subtitle: str = "") -> Path:
    """专栏封面：1280×720（16:9；专栏头图源图实测 1920×1080 同比）。"""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        die("缺 PIL——`uv add pillow` 后重试")
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), "#121217")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 20], fill="#2e6cff")
    font = mid = small = None
    for fp in FONT_CANDIDATES:
        if Path(fp).exists():
            try:
                font = ImageFont.truetype(fp, 96)
                mid = ImageFont.truetype(fp, 52)
                small = ImageFont.truetype(fp, 32)
                break
            except Exception:
                continue
    if font is None:
        die("找不到中文字体（msyh/simhei）——封面生成失败")
    name = re.sub(r"[《》\s]", "", title)
    d.text((80, 200), name[:10], font=font, fill="#ffffff")
    if subtitle:
        d.text((80, 420), subtitle[:26], font=mid, fill="#c8cdd8")
    d.text((80, 620), f"{name[:16]} · 专栏", font=small, fill="#6b7280")
    out = WF / f"cover_column_{name[:12]}.png"
    img.save(out)
    return out


VISIBLE_MODAL_JS = ("[...document.querySelectorAll('.create-column-modal')]"
                    ".find(e => e.offsetParent !== null)")


def cmd_column_cover(args) -> None:
    """专栏封面：PIL 生成 16:9 → CDP 驱动「修改介绍」弹窗上传 → 确认保存。"""
    meta = load_meta()
    cookie = load_cookie()
    cid = getattr(args, "column", None) or meta.get("column_id")
    if not cid:
        die("未指定专栏——先 `columns --use <id>` 设默认，或传 --column <id>")
    uid = meta.get("user_id")
    if not uid:
        u = api(USER_URL, None, cookie).get("data") or {}
        uid = str(u.get("user_id") or "")
        if uid:
            meta["user_id"] = uid
            save_meta(meta)
    if not uid:
        die("拿不到 user_id——先跑 whoami")
    col = next((it for it in fetch_columns(cookie, uid)
                if str((it.get("column") or {}).get("column_id")) == str(cid)), None)
    if not col:
        die(f"专栏 {cid} 不在你的专栏列表里——`columns` 核对")
    title = str((col.get("column_version") or {}).get("title") or "")
    old_cover = str((col.get("column_version") or {}).get("cover") or "")
    if not title:
        die(f"专栏 {cid} 拿不到标题——创作者中心核对")
    png = make_cover_column(title, getattr(args, "subtitle", None) or "")
    print(f"· 封面已生成：{png.name}")
    ensure_browser()
    tab = open_tab(COLUMN_MGMT_URL, reuse_prefix="https://juejin.cn/creator/content/column")
    try:
        tab.call("Network.enable")
        if "creator/content/column" not in str(tab.evaluate("location.href") or ""):
            tab.navigate(COLUMN_MGMT_URL)
        wait_page(tab, "document.readyState === 'complete'", timeout=30, desc="专栏管理页加载")
        tab.pump(5)
        # 逐个试「修改介绍」：以弹窗里的名称输入框对上目标为准（顺序不可靠）
        n = tab.evaluate("""(() => {
          window.__colEdits = [...document.querySelectorAll('[class*="byte-dropdown-item"]')]
            .filter(e => (e.innerText || '').includes('修改介绍'));
          return window.__colEdits.length;
        })()""")
        opened = False
        for i in range(int(n or 0)):
            tab.evaluate(f"window.__colEdits[{i}] && window.__colEdits[{i}].click()")
            tab.pump(3)
            val = tab.evaluate(f"""(() => {{
              const dlg = {VISIBLE_MODAL_JS};
              const inp = dlg && dlg.querySelector('input:not([type=file])');
              return inp ? inp.value : '';
            }})()""")
            if val == title:
                opened = True
                print(f"· 已打开「{title}」编辑弹窗")
                break
            # 不是目标专栏——取消换下一个
            tab.evaluate(f"""(() => {{
              const dlg = {VISIBLE_MODAL_JS};
              const c = dlg && [...dlg.querySelectorAll('button')]
                .find(b => (b.innerText || '').trim() === '取消');
              if (c) c.click();
            }})()""")
            tab.pump(2)
        if not opened:
            die(f"没找到「{title}」的编辑弹窗（页面上共 {n or 0} 个入口）")
        found = tab.evaluate(f"""(() => {{
          const dlg = {VISIBLE_MODAL_JS};
          const f = dlg && dlg.querySelector('.img-uploader input[type=file]');
          if (f) f.id = '__tool_col_cover';
          return !!f;
        }})()""")
        if not found:
            die("没找到封面上传 input——弹窗结构可能变了")
        doc = tab.call("DOM.getDocument")["root"]["nodeId"]
        node = tab.call("DOM.querySelector", nodeId=doc, selector="#__tool_col_cover").get("nodeId")
        if not node:
            die("封面 input 定位失败")
        tab.call("DOM.setFileInputFiles", files=[str(png.resolve())], nodeId=node)
        tab.evaluate("""(() => {
          const f = document.querySelector('#__tool_col_cover');
          if (f) {
            f.dispatchEvent(new Event('input', {bubbles: true}));
            f.dispatchEvent(new Event('change', {bubbles: true}));
          }
        })()""")
        print("· 上传中（gen_token → TOS → 页面内完成）…")
        tab.pump(10)
        prev = tab.evaluate(f"""(() => {{
          const dlg = {VISIBLE_MODAL_JS};
          const img = dlg && dlg.querySelector('.img-uploader img');
          return img ? (img.src || '').split('?')[0].slice(-40) : '';
        }})()""")
        if prev:
            print(f"✓ 封面预览可见：…{prev}")
        else:
            print("⚠ 未见封面预览——仍尝试保存，稍后到后台核对")
        tab.evaluate(f"""(() => {{
          const dlg = {VISIBLE_MODAL_JS};
          const b = dlg && [...dlg.querySelectorAll('button')]
            .find(x => (x.innerText || '').trim() === '确认');
          if (b) b.click();
        }})()""")
        tab.pump(8)
        tab.evaluate(f"""(() => !{VISIBLE_MODAL_JS})()""")   # 弹窗状态仅参考，成功与否看下面 API
    finally:
        tab.close_page()
    # 以 API 为准：version.cover 变了就是成功（弹窗关闭状态有滞后、实测会误判）
    new_cover = old_cover
    for _ in range(6):
        time.sleep(3)
        new_cover = next((str((it.get("column_version") or {}).get("cover") or "")
                          for it in fetch_columns(cookie, uid)
                          if str((it.get("column") or {}).get("column_id")) == str(cid)), "")
        if new_cover and new_cover != old_cover:
            break
    if new_cover and new_cover != old_cover:
        print(f"✓ 专栏封面已保存（version.cover 已更新，{cid}）")
        print(f"→ 核对：https://juejin.cn/column/{cid}")
    else:
        print("⚠ 封面字段未见变化——到创作者中心「专栏管理」核对")


def cmd_draft(args) -> None:
    post = parse_post(Path(args.file))
    brief, _ = check_brief(post["description"])
    cookie = load_cookie()
    print("· 解析标签…")
    tag_ids = resolve_tag_ids(post, cookie)
    print(f"· 标签：{tag_ids}")
    time.sleep(CALL_GAP_SECONDS)
    print("· 建草稿…")
    draft_id = create_draft(post, brief, tag_ids, cookie)
    meta = load_meta()
    meta[f"draft_{post['file'].stem}"] = draft_id
    save_meta(meta)
    print(f"✓ 草稿已建：draft_id={draft_id}（已记入 meta）")
    if not post["cover_image"]:
        upload_cover(post, draft_id)
    print(f"→ 掘金后台「草稿箱」核对排版后手动发布：https://juejin.cn/editor/drafts/{draft_id}")
    print("  或直接：uv run publish.py publish <同一文件>  重新建稿并自动发布")


def cmd_publish(args) -> None:
    post = parse_post(Path(args.file))
    brief, _ = check_brief(post["description"])
    url_guard(post)
    audit_guard(post)
    cookie = load_cookie()
    tag_ids = resolve_tag_ids(post, cookie, interactive=True)
    print(f"· 标签：{tag_ids}")
    time.sleep(CALL_GAP_SECONDS)
    draft_id = create_draft(post, brief, tag_ids, cookie)
    meta = load_meta()
    meta[f"draft_{post['file'].stem}"] = draft_id
    save_meta(meta)
    if not post["cover_image"] and not getattr(args, "no_cover", False):
        upload_cover(post, draft_id)          # PIL 生成 + CDP 上传，失败不阻塞
    word_count = len(re.sub(r"\s", "", post["body"]))
    column_id = None if getattr(args, "no_column", False) else column_id_from_meta()
    if column_id:
        print(f"· 收录专栏：{column_id}")
    else:
        print("· 未配置专栏（columns --use <id> 可设置），本次不挂专栏")
    time.sleep(CALL_GAP_SECONDS)
    print(f"· 发布…（草稿 {draft_id}）")
    publish_draft(draft_id, cookie, word_count, column_id)


def cmd_html(args) -> None:
    post = parse_post(Path(args.file))
    out = WF / f"zhihu_html_{post['file'].stem}.html"
    out.write_text("<meta charset='utf-8'>" + md_to_html(post["body"]), encoding="utf-8")
    print(f"✓ {out}（浏览器打开即可预览知乎粘贴的富文本效果）")


def main() -> None:
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="juejin-publisher（掘金 API 全自动 + 知乎 CDP 半自动）")
    sub = p.add_subparsers(dest="cmd", required=True)

    specs = (
        ("login", cmd_login, "浏览器扫码：掘金抓 Cookie + 知乎顺手登录", None, ()),
        ("whoami", cmd_whoami, "校验 Cookie 并显示当前账号", None, ()),
        ("status", cmd_status, "查文章审核状态（0=审核中，1/2=已上线）", "article_id", ()),
        ("cleanup", cmd_cleanup, "关闭 CDP 浏览器堆积的标签（防卡死；--all 连知乎写作页一起清）", None, ("--all",)),
        ("preview", cmd_preview, "离线校验（不发任何请求）", "file", ()),
        ("tags", cmd_tags, "搜索掘金标签 ID", "keyword", ()),
        ("columns", cmd_columns, "列出我的专栏；--use <id> 设为默认", None, ("--use",)),
        ("column-new", cmd_column_new, "新建专栏（纯 API）", "title", ("--intro", "--use")),
        ("column-cover", cmd_column_cover, "给专栏生成 16:9 封面并上传（CDP）", None, ("--column", "--subtitle")),
        ("draft", cmd_draft, "建掘金草稿（分类+双标签+摘要）", "file", ()),
        ("publish", cmd_publish, "全自动发布（含挂专栏与封面）", "file", ("--no-column", "--no-cover")),
        ("cover", cmd_cover, "生成 192×128 封面并上传到草稿", "file", ("--draft",)),
        ("zhihu", cmd_zhihu, "CDP：知乎填标题正文封面；--auto 自动点发布", "file", ("--auto",)),
        ("html", cmd_html, "调试：预览知乎粘贴用 HTML", "file", ()),
    )
    for name, fn, help_, arg, flags in specs:
        sp = sub.add_parser(name, help=help_)
        if arg:
            sp.add_argument(arg, help={"file": "posts 下的 md 文件", "title": "专栏标题",
                                       "keyword": "标签关键词", "article_id": "文章 ID"}[arg])
        for fl in flags:
            if fl == "--use":
                sp.add_argument("--use", help="设为默认专栏的 column_id")
            elif fl == "--no-column":
                sp.add_argument("--no-column", action="store_true", help="本次发布不挂专栏")
            elif fl == "--draft":
                sp.add_argument("--draft", help="指定草稿 ID（默认取 meta 里记的）")
            elif fl == "--no-cover":
                sp.add_argument("--no-cover", action="store_true", help="跳过自动封面")
            elif fl == "--all":
                sp.add_argument("--all", action="store_true", help="连知乎写作页一起清")
            elif fl == "--intro":
                sp.add_argument("--intro", help="专栏简介（默认占位文案）")
            elif fl == "--column":
                sp.add_argument("--column", help="专栏 ID（默认取 meta 里的默认专栏）")
            elif fl == "--subtitle":
                sp.add_argument("--subtitle", help="封面副标题文案")
            elif fl == "--auto":
                sp.add_argument("--auto", action="store_true",
                                help="知乎全自动：填完直接点发布（创作声明沿用上次设置）")
        sp.set_defaults(func=fn)

    args = p.parse_args()
    if getattr(args, "file", None) and not Path(args.file).is_absolute():
        cand = POSTS / args.file
        args.file = str(cand if cand.exists() else args.file)
    args.func(args)


if __name__ == "__main__":
    main()
