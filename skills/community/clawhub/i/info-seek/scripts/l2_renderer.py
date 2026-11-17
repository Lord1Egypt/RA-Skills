#!/usr/bin/env python3
"""
scripts/l2_renderer.py — L2 多引擎渲染抽象层（v1.5.0 · 功能层 · S6 探测收口）

把 infoseek 的 L2 抓取（浏览器渲染）从"单 playwright 依赖"升级为
"多引擎注册表 + 场景路由 + 健康状态机 + 故障 cross-over"：

    Camoufox（主）  → 引擎层反指纹，Cloudflare/Turnstile 穿透最强
    Obscura（批量）  → Rust 轻量（30MB/85ms），高并发批量抓取
    Patchright       → Playwright 补丁，一行替换快速加固
    Chromium（兜底）  → 原生 playwright，生态最成熟
    L1 静态           → 全引擎失败时由调用方兜底（本模块返回空串）

设计对齐 infoseek 架构：
  - 声明式引擎注册表（对齐 capabilities/registry.yaml 哲学）
  - 健康状态机复用 engine_lifecycle（record_success/failure/is_disabled）
  - 引擎探测懒加载：包/二进制缺失自动跳过（probe=False），行为零侵入
  - 场景路由：default(反爬) / batch(批量) / last(兜底) 三场景排序
  - 向后兼容：引擎全不可用时返回 ""，调用方照旧降级 L1

用法:
    from l2_renderer import render_html, render_html_batch, engine_status
    html = render_html("https://example.com")        # 默认场景
    html = render_html(url, prefer="batch")          # 批量场景优先
    results = render_html_batch(urls, concurrency=5) # 并行批量
    print(engine_status())                            # 各引擎健康/可用状态

CLI:
    python scripts/l2_renderer.py --status           # 引擎可用性探测
    python scripts/l2_renderer.py --render URL       # 单 URL 渲染测试
"""

from __future__ import annotations

import os
import socket
import sys
import time
from pathlib import Path
from typing import Callable, Dict, List, Optional

# 日志（对齐 infoseek：禁 print 用 logging）
import logging
log = logging.getLogger("infoseek.l2_renderer")


# ═══════════════════════════════════════════════════════════════
# 常量与引擎注册表
# ═══════════════════════════════════════════════════════════════

DEFAULT_TIMEOUT = float(os.environ.get("INFOSEEK_L2_TIMEOUT", "15"))
OBSCURA_PORT = int(os.environ.get("OBSCURA_PORT", "9222"))
BATCH_CONCURRENCY = int(os.environ.get("INFOSEEK_L2_CONCURRENCY", "5"))
# stealth 反检测注入（实测 sannysoft 0 FAIL；缺失/失败自动降级裸奔）
STEALTH_ENABLED = os.environ.get("INFOSEEK_L2_STEALTH", "1") == "1"
# L1 正文长度阈值（低于则判定需渲染）
RENDER_TRIGGER_LEN = int(os.environ.get("INFOSEEK_L2_TRIGGER_LEN", "100"))

# 场景标签
SCENE_DEFAULT = "default"   # 反爬兜底：Camoufox 优先
SCENE_BATCH = "batch"       # 批量并行：Obscura 优先
SCENE_LAST = "last"         # 终极兜底


# ── S6：dep_registry 事实层惰性 accessor（收口浏览器探测原语，零漂移）──
# 统一以顶层名 dep_registry 导入（scripts 把 core/ 注入 sys.path）；
# dep_registry 加载时已做 sys.modules 双登记，顶层名 ↔ core.dep_registry 合一。
_dr = None


def _dep_reg():
    global _dr
    if _dr is None:
        _cand = Path(__file__).resolve().parent.parent / "core"
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        import dep_registry as _mod  # 顶层名
        _dr = _mod
    return _dr


def _tcp_probe(port: int, host: str = "127.0.0.1", timeout: float = 1.5) -> bool:
    """TCP 端口连通探测（Obscura CDP 端口）。"""
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        s.close()
        return True
    except Exception:
        return False


# ── 引擎探测（懒加载，缺失自动跳过）──

