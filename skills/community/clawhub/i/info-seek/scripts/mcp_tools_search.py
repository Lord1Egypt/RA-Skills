#!/usr/bin/env python3
"""mcp_tools_search.py — Infoseek MCP 搜索/抓取工具（G11 拆分 v1.0.1）"""
import sys
import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp_tools_common import INFOSEEK_ROOT

# ── S7：dep_registry 事实层惰性 accessor（playwright/whisper 可选点零漂移收口）──
_dr = None


def _dep_reg():
    global _dr
    if _dr is None:
        _core = str(Path(__file__).resolve().parent.parent / "core")
        if _core not in sys.path:
            sys.path.insert(0, _core)
        import dep_registry as _mod
        _dr = _mod
    return _dr


# ══ 以下函数由 G11 拆分脚本从 infoseek_mcp_server.py 提取（v1.0.1）══

def tool_search_anchors(args: Dict) -> Dict:
    """锚点发现（v1.0.1 PATCH: 接入 pipeline.search_web 真实搜索链）

    此前为壳实现（仅返回提示文案），现调用 infoseek_pipeline.search_web
    执行 DDG/Bing/Jina/Wikipedia 多引擎并行搜索，并对结果做主题相关性过滤。
    """
    subject = args['subject']
    depth = args.get('depth', 2)
    max_results = args.get('max_results', 8)

    try:
        _anchors_key = f"anchors:{subject}:{depth}:{max_results}"
        _anchors_hit = _cache_try_get(_anchors_key)
        if _anchors_hit and _anchors_hit.get("content"):
            try:
                _cached = json.loads(_anchors_hit["content"])
                if isinstance(_cached, dict) and _cached.get("status") == "ok" and "anchors" in _cached:
                    return _cached
            except Exception:
                pass
        from infoseek_pipeline import search_web
        results = search_web(subject, max_results=max_results)
        anchors = []
        for r in results:
            anchors.append({
                'title': r.get('title', ''),
                'url': r.get('url', ''),
                'engine': r.get('engine', ''),
                'snippet': r.get('snippet', ''),
            })
        _anchors_result = {
            "subject": subject,
            "depth": depth,
            "sources": args.get('sources', ['web']),
            "anchors_count": len(anchors),
            "anchors": anchors,
            "status": "ok",
            "message": f"多引擎搜索完成，发现 {len(anchors)} 个候选锚点（已按主题相关性过滤）。",
            "next_steps": [
                "1. 用 score_source 四维评分筛选（≥70 入采集队列）",
                "2. 用 fetch_content 抓取正文",
                "3. 用 fuse_analysis 做跨源融合"
            ],
        }
        try:
            _cache_try_put(_anchors_key, "", json.dumps(_anchors_result, ensure_ascii=False))
        except Exception:
            pass
        return _anchors_result
    except Exception as e:
        return {
            "subject": subject,
            "depth": depth,
            "anchors_count": 0,
            "anchors": [],
            "status": "error",
            "error": f"{type(e).__name__}: {str(e)[:200]}",
            "message": "搜索链执行失败，请检查网络或搜索配置。",
        }


def _read_local_file(url: str, max_chars: int = 0) -> tuple:
    """file:// 本地读取（缺口⑤，2026-09-10 修复）。

    策略③「数据文件通道」前提：允许 fetch 直接读本机文件。
    安全：仅接受 netloc 为空或 localhost 的绝对路径（file:///abs/path），
    拒绝远程主机与相对路径；异常抛给调用方处理。
    返回 (raw_text, title)；max_chars=0 全量，>0 截断。
    """
    from urllib.parse import unquote, urlparse
    p = urlparse(url)
    if p.netloc and p.netloc.lower() != 'localhost':
        raise ValueError(f"file:// 仅支持本机读取，拒绝远程主机: {p.netloc}")
    path = unquote(p.path)
    if not path.startswith('/'):
        raise ValueError(f"file:// 需要绝对路径: {url}")
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        raw = f.read()
    if max_chars and len(raw) > max_chars:
        raw = raw[:max_chars] + "\n...[truncated]"
    import os
    return raw, os.path.basename(path)


