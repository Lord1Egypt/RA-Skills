#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ctsearch_client.py — meta-analysis → ct-registry 统一端点 (ct-search.coze.site/run) 轻客户端

B2 (2026-09-04)：MDPI 等反爬出版商的全文 PDF 下载 + 出版商页面 review 标签解析，
需要真实浏览器（无头 urllib 被 403）。ct-registry 的 ct-search.coze.site/run 端点
已在服务端部署 Playwright（graphs.nodes.browser_utils），故把这部分浏览器重活委托给它，
source="publisher_pdf"，与 nmpa_pv 同源（仅浏览器抓取、无详情接口）。

契约（对齐 ct-registry/adapters/extsvc_client.py + graphs/sources.py）：
  - POST JSON {source:"publisher_pdf", doi, query_origin} 到端点，Authorization: Bearer <token>。
  - 端点返回 {"total_count":N, "projects":[{doi, pdf_base64|pdf_s3_url,
    review_tag, review_source, status}], "status":...}
    或 nmpa 式 project_list JSON 字符串（解析同形态）。
  - token 解析优先级：env CT_SEARCH_COZE_TOKEN > 动态 import ct-registry 内嵌公开 blob
    （endpoint_token.get_token，ct-base §5 公开凭据，不跨技能复制避免漂移）。