def _probe_camoufox() -> bool:
    # S6 收口：import + official 目录非空（probe_mode=all），事实原语走 dep_registry
    dr = _dep_reg()
    if not dr.has_module("camoufox"):
        return False
    # 浏览器二进制必须真实存在（fetch 后落 ~/.cache/camoufox/browsers/official/<ver>/）
    # 注意：pip CLI(camoufox) 存在≠浏览器已装，禁止用 which 兜底（误判 P5）
    return dr.probe_token("path:~/.cache/camoufox/browsers/official") and _camoufox_dir_nonempty()


def _camoufox_dir_nonempty() -> bool:
    base = Path.home().joinpath(".cache/camoufox/browsers/official")
    try:
        return base.is_dir() and any(base.iterdir())
    except Exception:
        return False


def _probe_obscura() -> bool:
    # which 走 dep_registry；运行期 CDP 端口探测（registry 未含）保留在消费层
    if _dep_reg().which_path("obscura"):
        return True
    return _tcp_probe(OBSCURA_PORT)  # CDP 服务已在跑


def _probe_patchright() -> bool:
    dr = _dep_reg()
    if not dr.has_module("patchright"):
        return False
    # patchright 价值=自家源码级反检测补丁浏览器（install 后落 ms-playwright 缓存）。
    # 复用系统 chromium 时 patchright 退化为裸奔（无 stealth），probe=False 让位 chromium 引擎
    # （2026-09-06 实测：patchright+系统chromium 于 sannysoft 检出 WebDriver，与裸奔一致）
    return _has_playwright_browser()


def _find_system_chromium() -> Optional[str]:
    """探测可用 chromium 二进制：CHROMIUM_PATH env → which → Debian/Ubuntu 默认路径。

    S6：env/which 事实原语走 dep_registry；路径返回（供 _launch_opts 消费）保留本层。
    """
    dr = _dep_reg()
    if dr.probe_token("env:CHROMIUM_PATH"):
        cand = os.environ.get("CHROMIUM_PATH", "").strip()
        if cand and os.path.isfile(cand):
            return cand
    for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
        p = dr.which_path(name)
        if p:
            return p
    for p in ("/usr/lib/chromium/chromium", "/usr/bin/chromium",
              "/opt/google/chrome/chrome",
              "/usr/lib/chromium-browser/chromium-browser"):
        if os.path.isfile(p):
            return p
    return None


def _has_playwright_browser() -> bool:
    """playwright 自家缓存（~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome）。"""
    base = Path.home().joinpath(".cache/ms-playwright")
    if not base.is_dir():
        return False
    try:
        return any(base.glob("chromium-*/chrome-linux*/chrome")) or any(
            base.glob("chromium-*/chrome-linux64/chrome"))
    except Exception:
        return False


def _probe_chromium() -> bool:
    # playwright 可 import 的事实走 dep_registry；浏览器（系统路径/缓存）组合保留本层
    if not _dep_reg().has_module("playwright.sync_api"):
        return False
    return bool(_find_system_chromium()) or _has_playwright_browser()



# ── 引擎渲染实现（各自 try/except，失败抛异常由路由层记录）──

def _render_camoufox(url: str, timeout: float = DEFAULT_TIMEOUT) -> str:
    # camoufox >= 0.5: Camoufox 上下文管理器（自动 launch/close），0.4 的 sync_launch 已废弃
    from camoufox.sync_api import Camoufox
    with Camoufox(headless=True) as browser:
        page = browser.new_page()
        page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
        page.wait_for_timeout(1200)
        return page.content()