def _cache_try_get(key: str, ttl: Optional[int] = None) -> Optional[Dict]:
    """轻量 HTTP 缓存读（缺口①, 2026-09-10）。失败静默返回 None，缓存故障不阻塞抓取。"""
    try:
        if os.environ.get("INFOSEEK_ENABLE_CACHE", "1") != "1":
            return None
        sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
        from http_cache import get_http_cache
        return get_http_cache(key, ttl=ttl)
    except Exception:
        return None


def _cache_try_put(key: str, title: str, content: str, raw: str = "") -> None:
    """轻量 HTTP 缓存写（缺口①, 2026-09-10）。写入失败静默忽略。"""
    try:
        if os.environ.get("INFOSEEK_ENABLE_CACHE", "1") != "1":
            return None
        sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
        from http_cache import put_http_cache
        put_http_cache(key, title or "", content or "", raw=raw or "")
    except Exception:
        pass


def _mirror_resolve(url: str) -> str:
    """G4 (P2-2): 镜像域映射重写（references/mirror-domains.yaml）。

    命中 host 映射 → 重写为镜像 URL；未命中 / 关闭 / 异常 → 原样返回。
    """
    try:
        sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
        from mirror_map import resolve_url
        return resolve_url(url)
    except Exception:
        return url



def tool_fetch_content(args: Dict) -> Dict:
    """内容采集（v1.5.0+ 基础，v1.7.3 v1 增强，v1.8.0 v2 增强，v1.9.0 v3 多层递归）

    v1.9.0 v3 新增:
      - chain_strategy="recursive": 多层递归追踪（_fetch_chain_v3）
      - max_chain_depth: 1-3 递归深度（默认 1）
      - 见 _fetch_chain_v3() 防环 + 深度折扣

    v1.8.0 v2 保留:
      - chain_strategy="discover": 仅发现链接
      - chain_strategy="fetch": 逐个抓取摘要（1 层）
      - chain_strategy="graph": 生成 dot 引用图
      - chain_limit: 链式追踪最大 URL 数
      - subject: 引用相关性评分

    v1.7.3 v1 保留:
      - follow_links: 是否启用链式追踪
      - max_depth: 1-3 深度

    v1.0.1 PATCH (P0-2): 实现 L1 静态正文抓取（此前不抓正文，返回空内容）。
      - follow_links=False（默认）时也抓取页面正文，返回 content 字段
      - 正文提取：<title> + <h1>-<h3> + <p> 段落拼接（去 script/style）
    """
    import re as re_mod
    import urllib.request

    url = args['url']
    fmt = args.get('format', 'md')
    # v1.2.x L3/L4: 客户端可请求 extraction_level 1/2/3/4（钳制到合法范围）
    req_level = args.get('extraction_level', 1)
    try:
        req_level = int(req_level)
    except (TypeError, ValueError):
        req_level = 1
    req_level = max(1, min(4, req_level))
    max_retries = args.get('max_retries', 3)
    follow_links = args.get('follow_links', False)
    max_depth = args.get('max_depth', 1)
    chain_strategy = args.get('chain_strategy', 'discover')
    chain_limit = args.get('chain_limit', 5)
    subject = args.get('subject', '')
    max_chain_depth = args.get('max_chain_depth', 1)  # v1.9.0 新增

    extraction_strategy = [
        "Level 1: 静态页面 fetch",
        "Level 2: 反爬兜底（浏览器渲染）",
        "Level 3: 凭证辅助（API key）",
        "Level 4: 多媒体处理（截图/OCR）"
    ]

    related_links = []
    citation_graph = None
    chain_tracking_error = None
    _is_local = url.startswith('file://')  # 缺口⑤: file:// 本地读取标志（2026-09-10）

    # v1.0.1 PATCH (P0-2): L1 静态正文抓取（无论是否 follow_links 都执行）
    content = ""
    page_title = ""
    fetch_error = None

    # 缺口⑤ (2026-09-10): file:// 本地读取通道（策略③ 数据文件导入前提）
    # 仅本机绝对路径；读取成功后立即返回——避开 L1 urlopen 对 file:// 的二次读取
    # （urllib 内置 FileHandler 会重读文件，_extract_main_text 对纯文本返回空会覆盖内容）。
    # 本地文件无 L3 凭证 / L2 渲染 / 链接追踪语义，result 结构与网络路径保持一致。
    if _is_local:
        try:
            content, page_title = _read_local_file(url)
        except Exception as e:
            fetch_error = f"{type(e).__name__}: {str(e)[:100]}"
            content = ""
            page_title = ""
        return {
            "url": url,
            "local_file": True,
            "format": fmt,
            "max_retries": max_retries,
            "title": page_title,
            "content": content,
            "content_length": len(content),
            "extraction_level": 1,
            "fetch_error": fetch_error,
            "extraction_strategy": extraction_strategy,
            "chain_tracking_v3": {
                "enabled": False,
                "strategy": chain_strategy,
                "max_depth": max_depth,
                "max_chain_depth": max_chain_depth,
                "chain_limit": chain_limit,
                "subject": subject or "(none)",
                "discovered_count": 0,
                "discovered_links": [],
                "citation_graph_dot": None,
                "error": None,
                "version": "1.9.0",
            },
        }
    # 缺口① (2026-09-10): 全网络 HTTP 缓存先行（LRU+TTL+容量上限，~/.infoseek/http_cache/）
    _cache_hit = None
    _get_cache = None
    _put_cache = None
    try:
        from http_cache import get_http_cache as _get_cache, put_http_cache as _put_cache
        _cache_hit = _get_cache(url)
    except Exception:
        _cache_hit = None
    if _cache_hit:
        content = _cache_hit.get("content", "")
        page_title = _cache_hit.get("title", "")
    else:
        try:
            # G4 (P2-2): 镜像域映射重写（命中 → 镜像 host；未命中 → 原样）
            _req_url = _mirror_resolve(url)
            req = urllib.request.Request(_req_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Infoseek/1.0.1"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read()
                html = raw.decode("utf-8", errors="ignore")
                page_title = _extract_title_from_html(html)
                content = _extract_main_text(html)
            if _put_cache is not None and not fetch_error:
                try:
                    _put_cache(url, page_title, content)
                except Exception:
                    pass
        except Exception as e:
            fetch_error = f"{type(e).__name__}: {str(e)[:100]}"

    # v1.2.x L3: 请求级别 ≥3 且 L1 正文不足 → 凭证辅助抓取（KeyManager 注入，失败降级）
    extraction_level = 1
    if not _is_local and req_level >= 3 and len(content.strip()) < 100:
        host = ''
        try:
            host = url.split('//', 1)[1].split('/', 1)[0].split(':')[0]
        except IndexError:
            host = ''
        cred_html = _fetch_with_credential(url, host)
        if cred_html:
            content = cred_html
            page_title = page_title or _extract_title_from_html(cred_html) or page_title
            extraction_level = 3
            fetch_error = None

    # v1.0.1 C2 (L2): L1/L3 失败或正文过短 → playwright 无头渲染增强（可选，失败静默降级 L1）
    if not _is_local and len(content.strip()) < 100:
        render_html = _fetch_render_with_playwright(url)
        if render_html:
            content = render_html
            page_title = page_title or _extract_title_from_html(render_html) or page_title
            extraction_level = 2
            fetch_error = None

    if not _is_local and follow_links and max_depth > 0:
        try:
            _fl_cache = _cache_try_get(url)
            _fl_hit = bool(_fl_cache and _fl_cache.get("raw") is not None)
            if _fl_hit:
                _fl_html = _fl_cache["raw"]
                _fl_title = _fl_cache.get("title") or _extract_title_from_html(_fl_html) or ""
            else:
                req = urllib.request.Request(url, headers={"User-Agent": "Infoseek/1.9.0"})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    _fl_html = resp.read().decode("utf-8", errors="ignore")
                    _fl_title = _extract_title_from_html(_fl_html)
                    _cache_try_put(url, _fl_title or "", _fl_html[:20000] or "", _fl_html)
            if _fl_html:
                html = _fl_html
                base_title = _fl_title
                raw_links = re_mod.findall(r"href=[\\'](https?://[^\\']+)[\\']", html)
                seen = set()
                for link in raw_links:
                    if link in seen or link == url:
                        continue
                    seen.add(link)
                    related_links.append({"url": link, "depth": 1, "title": ""})
                    if len(related_links) >= chain_limit:
                        break
                if chain_strategy == "fetch":
                    related_links = _fetch_chain_v2(related_links, chain_limit, subject)
                elif chain_strategy == "graph":
                    citation_graph = _build_citation_graph(url, base_title, related_links)
                elif chain_strategy == "recursive":
                    # v1.9.0 v3 多层递归
                    related_links = _fetch_chain_v3(
                        url,
                        current_depth=0,
                        max_chain_depth=max_chain_depth,
                        seen=set(),
                        subject=subject,
                        chain_limit=chain_limit,
                        depth_discount=0.7,
                    )
                    # 同时生成 dot 引用图（递归结果）
                    citation_graph = _build_citation_graph(url, base_title, related_links)

        except Exception as e:
            chain_tracking_error = f"{type(e).__name__}: {str(e)[:100]}"
            related_links = []
            citation_graph = None

    result = {
        "url": url,
        "local_file": _is_local,  # 缺口⑤: True=本地文件读取（2026-09-10）
        "format": fmt,
        "max_retries": max_retries,
        "title": page_title,
        "content": content,  # v1.0.1 PATCH (P0-2): L1 静态正文；C2: L2 渲染增强；L3 凭证辅助
        "content_length": len(content),
        "extraction_level": extraction_level,  # 1=L1 静态 / 2=L2 渲染 / 3=L3 凭证 / 4=L4 多媒体
        "fetch_error": fetch_error,
        "extraction_strategy": extraction_strategy,
        "chain_tracking_v3": {  # v1.9.0 改名
            "enabled": follow_links,
            "strategy": chain_strategy,
            "max_depth": max_depth,
            "max_chain_depth": max_chain_depth,  # v1.9.0 新增
            "chain_limit": chain_limit,
            "subject": subject or "(none)",
            "discovered_count": len(related_links),
            "discovered_links": related_links[:chain_limit],
            "citation_graph_dot": citation_graph,
            "error": chain_tracking_error,
            "version": "1.9.0",
        }
    }

    # v1.2.x L4: 请求级别 ≥4 且命中多媒体 URL → 附加统一 multimodal chunk
    if req_level >= 4:
        media = _probe_media(url)
        if media:
            result['media'] = media
            result['multimodal'] = True
            result['extraction_level'] = 4
    return result


def _fetch_render_with_playwright(url: str, timeout: int = 15) -> str:
    """L2 抓取（v1.4.2 多引擎）：Camoufox 主 + Obscura 批 + Patchright/Chromium 备。

    壳函数（名称保留，兼容调用方）：委托 l2_renderer.render_html 走多引擎
    场景路由 + 健康状态机 + 故障 cross-over。全部引擎不可用 → 返回空串
    （调用方自动降级 L1，零侵入），与 v1.0.1 单 playwright 行为完全兼容。
    """
    try:
        from l2_renderer import render_html
        html = render_html(url, timeout=timeout)
        if html:
            return _extract_main_text(html, max_chars=12000)
        return ""
    except ImportError:
        # l2_renderer 缺失（理论不发生）→ 回退原生 playwright
        pass
    except Exception as e:
        log.warning(f"[L2] 多引擎渲染失败: {e}")
        return ""
    # ── 回退：原生 playwright（单引擎旧行为）──
    if not _dep_reg().is_available("playwright"):
        return ""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return ""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Infoseek/1.0.1")
                page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
                page.wait_for_timeout(1500)  # 等 JS 渲染
                html = page.content()
            finally:
                browser.close()
        return _extract_main_text(html, max_chars=12000)
    except Exception:
        return ""


def _get_host_credential(host: str) -> str:
    """L3 凭证获取（v1.2.x）：按 host 从 KeyManager 查找凭证。

    明文禁令：凭证仅内存返回给 playwright 注入，不写入日志/文件/状态。
    KeyManager 缺失 / 无匹配凭证 → 返回 ""（调用方自动降级 L1/L2）。
    """
    if not host:
        return ""
    try:
        import sys as _s
        from pathlib import Path as _P
        _root = _P(__file__).parent.parent
        if str(_root) not in _s.path:
            _s.path.insert(0, str(_root))
        from core.key_manager import get_key
        candidates = [host]
        if '.' in host:
            candidates.append(host.split('.')[0])
        candidates.append('default')
        for provider in candidates:
            try:
                v = get_key(provider)
                if v:
                    return v
            except Exception:
                continue
    except Exception:
        pass
    return ""


def _fetch_with_credential(url: str, host: str, timeout: int = 15) -> str:
    """L3 抓取（v1.2.x）：playwright 带凭证渲染 → 提取正文。

    凭证注入两种形态：
      - `Authorization: Bearer <cred>`（KeyManager 存 API key 时）
      - `Cookie: <name>=<value>` 前缀（登录源，解析为 playwright cookie）
    凭证缺失 / playwright 不可用 / 启动失败 → 返回 ""（降级 L1/L2，零侵入）。
    """
    if not _dep_reg().is_available("playwright"):
        return ""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return ""
    cred = _get_host_credential(host)
    if not cred:
        return ""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                extra_headers = {}
                cookie = None
                if cred.startswith('Cookie:'):
                    cookie = cred[7:].strip()
                else:
                    extra_headers['Authorization'] = f'Bearer {cred}'
                ctx = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Infoseek/1.0.1",
                    extra_http_headers=extra_headers,
                )
                if cookie and host:
                    try:
                        name = cookie.split('=', 1)[0].strip()
                        value = cookie.split('=', 1)[1].split(';', 1)[0].strip()
                        ctx.add_cookies([{
                            'name': name, 'value': value,
                            'domain': host, 'path': '/', 'url': f'https://{host}/',
                        }])
                    except Exception:
                        pass
                page = ctx.new_page()
                page.goto(url, timeout=timeout * 1000, wait_until="domcontentloaded")
                page.wait_for_timeout(1500)  # 等 JS 渲染
                html = page.content()
                ctx.close()
            finally:
                browser.close()
        return _extract_main_text(html, max_chars=12000)
    except Exception:
        return ""