⚠️ 部署状态：publisher_pdf 节点已于 2026-09-05 实测确认部署在 ct-search.coze.site/run；
若日后端点返回 UNSUPPORTED_SOURCE（未部署/已下线），本客户端 graceful 返回 {ok:False, error:...}。
"""
import base64
import copy
import hashlib
import json
import os
import re
import socket
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
import uuid

ENDPOINT = os.environ.get("CT_SEARCH_ENDPOINT", "https://ct-search.coze.site/run")
# 2026-09-07 对齐 ct-literature pdf_download 的「流式批量」契约：publisher_pdf_batch
# 走 stream_run（SSE 实时返回节点事件），避免长连接被网关按单响应超时掐断。
STREAM_ENDPOINT = os.environ.get("CT_SEARCH_ENDPOINT_STREAM",
                                 "https://ct-search.coze.site/stream_run")
CT_REGISTRY_SKILL = os.path.expanduser("~/.workbuddy/skills/ct-registry")

# 单批篇数上限：必须与 coze 端 publisher_pdf_batch_node.MAX_BATCH_ITEMS 一致；
# 超限由调用方拆批（每批一次传送）。
MAX_BATCH_ITEMS = 50
# sub-batch 之间强制间隔（秒），避免触发 coze 端限流（与 ct-literature 同款设定）。
COZE_BATCH_INTERVAL = 5


# ---------------------------------------------------------------------------
# 请求级去重闸门（防「同参重复 coze 调用」刷屏，对齐 coze_client._DEDUP_CACHE）
# 根因（2026-09-15 飞书 searchlog 复盘）：选题门控「简单分析」路径下，调用方
# （agent 重试 / 工作台重跑）把偶发失败或空返回误判为「没查到」，于是原样重发
# 同一 querystr → coze 每次真跑一次检索，飞书表同一请求重复落库（实测 2 查询 ×
# 4 轮、~2 分钟一轮）。这道闸门：窗口内命中同参请求 → 直接回放缓存，不再出站。
#
# 设计要点：
#   1. 跨进程生效——发布沙箱里每次 CLI 调用是独立进程，纯内存缓存拦不住，故落盘
#      （文件缓存 + 进程内 dict 双写）。缓存目录 env CT_SEARCH_DEDUP_DIR 覆盖。
#   2. 只缓存成功（works 非空且 error 为空）——偶发失败不入缓存，否则毒化窗口内
#      后续真实重试（与 coze_client._dedup_store 同一红线）。
#   3. 窗口默认 300s（env CT_SEARCH_DEDUP_WINDOW 覆盖，<=0 关闭）——选题探针是秒级
#      幂等只读，5 分钟内同参重复调用视为同一意图，直接复用。
#   4. 键含全部影响结果的入参（source/keyword/year_from/year_to/max_results），
#      任一不同即视为不同请求，绝不串味。
# ---------------------------------------------------------------------------
_DEDUP_LOCK = threading.Lock()
_DEDUP_MEM = {}  # fp -> (ts, result_dict)，进程内快路径


def _dedup_dir() -> str:
    d = os.environ.get("CT_SEARCH_DEDUP_DIR")
    if not d:
        d = os.path.join(tempfile.gettempdir(), "ct_search_dedup")
    try:
        os.makedirs(d, exist_ok=True)
    except Exception:
        return ""
    return d


def _dedup_window() -> int:
    try:
        return int(os.environ.get("CT_SEARCH_DEDUP_WINDOW", "300"))
    except ValueError:
        return 300


def _dedup_key(source, keyword, year_from, year_to, max_results) -> str:
    payload = "|".join([
        "literature_search", str(source or ""), str(keyword or "").strip().lower(),
        "" if year_from is None else str(year_from),
        "" if year_to is None else str(year_to),
        str(max_results),
    ])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _dedup_load(fp: str):
    """返回缓存的 result dict（命中且未过期），否则 None。"""
    win = _dedup_window()
    if win <= 0:
        return None
    now = time.time()
    with _DEDUP_LOCK:
        hit = _DEDUP_MEM.get(fp)
        if hit and (now - hit[0]) <= win:
            return copy.deepcopy(hit[1])
        # 内存未命中 → 查磁盘（跨进程）
        d = _dedup_dir()
        if d:
            p = os.path.join(d, fp + ".json")
            try:
                if os.path.isfile(p) and (now - os.path.getmtime(p)) <= win:
                    with open(p, encoding="utf-8") as f:
                        res = json.load(f)
                    _DEDUP_MEM[fp] = (os.path.getmtime(p), res)
                    return copy.deepcopy(res)
            except Exception:
                pass
    return None


def _dedup_save(fp: str, result: dict) -> None:
    """仅缓存成功结果（works 非空且无 error）。失败不入，避免毒化窗口内真实重试。"""
    if _dedup_window() <= 0:
        return
    if not isinstance(result, dict) or result.get("error") or not result.get("works"):
        return
    now = time.time()
    with _DEDUP_LOCK:
        _DEDUP_MEM[fp] = (now, copy.deepcopy(result))
        d = _dedup_dir()
        if d:
            p = os.path.join(d, fp + ".json")
            tmp = p + ".%d.tmp" % os.getpid()
            try:
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False)
                os.replace(tmp, p)
            except Exception:
                try:
                    os.remove(tmp)
                except Exception:
                    pass


def _dedup_evict() -> None:
    """清理过期磁盘缓存，防临时目录无限增长（低频、best-effort）。"""
    d = _dedup_dir()
    win = _dedup_window()
    if not d or win <= 0:
        return
    now = time.time()
    try:
        for name in os.listdir(d):
            if not name.endswith(".json"):
                continue
            p = os.path.join(d, name)
            try:
                if now - os.path.getmtime(p) > win * 4:
                    os.remove(p)
            except Exception:
                pass
    except Exception:
        pass


def _resolve_token() -> str:
    """token 优先级：env CT_SEARCH_COZE_TOKEN > 动态复用 ct-registry 内嵌公开 blob。"""
    tok = os.environ.get("CT_SEARCH_COZE_TOKEN")
    if tok:
        return tok
    try:
        sys.path.insert(0, os.path.join(CT_REGISTRY_SKILL, "adapters"))
        from endpoint_token import get_token as _gt  # ct-registry 内嵌公开 token
        return _gt() or ""
    except Exception:
        return ""


def _headers() -> dict:
    h = {"Content-Type": "application/json"}
    tok = _resolve_token()
    if tok:
        h["Authorization"] = "Bearer " + tok
    return h


def _query_origin() -> str:
    """稳定机器标识（ct-base §8.6：由客户端注入，原样透传）。"""
    return "sha256:" + hashlib.sha256(socket.gethostname().encode("utf-8")).hexdigest()


def _skill_version() -> str:
    """技能版本号：优先读技能根 SKILL.md frontmatter 的 `version:`（单一事实来源），
    读取失败回退常量。位置：coze 请求顶层信封字段（与 query_origin 同级，ct-base §1.2）。
    """
    try:
        md = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SKILL.md")
        with open(md, encoding="utf-8") as f:
            head = f.read(4000)
        m = re.search(r"^version:\s*([0-9][\w.\-]*)", head, re.M)
        if m:
            return m.group(1)
    except Exception:
        pass
    return "1.0.0"


def _dig_output(node):
    """从单个流式事件对象（workflow_end / node_end）提取最终 output（兼容多层嵌套）。"""
    if not isinstance(node, dict):
        return None
    out = node.get("output")
    if out is None and isinstance(node.get("data"), dict):
        out = node["data"].get("output")
    if (out is None and isinstance(node.get("data"), dict)
            and isinstance(node["data"].get("data"), dict)):
        out = node["data"]["data"].get("output")
    return out


def _has_real_output(o) -> bool:
    """判定节点输出是否携带真实结果（空 dict/list 不算）。"""
    if isinstance(o, dict):
        return any(k in o for k in ("projects", "project_list", "s3_url", "status", "total_count"))
    if isinstance(o, str):
        try:
            d = json.loads(o)
        except Exception:
            return bool(o) and "[DONE]" not in o
        return isinstance(d, dict) and any(
            k in d for k in ("projects", "project_list", "s3_url", "status", "total_count"))
    if isinstance(o, list):
        return len(o) > 0
    return False


def _get(url: str, timeout: int = 60, retries: int = 2):
    """GET 带重试（429 指数退避），供 S3 外置结果拉取用。"""
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "meta-analysis-skill/1.10"})
            proxy_handler = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(proxy_handler)
            with opener.open(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries:
                wait = min(30 * (2 ** attempt), 120)
                time.sleep(wait)
                last = "HTTP 429"
                continue
            raise
        except Exception as e:
            last = "%s: %s" % (type(e).__name__, e)
            time.sleep(0.5)
    raise RuntimeError(str(last))


def _parse_coze_stream(resp, log_fn) -> list:
    """解析 ct-search stream_run 的 SSE 流，提取 publisher_pdf_batch 最终 projects 列表。

    事件类型（外层 data.type）：workflow_start / node_start / node_end /
    workflow_end / error / ping。最终结果优先取 workflow_end.output（非空），
    否则回退到「含真实结果的」node_end 输出。兼容 projects 列表 / project_list
    字符串或字典 / s3_url 外置三种形态。
    """
    events = []
    buf = b""
    for chunk in resp:
        buf += chunk
        while b"\n" in buf:
            line_b, buf = buf.split(b"\n", 1)
            line = line_b.decode("utf-8", "ignore").rstrip("\r")
            if line.startswith("data:"):
                ds = line[len("data:"):].lstrip()
                if ds and ds != "[DONE]":
                    try:
                        events.append(json.loads(ds))
                    except Exception:
                        pass
    if not events:
        try:
            events.append(json.loads(buf.decode("utf-8", "ignore")))
        except Exception:
            log_fn("[coze] 流式响应无法解析为事件")
            return []

    workflow_end_out = None
    node_outputs = []
    for evt in events:
        if not isinstance(evt, dict):
            continue
        etype = evt.get("type")
        inner = evt.get("data")
        if isinstance(inner, dict) and inner.get("type"):
            etype = inner.get("type")
            node = inner
        else:
            node = evt
        if etype == "workflow_start":
            log_fn("[coze:workflow_start] 工作流开始")
        elif etype == "node_start":
            nt = node.get("node_title") or node.get("title") or node.get("node_id") or ""
            log_fn("[coze:node_start] %s" % nt)
        elif etype == "node_end":
            nt = node.get("node_title") or node.get("node_id") or ""
            o = _dig_output(node)
            if o is not None:
                node_outputs.append(o)
                if nt:
                    try:
                        sz = len(json.dumps(o, ensure_ascii=False))
                    except Exception:
                        sz = 0
                    log_fn("[coze:node_end] %s -> %d 字节输出" % (nt, sz))
        elif etype == "workflow_end":
            workflow_end_out = _dig_output(node)
            log_fn("[coze:workflow_end] 工作流结束")
        elif etype == "error":
            log_fn("[coze] 流式返回 error: %s"
                   % json.dumps(evt.get("data") or evt, ensure_ascii=False)[:400])
            return []
        # ping 等其它类型：忽略

    final = None
    if _has_real_output(workflow_end_out):
        final = workflow_end_out
    else:
        for o in reversed(node_outputs):
            if _has_real_output(o):
                final = o
                break
        if final is None and node_outputs:
            final = node_outputs[-1]
    if final is None:
        for evt in reversed(events):
            if isinstance(evt, dict) and ("projects" in evt or "project_list" in evt):
                final = evt
                break
    if final is None:
        return []
    if isinstance(final, str):
        try:
            final = json.loads(final)
        except Exception:
            log_fn("[coze] 最终结果非 JSON: %s" % final[:200])
            return []
    if not isinstance(final, dict):
        return []

    projects = final.get("projects")
    if isinstance(projects, list):
        return projects
    pl = final.get("project_list")
    s3 = final.get("s3_url")
    if pl is None and s3:
        try:
            raw = _get(s3, timeout=60)
            pl = json.loads(raw.decode("utf-8"))
        except Exception as e:
            log_fn("[coze] S3 结果拉取失败: %s" % e)
            return []
    if pl is not None:
        if isinstance(pl, str):
            try:
                pl = json.loads(pl)
            except Exception:
                return []
        if isinstance(pl, dict):
            p = pl.get("projects")
            if isinstance(p, list):
                return p
    return []


def resolve_publisher_pdfs(identifiers: list, query_origin: str = None,
                           timeout: int = 1200, progress=None) -> list:
    """批量委托 ct-search 端点（stream_run + publisher_pdf_batch）把间接链接/DOI
    解码为可直接下载的真实直链。

    解码上移 coze、下载在本地：coze 端对每条标识执行 A(解码+直下探测验证真实 PDF)
    → 若 A 失败则 B(浏览器+S3)，仅返回经探测/上传验证过的真实直链（pdf_url /
    pdf_s3_url）；拿不到真实直链只返 pdf_failed，绝不返回伪直链。本地只负责下载
    返回的真实直链。

    Args:
        identifiers: 统一标识列表（open_access_url / preprint.url / doi 混排）。
        progress: 可选进度回调 fn(msg)。
    Returns:
        list[dict]，每项为 {key, doi, pdf_url, pdf_s3_url, status, via, ...}；
        与 coze 端 publisher_pdf_batch 回参同形态。空列表表示无结果/失败。
    """
    if progress is None:
        progress = lambda m: None
    if not identifiers:
        return []
    # 拆批（与 coze 端 MAX_BATCH_ITEMS 一致）
    chunks = [identifiers[i:i + MAX_BATCH_ITEMS]
              for i in range(0, len(identifiers), MAX_BATCH_ITEMS)] or [[]]
    collected = []
    for ci, chunk in enumerate(chunks, 1):
        if not chunk:
            continue
        if ci > 1:
            progress("[coze] 等待 %ds 后发送下一批..." % COZE_BATCH_INTERVAL)
            time.sleep(COZE_BATCH_INTERVAL)
        payload = {
            "source": "publisher_pdf_batch",
            "keyword": json.dumps(chunk, ensure_ascii=False),
            "mode": "search",
            "log_feishu": True,
            "query_origin": query_origin or _query_origin(),
            # 家族契约：每次出站必带 request_id，便于日志表过滤/去重
            "request_id": uuid.uuid4().hex,
            "skill_version": _skill_version(),
            "locale": "zh",
            "skillname": "meta-analysis",
            # 审计透传（对齐 ct-literature 新格式）：Coze 端飞书节点原样落库
            "querystr": json.dumps({
                "type": "publisher_pdf_batch",
                "caller_skill": "meta-analysis",
                "purpose": "pdf_download_optin",
                "batch_size": len(chunk),
                "identifiers": chunk,
            }, ensure_ascii=False),
            "params": {"user_language": "zh"},
        }
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(STREAM_ENDPOINT, data=body,
                                     headers=_headers(), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                part = _parse_coze_stream(r, progress)
        except Exception as e:
            progress("[coze] 流式传送失败: %s: %s" % (type(e).__name__, e))
            part = None
        if part is None:
            # 整批失败 → 逐条标 manual（本地不再重试，符合「只做一次 coze 传送」）
            for k in chunk:
                collected.append({"key": k, "doi": "", "pdf_url": None,
                                  "pdf_s3_url": None, "status": "manual",
                                  "error": "coze 传送失败"})
            continue
        collected.extend(part)
    return collected


def search_literature(source: str = "europepmc", keyword: str = None,
                      year_from: int = None, year_to: int = None,
                      max_results: int = 50, timeout: int = 300) -> dict:
    """选题门控「简单分析」路径：直接调用 ct-search 远端服务做轻量文献检索/去重探针。

    这是 ct-literature 的统一文献检索后端（source 与 ct-literature 共用同一 Coze 端点），
    因此**无需安装 ct-literature 技能**即可使用——选题门控在未装 ct-literature 且用户选
    「简单分析」时走这条路径。

    当前支持的 source（与 ct-literature/adapters/fetch_coze_unified.py 同步）：
      openalex / europepmc / biorxiv / medrxiv / semantic_scholar / arxiv
    选题去重默认 europepmc（命中数 + 前几篇标题，直接喂 Stage 4 新颖性维度 + R7）。

    窗口内同参重复调用直接回放缓存（跨进程，见 _dedup_*），不再重复出站——防
    调用方「误判为空→重试」把同一 querystr 反复打到 coze/飞书日志（2026-09-15 复盘）。

    Returns:
        dict: {source, works:[...], total_count:N, error:str|None, from_cache:bool}
        works 为空且 error 非空 → 调用方降级到 in-skill literature_probe.py。
    """
    if not keyword:
        return {"source": source, "works": [], "total_count": 0,
                "error": "keyword 为空"}
    fp = _dedup_key(source, keyword, year_from, year_to, max_results)
    cached = _dedup_load(fp)
    if cached is not None:
        cached = dict(cached)
        cached["from_cache"] = True
        return cached
    result = _search_literature_uncached(
        source, keyword, year_from, year_to, max_results, timeout)
    _dedup_save(fp, result)
    _dedup_evict()
    return result


def _search_literature_uncached(source, keyword, year_from, year_to,
                                max_results, timeout) -> dict:
    payload = {
        "source": source,
        "mode": "search",
        "keyword": keyword,
        "max_results": max_results,
        "log_feishu": True,
        "query_origin": _query_origin(),
        # 家族契约：每次出站必带 request_id（meta SKILL.md §6），便于日志表过滤/去重
        "request_id": uuid.uuid4().hex,
        "skill_version": _skill_version(),
        "locale": "zh",
        "params": {"user_language": "zh"},
        "skillname": "meta-analysis",
        # 审计透传（对齐 ct-literature 新格式）：Coze 端飞书节点把 querystr 原样落库。
        # 修复老格式只存 {"source": ...} 导致后台飞书记录信息量不足的问题。
        "querystr": json.dumps({
            "type": "literature_search",
            "purpose": "topic_gate_simple_analysis",
            "caller_skill": "meta-analysis",
            "query": keyword,
            "source": source,
            "max_results": max_results,
            "year_from": year_from,
            "year_to": year_to,
        }, ensure_ascii=False),
    }
    if year_from:
        payload["year_from"] = year_from
    if year_to:
        payload["year_to"] = year_to

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    # 主路径 /stream_run（SSE 流式）：长检索不被网关单响应超时掐断
    try:
        req = urllib.request.Request(STREAM_ENDPOINT, data=body,
                                     headers=_headers(), method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            projects = _parse_coze_stream(r, lambda m: None)
        # 注意：_parse_coze_stream 解析失败返回 []（而非 None）——若直接接受，
        # 「解析失败」会伪装成「检索无结果」，上游据此误判重试 → 同参重复出站
        # （2026-09-15 飞书 searchlog 实测 2 查询×4 轮 burst 的成因之一）。
        # 空列表视同失败，继续走 /run 回退拿真实结果。
        if projects:
            return {"source": source, "works": projects,
                    "total_count": len(projects), "error": None}
    except Exception as e:
        # 落到 /run 回退
        pass
    # 回退 /run（非流式）
    try:
        req2 = urllib.request.Request(ENDPOINT, data=body,
                                      headers=_headers(), method="POST")
        with urllib.request.urlopen(req2, timeout=timeout) as r2:
            data = json.loads(r2.read().decode("utf-8"))
        return _parse_run_response(data, source)
    except Exception as e:
        return {"source": source, "works": [], "total_count": 0,
                "error": "ct-search 请求失败: %s: %s" % (type(e).__name__, e)}


def _parse_run_response(data, source):
    """解析 /run（非流式）返回体 → 本地统一格式（与 fetch_coze_unified 对齐）。"""
    if isinstance(data.get("project_list"), str):
        try:
            pl = json.loads(data["project_list"])
            works = pl.get("projects", [])
            return {"source": source, "works": works,
                    "total_count": pl.get("total_count", len(works)), "error": None}
        except (json.JSONDecodeError, TypeError):
            pass
    if "projects" in data and "works" not in data:
        data["works"] = data.pop("projects")
        data["total_count"] = data.get("total_count", len(data["works"]))
    return {"source": source, "works": data.get("works", []),
            "total_count": data.get("total_count", len(data.get("works", []))),
            "error": data.get("error")}


def fetch_publisher_pdf(doi: str, query_origin: str = None, timeout: int = 240) -> dict:
    """委托 ct-search 端点用真实浏览器抓取反爬出版商全文 PDF + 解析 review 标签。

    2026-09-07 起内部改用 stream_run + publisher_pdf_batch 统一契约（与 ct-literature
    pdf_download 同款），单 DOI 作为单元素列表传入；返回形态保持不变。

    Returns: {ok, pdf_bytes|pdf_url, review_tag:bool|None, review_source, status, error}
      - ok=True 且 pdf_bytes 存在 → 调用方直接落盘；
      - ok=True 且 pdf_url 存在 → 调用方另行 GET 下载（S3 预签名，通常直连可下）；
      - ok=False → error 说明（UNSUPPORTED_SOURCE 未部署 / 超时 / 反爬失败）。
    """
    if not doi:
        return {"ok": False, "error": "doi 为空"}
    items = resolve_publisher_pdfs([doi], query_origin=query_origin,
                                   timeout=timeout, progress=lambda m: None)
    if not items:
        return {"ok": False, "error": "coze 未返回 publisher_pdf_batch 结果",
                "status": "no_result"}
    rec = items[0]
    if rec.get("status") == "manual":
        return {"ok": False, "error": rec.get("error", "coze 传送失败"),
                "status": "manual"}
    pdf_b64 = rec.get("pdf_base64")
    s3_url = rec.get("pdf_s3_url")
    direct_url = rec.get("pdf_url")
    pdf_url = s3_url or direct_url
    is_s3 = bool(s3_url)
    pdf_bytes = None
    if pdf_b64:
        try:
            pdf_bytes = base64.b64decode(pdf_b64)
        except Exception:
            pdf_bytes = None
    if not (pdf_bytes or pdf_url):
        return {"ok": False,
                "error": rec.get("error", "coze 未返回可下载直链"),
                "status": rec.get("status", "failed")}
    return {
        "ok": True,
        "pdf_bytes": pdf_bytes,
        "pdf_url": pdf_url,
        "s3": is_s3,
        "review_tag": rec.get("review_tag"),
        "review_source": rec.get("review_source"),
        "status": rec.get("status", "ok"),
        "error": None,
    }


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="ct-search 客户端（文献检索 + 出版商 PDF）")
    sub = ap.add_subparsers(dest="cmd")

    # 文献检索子命令（选题门控「简单分析」路径，无需安装 ct-literature）
    sp = sub.add_parser("search", help="调用 ct-search 远端做轻量文献检索/去重探针")
    sp.add_argument("--source", default="europepmc",
                    choices=["openalex", "europepmc", "biorxiv", "medrxiv",
                             "semantic_scholar", "arxiv"],
                    help="数据源（默认 europepmc）")
    sp.add_argument("--keyword", required=True, help="检索词（英文）")
    sp.add_argument("--year-from", type=int, default=None, help="起始年份")
    sp.add_argument("--year-to", type=int, default=None, help="截止年份")
    sp.add_argument("--max-results", type=int, default=50, help="每源最大返回数")
    sp.add_argument("--timeout", type=int, default=300, help="HTTP 超时秒数")

    # 出版商 PDF 子命令（保留旧用法）
    pp = sub.add_parser("pdf", help="解析/下载出版商 PDF（默认子命令）")
    pp.add_argument("doi", nargs="*", help="单篇或多篇 DOI（批量走 publisher_pdf_batch）")
    pp.add_argument("--batch", action="store_true", help="强制批量模式（多篇一次传送）")

    args = ap.parse_args()

    if args.cmd == "search":
        res = search_literature(
            source=args.source, keyword=args.keyword,
            year_from=args.year_from, year_to=args.year_to,
            max_results=args.max_results, timeout=args.timeout,
        )
        print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
    else:
        # 默认 / pdf 子命令：旧行为
        dois = getattr(args, "doi", [])
        if args.cmd != "pdf" and not dois:
            # 未给子命令也未给 doi：提示
            ap.error("请提供 DOI（pdf 模式）或使用 search 子命令")
        if args.batch and len(dois) > 1:
            res = resolve_publisher_pdfs(dois, progress=print)
            print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
        else:
            for d in dois:
                print(json.dumps(fetch_publisher_pdf(d), ensure_ascii=False, indent=2, default=str))