def _render_obscura(url: str, timeout: float = DEFAULT_TIMEOUT) -> str:
    """Obscura CDP 直连（playwright-core connectOverCDP，无需 chromium 下载）。"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{OBSCURA_PORT}")
            try:
                page = browser.new_page()
                page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
                page.wait_for_timeout(1000)
                return page.content()
            finally:
                browser.close()
    except Exception:
        # 兜底：obscura CLI 启动临时实例
        import subprocess
        proc = subprocess.Popen(
            [_dep_reg().which_path("obscura"), "serve", "--port", str(OBSCURA_PORT), "--stealth"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            time.sleep(2.0)
            return _render_obscura(url, timeout)  # 递归重试
        finally:
            proc.terminate()


def _render_patchright(url: str, timeout: float = DEFAULT_TIMEOUT) -> str:
    # 自家补丁浏览器已由 probe 保证存在 → 不注入 executable_path，走补丁浏览器（自带反检测）
    from patchright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        try:
            page = browser.new_page()
            page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
            page.wait_for_timeout(1200)
            return page.content()
        finally:
            browser.close()


def _launch_opts() -> Dict[str, str]:
    """launch 附加参数：优先系统 chromium（apt 安装）；root 沙箱需 --no-sandbox。"""
    opts: Dict[str, str] = {"args": ["--no-sandbox"]}
    exe = _find_system_chromium()
    if exe:
        opts["executable_path"] = exe
    return opts


def _apply_stealth(page) -> None:
    """注入 playwright-stealth 反检测（隐藏 webdriver/UA/WebGL/视口特征）。

    2026-09-06 实测：bot.sannysoft.com 裸 chromium 4 项 FAIL → stealth 注入后 0 FAIL。
    依赖缺失/注入失败静默降级裸奔（零侵入，不中断渲染）。
    """
    if not STEALTH_ENABLED:
        return
    try:
        from playwright_stealth import Stealth
        Stealth().apply_stealth_sync(page)
    except Exception:
        log.debug("[l2_renderer] stealth 注入不可用，降级裸奔")



def _stealth_ctx():
    """stealth hook 上下文管理器：可用返回 use_sync 包装，不可用返回原 ctx（降级裸奔）。"""
    if not STEALTH_ENABLED:
        return None
    try:
        from playwright_stealth import Stealth
        return Stealth()
    except Exception:
        return None


def _render_chromium(url: str, timeout: float = DEFAULT_TIMEOUT) -> str:
    from playwright.sync_api import sync_playwright
    stealth = _stealth_ctx()
    cm = stealth.use_sync(sync_playwright()) if stealth else sync_playwright()
    with cm as p:
        browser = p.chromium.launch(headless=True, **_launch_opts())
        try:
            page = browser.new_page()
            page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
            page.wait_for_timeout(1200)
            return page.content()
        finally:
            browser.close()


# 引擎注册表（声明式；probe 失败 = 自动跳过）
RENDER_ENGINES: Dict[str, Dict] = {
    "camoufox": {
        "probe": _probe_camoufox, "render": _render_camoufox,
        "scene": SCENE_DEFAULT, "priority": 1, "weight": 1.0,
        "desc": "反指纹 Firefox 主引擎",
    },
    "obscura": {
        "probe": _probe_obscura, "render": _render_obscura,
        "scene": SCENE_BATCH, "priority": 1, "weight": 0.9,
        "desc": "Rust 轻量批量引擎（30MB）",
    },
    "patchright": {
        "probe": _probe_patchright, "render": _render_patchright,
        "scene": SCENE_DEFAULT, "priority": 2, "weight": 0.7,
        "desc": "Playwright 反检测补丁",
    },
    "chromium": {
        "probe": _probe_chromium, "render": _render_chromium,
        "scene": SCENE_LAST, "priority": 1, "weight": 0.6,
        "desc": "原生 playwright 兜底",
    },
}

# 场景 → 引擎执行顺序
_SCENE_ORDER = {
    SCENE_DEFAULT: ["camoufox", "patchright", "chromium", "obscura"],
    SCENE_BATCH: ["obscura", "camoufox", "chromium", "patchright"],
    SCENE_LAST: ["chromium", "patchright", "camoufox", "obscura"],
}


# ═══════════════════════════════════════════════════════════════
# 健康状态机（复用 engine_lifecycle，缺失时本地降级）
# ═══════════════════════════════════════════════════════════════

def _lifecycle():
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from engine_lifecycle import get_lifecycle
        return get_lifecycle()
    except Exception:
        return None


def _is_disabled(name: str) -> bool:
    lc = _lifecycle()
    if lc is None:
        return False
    try:
        return lc.is_disabled(f"L2-{name}")
    except Exception:
        return False


def _record(name: str, ok: bool, err: Optional[Exception] = None) -> None:
    lc = _lifecycle()
    if lc is None:
        return
    try:
        if ok:
            lc.record_success(f"L2-{name}")
        else:
            lc.record_failure(f"L2-{name}", err)
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════
# 核心路由
# ═══════════════════════════════════════════════════════════════

def _engine_available(name: str) -> bool:
    if _is_disabled(name):
        return False
    eng = RENDER_ENGINES.get(name)
    if not eng:
        return False
    try:
        return bool(eng["probe"]())
    except Exception:
        return False


def render_html(url: str, timeout: float = DEFAULT_TIMEOUT,
                prefer: str = SCENE_DEFAULT) -> str:
    """L2 渲染统一入口：场景路由 → 健康过滤 → 故障 cross-over。

    - prefer: default(反爬优先) / batch(批量优先) / last(纯兜底)
    - 引擎全失败 → 返回 ""（调用方照旧降级 L1，行为零回归）
    """
    order = _SCENE_ORDER.get(prefer, _SCENE_ORDER[SCENE_DEFAULT])
    for name in order:
        if not _engine_available(name):
            log.debug(f"[l2_renderer] 跳过 {name}（不可用/熔断）")
            continue
        eng = RENDER_ENGINES[name]
        log.debug(f"[l2_renderer] 尝试 {name}（{eng['desc']}）")
        try:
            html = eng["render"](url, timeout)
        except Exception as e:
            _record(name, False, e)
            log.warning(f"[l2_renderer] {name} 渲染失败: {e}")
            continue
        if html:
            _record(name, True)
            return html
        _record(name, False)
    log.warning(f"[l2_renderer] 全部引擎失败，降级 L1 静态: {url[:80]}")
    return ""


def render_html_batch(urls: List[str], concurrency: int = BATCH_CONCURRENCY,
                      timeout: float = DEFAULT_TIMEOUT) -> List[Dict]:
    """批量渲染（Obscura 并行场景；线程池模拟，无额外重依赖）。"""
    out: List[Dict] = []
    if not urls:
        return out
    # 批量 → 优先走 batch 场景单引擎（避免每 URL 全链探测）
    names = _SCENE_ORDER[SCENE_BATCH]
    engine_name = next((n for n in names if _engine_available(n)), None)
    if engine_name is None:
        return [{"url": u, "html": "", "engine": None} for u in urls]

    import concurrent.futures as cf
    eng = RENDER_ENGINES[engine_name]
    with cf.ThreadPoolExecutor(max_workers=min(concurrency, len(urls))) as ex:
        fut = {ex.submit(eng["render"], u, timeout): u for u in urls}
        for f in cf.as_completed(fut):
            u = fut[f]
            try:
                html = f.result()
                out.append({"url": u, "html": html or "", "engine": engine_name})
            except Exception as e:
                _record(engine_name, False, e)
                out.append({"url": u, "html": "", "engine": engine_name, "error": str(e)[:120]})
    _record(engine_name, True)
    return out


def engine_status() -> Dict:
    """各引擎可用性 + 健康状态（探测结果）。"""
    return {
        name: {"available": _engine_available(name),
               "desc": eng["desc"],
               "scene": eng["scene"],
               "priority": eng["priority"]}
        for name, eng in RENDER_ENGINES.items()
    }


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="L2 多引擎渲染抽象层")
    ap.add_argument("--status", action="store_true", help="引擎可用性探测")
    ap.add_argument("--render", metavar="URL", help="渲染单 URL 测试")
    ap.add_argument("--scene", default=SCENE_DEFAULT,
                    choices=[SCENE_DEFAULT, SCENE_BATCH, SCENE_LAST], help="场景")
    args = ap.parse_args()

    if args.status:
        import json
        print(json.dumps(engine_status(), ensure_ascii=False, indent=2))
        return 0
    if args.render:
        html = render_html(args.render, prefer=args.scene)
        print(f"渲染结果: {len(html)} 字符 (scene={args.scene})")
        print(html[:300] if html else "(空 → 已降级 L1)")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