_MEDIA_EXT = {
    'image': ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg', '.avif', '.ico'),
    'video': ('.mp4', '.webm', '.mov', '.avi', '.mkv', '.m3u8', '.flv', '.wmv'),
    'audio': ('.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a', '.wma', '.opus'),
}


def _classify_media(url: str, content_type: str = '') -> Optional[str]:
    """L4 多媒体分类（v1.2.x）：优先 Content-Type（image/video/audio 前缀），
    回退 URL 扩展名（去 query）。非媒体 → None。
    """
    if content_type:
        ct = content_type.lower().split(';')[0].strip()
        for kind in ('image', 'video', 'audio'):
            if ct.startswith(kind):
                return kind
    path = (url.split('?', 1)[0]).lower()
    for kind, exts in _MEDIA_EXT.items():
        if path.endswith(exts):
            return kind
    return None


def _probe_media(url: str) -> Optional[Dict]:
    """L4 多媒体探测（v1.2.x）：分类 + 元信息（format/size/content-type）。

    网络不可达时仅按 URL 扩展名分类（format 由扩展名推断）；
    whisper 转录为可选能力：未启用/不可用 → transcript_available=False（降级不崩）。
    """
    try:
        kind = _classify_media(url)
        if not kind:
            return None
        meta = {'format': None, 'size_bytes': None, 'content_type': None}
        try:
            import urllib.request
            req = urllib.request.Request(
                url, method='HEAD',
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Infoseek/1.0.1'})
            with urllib.request.urlopen(req, timeout=5) as resp:
                ct = resp.headers.get('Content-Type', '')
                kind2 = _classify_media(url, ct)
                if kind2:
                    kind = kind2
                meta['content_type'] = ct or None
                meta['format'] = (ct.split('/')[-1].split(';')[0] if ct else None)
                try:
                    cl = resp.headers.get('Content-Length')
                    meta['size_bytes'] = int(cl) if cl else None
                except (TypeError, ValueError):
                    meta['size_bytes'] = None
        except Exception:
            pass
        if not meta['format']:
            fname = url.split('?', 1)[0].rsplit('/', 1)[-1]
            meta['format'] = fname.rsplit('.', 1)[-1].lower() if '.' in fname else None
        # v2.5.0 G5 (P2): L4 转录启用——whisper 可选依赖 + 本地音频真实转录路径。
        # - whisper 未安装 / 模型不可达 → transcript=None + 原因标注（降级不崩）
        # - 本地媒体文件（file:// 或纯路径）且 whisper 可用 → 真实转录（≤2000 字）
        # - 网络媒体不自动下载转录（避免大流量）；INFOSEEK_WHISPER_MODEL 可指定模型
        transcript = None
        available = False
        note = 'whisper 转录为可选能力；未启用时 transcript=None（降级）。'
        try:
            # S7：此处语义=直接尝试 import（须识别 sys.modules 注入的 mock，不可用 is_available 缓存），
            # 故用 has_module 探测真实 import 名「whisper」，与收口前裸 import 行为零漂移。
            if not _dep_reg().has_module("whisper"):
                raise ImportError("whisper unavailable")
            import whisper  # noqa: F401  # 可选依赖
            if kind in ('video', 'audio'):
                available = True
                local_path = None
                if url.startswith('file://'):
                    from urllib.parse import unquote, urlparse
                    local_path = unquote(urlparse(url).path)
                elif '://' not in url and os.path.exists(url):
                    local_path = url
                if local_path and os.path.exists(local_path):
                    model_name = os.environ.get('INFOSEEK_WHISPER_MODEL', 'base')
                    model = whisper.load_model(model_name)
                    res = model.transcribe(local_path)
                    transcript = (res.get('text') or '').strip()[:2000]
                    note = f'whisper({model_name}) 转录完成（{len(transcript)} 字）'
                else:
                    note = ('whisper 可用；网络媒体未自动转录（本地文件经 file:// 或路径输入可转录）。'
                            'INFOSEEK_WHISPER_MODEL=' + os.environ.get('INFOSEEK_WHISPER_MODEL', 'base'))
        except ImportError:
            available = False
            note = 'whisper 未安装（pip install openai-whisper 可启用转录）'
        except Exception as e:  # noqa: BLE001 转录失败降级，不阻断媒体探测
            transcript = None
            available = False
            note = f'whisper 转录不可用（降级）: {type(e).__name__}'
        return {
            'media_type': kind,
            'metadata': meta,
            'transcript': transcript,
            'transcript_available': available,
            'note': note,
        }
    except Exception:
        return None


def _extract_title_from_html(html: str) -> str:
    import re as re_mod
    m = re_mod.search(r"<title>([^<]+)</title>", html, re_mod.IGNORECASE)
    if m:
        return m.group(1).strip()[:100]
    m = re_mod.search(r"<h1[^>]*>([^<]+)</h1>", html, re_mod.IGNORECASE)
    if m:
        return m.group(1).strip()[:100]
    return "(no title)"


def _extract_main_text(html: str, max_chars: int = 8000) -> str:
    """L1 静态正文提取（v1.0.1 PATCH / P0-2）

    策略：去 script/style/nav 标签 → 收集 h1-h3 + p 文本 → 去空白合并。
    返回纯文本（截断到 max_chars）。无正文时返回空串。
    """
    import re as re_mod
    if not html:
        return ""
    try:
        # 1. 去掉脚本/样式/导航块
        html = re_mod.sub(r"(?is)<(script|style|noscript|nav|footer|header)[^>]*>.*?</\1>", " ", html)
        # 2. 段落/标题标签内文本（含属性）
        blocks = re_mod.findall(r"(?is)<(h1|h2|h3|p|li)[^>]*>(.*?)</\1>", html)
        parts = []
        for _tag, body in blocks:
            text = re_mod.sub(r"(?s)<[^>]+>", "", body)
            text = re_mod.sub(r"&nbsp;|&#160;", " ", text)
            text = re_mod.sub(r"&amp;", "&", text)
            text = re_mod.sub(r"&lt;", "<", text)
            text = re_mod.sub(r"&gt;", ">", text)
            text = re_mod.sub(r"\s+", " ", text).strip()
            if text:
                parts.append(text)
        joined = "\n".join(parts)
        if len(joined) > max_chars:
            joined = joined[:max_chars] + "\n...[truncated]"
        return joined
    except Exception:
        return ""


def _fetch_chain_v2(links: list, limit: int, subject: str = "") -> list:
    import urllib.request
    import urllib.error
    import re as re_mod
    try:
        from anchor_adapter import _jaccard_similarity
        has_jaccard = True
    except ImportError:
        has_jaccard = False

    if not links:
        return []
    results = []
    for link_dict in links[:limit]:
        link_url = link_dict["url"]
        if link_url.startswith('file://'):
            # 缺口⑤: 本地文件链式读取（2026-09-10）
            try:
                raw_local, title_local = _read_local_file(link_url, max_chars=50000)
            except Exception as e:
                results.append({
                    "url": link_url,
                    "depth": link_dict.get("depth", 1),
                    "title": "(local read failed)",
                    "snippet": "",
                    "relevance_score": 0,
                    "error": f"{type(e).__name__}: {str(e)[:60]}",
                })
                continue
            text = re_mod.sub(r"\s+", " ", raw_local).strip()[:300]
            relevance = 0
            if has_jaccard and subject:
                relevance = _jaccard_similarity(text, subject)
            results.append({
                "url": link_url,
                "depth": link_dict.get("depth", 1),
                "title": title_local,
                "snippet": text + ("..." if len(text) >= 300 else ""),
                "relevance_score": relevance,
            })
            continue
        _v2_cached = _cache_try_get(link_url)
        if _v2_cached and _v2_cached.get("raw") is not None and _v2_cached.get("content"):
            _v2_html = _v2_cached["raw"]
            _v2_title = _v2_cached.get("title") or _extract_title_from_html(_v2_html) or ""
            _v2_text = _v2_cached.get("content", "")
            _v2_rel = 0
            if has_jaccard and subject:
                _v2_rel = _jaccard_similarity(_v2_text, subject)
            results.append({
                "url": link_url,
                "depth": link_dict.get("depth", 1),
                "title": _v2_title,
                "snippet": _v2_text + ("..." if len(_v2_text) >= 300 else ""),
                "relevance_score": _v2_rel,
            })
        else:
            try:
                # G4 (P2-2): 镜像域映射重写（链式追踪链接）
                _v2_req_url = _mirror_resolve(link_url)
                req = urllib.request.Request(_v2_req_url, headers={"User-Agent": "Infoseek/1.8.0"})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    html = resp.read().decode("utf-8", errors="ignore")[:50000]
                    title = _extract_title_from_html(html)
                    text = re_mod.sub(r"<[^>]+>", " ", html)
                    text = re_mod.sub(r"\s+", " ", text).strip()[:300]
                    relevance = 0
                    if has_jaccard and subject:
                        relevance = _jaccard_similarity(text, subject)
                    results.append({
                        "url": link_url,
                        "depth": link_dict.get("depth", 1),
                        "title": title,
                        "snippet": text + ("..." if len(text) >= 300 else ""),
                        "relevance_score": relevance,
                    })
                    _cache_try_put(link_url, title or "", text[:20000] or "", html)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
                results.append({
                    "url": link_url,
                    "depth": link_dict.get("depth", 1),
                    "title": "(fetch failed)",
                    "snippet": "",
                    "relevance_score": 0,
                    "error": f"{type(e).__name__}: {str(e)[:60]}",
                })
            except Exception as e:
                results.append({
                    "url": link_url,
                    "depth": link_dict.get("depth", 1),
                    "title": "(fetch error)",
                    "snippet": "",
                    "relevance_score": 0,
                    "error": f"{type(e).__name__}: {str(e)[:60]}",
                })
    if subject:
        results.sort(key=lambda x: -x["relevance_score"])
    return results


def _fetch_chain_v3(
    seed_url: str,
    current_depth: int = 0,
    max_chain_depth: int = 1,
    seen: set = None,
    subject: str = "",
    chain_limit: int = 5,
    depth_discount: float = 0.7,
    budget_remaining: int = 50,
) -> list:
    """链式抓取 v3：多层递归追踪（v1.9.0 新增）

    算法：
      1. 若 current_depth > max_chain_depth: return []
      2. 若 seed_url in seen: return []（防环）
      3. fetch seed → extract links (top chain_limit)
      4. 对每个 link 递归调用：
         - current_depth + 1
         - 应用 depth_discount^depth 到 relevance_score
         - tag with depth marker
      5. seen.add(seed_url)
      6. 返回扁平化的链式结果

    防环：seen 集合全局
    评分折扣：每个深度 × 0.7（深 1 层保留 70%，深 2 层 49%）
    预算控制：budget_remaining 默认 50，每抓一个 URL -1
    """
    import urllib.request
    import urllib.error
    import re as re_mod

    if seen is None:
        seen = set()
    if current_depth > max_chain_depth:
        return []
    if seed_url in seen:
        return []
    if budget_remaining <= 0:
        return []

    seen.add(seed_url)
    budget_remaining -= 1

    results = []

    # 缺口⑤: file:// 本地种子 → 叶子节点（本地文件无 http 链接语义，不递归）
    if seed_url.startswith('file://'):
        try:
            raw_local, title_local = _read_local_file(seed_url, max_chars=50000)
            text_clean = re_mod.sub(r"\s+", " ", raw_local).strip()[:300]
            relevance = 0
            if subject:
                try:
                    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
                    from anchor_adapter import _jaccard_similarity
                    relevance = _jaccard_similarity(text_clean, subject)
                except Exception:
                    relevance = 0
            relevance = int(relevance * (depth_discount ** current_depth))
            return [{
                "url": seed_url,
                "depth": current_depth,
                "title": title_local,
                "snippet": text_clean + ("..." if len(text_clean) >= 300 else ""),
                "relevance_score": relevance,
                "is_seed": current_depth == 0,
            }]
        except Exception:
            return []

    # 当前层：fetch + Jaccard（缺口①: 命中缓存跳过网络）
    html = ""
    _v3_cached = _cache_try_get(seed_url)
    if _v3_cached and _v3_cached.get("raw") is not None:
        html = _v3_cached["raw"]
        try:
            title = _extract_title_from_html(html)
            text = re_mod.sub(r"<[^>]+>", " ", html)
            text = re_mod.sub(r"\\s+", " ", text).strip()[:300]

            try:
                sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
                from anchor_adapter import _jaccard_similarity
                relevance = _jaccard_similarity(text, subject) if subject else 0
            except (ImportError, Exception):
                relevance = 0

            # 深度折扣
            relevance = int(relevance * (depth_discount ** current_depth))

            results.append({
                "url": seed_url,
                "depth": current_depth,
                "title": title,
                "snippet": text + ("..." if len(text) >= 300 else ""),
                "relevance_score": relevance,
                "is_seed": current_depth == 0,
            })

        except Exception:
            pass
    else:
        try:
            req = urllib.request.Request(seed_url, headers={"User-Agent": "Infoseek/1.9.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode("utf-8", errors="ignore")[:50000]
                title = _extract_title_from_html(html)
                text = re_mod.sub(r"<[^>]+>", " ", html)
                text = re_mod.sub(r"\\s+", " ", text).strip()[:300]

                try:
                    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
                    from anchor_adapter import _jaccard_similarity
                    relevance = _jaccard_similarity(text, subject) if subject else 0
                except (ImportError, Exception):
                    relevance = 0

                # 深度折扣
                relevance = int(relevance * (depth_discount ** current_depth))

                results.append({
                    "url": seed_url,
                    "depth": current_depth,
                    "title": title,
                    "snippet": text + ("..." if len(text) >= 300 else ""),
                    "relevance_score": relevance,
                    "is_seed": current_depth == 0,
                })

                # 缺口①: 真实抓取后写回（content=清洗文本, raw=原始HTML）
                _cache_try_put(seed_url, title or "", text[:20000] or "", html)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            return []
        except Exception:
            return []

    # 递归下一层
    if current_depth < max_chain_depth and html:
        raw_links = re_mod.findall(r"""href=["']([^"']+)["']""", html)
        raw_links = [l for l in raw_links if l.startswith("http")]  # v1.9.0 PATCH: 仅保留绝对 URL
        seen_in_layer = set()
        layer_count = 0
        for link in raw_links:
            if link in seen or link in seen_in_layer or link == seed_url:
                continue
            seen_in_layer.add(link)
            if layer_count >= chain_limit:
                break

            sub_results = _fetch_chain_v3(
                link,
                current_depth + 1,
                max_chain_depth,
                seen,
                subject,
                chain_limit,
                depth_discount,
                budget_remaining,
            )
            results.extend(sub_results)
            layer_count += 1
            budget_remaining -= sum(1 for r in sub_results if r.get('is_seed', False))

    return results


def _build_citation_graph(root_url: str, root_title: str, refs: list) -> str:
    if not refs:
        return ""
    lines = [
        "digraph citations {",
        "  rankdir=LR;",
        '  node [shape=box, style=rounded, fontname="Helvetica"];',
        f'  "ROOT: {root_title[:50]}" [style=filled, fillcolor=lightblue];',
    ]
    for ref in refs:
        short_url = ref["url"][:60]
        label = ref.get("title", short_url)[:50]
        lines.append(f'  "{short_url}" [label="{label}"];')
        lines.append(f'  "ROOT: {root_title[:50]}" -> "{short_url}";')
    lines.append("}")
    return "\n".join(lines)

