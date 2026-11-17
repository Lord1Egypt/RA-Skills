#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prospero_probe.py — PROSPERO 国际系统评价前瞻性注册库 自动检索探针。

零依赖（仅标准库 urllib），用于本地选题评估时自动核查「是否已有同类
已注册/已发表系统评价方案」，作为去重与新颖性判断的第三类真实证据
（另两类为 Europe PMC 的 Cochrane/PubMed SR-MA 命中、ClinicalTrials.gov 注册试验数）。

上游现状（2026-09-24 实测）：
  - PROSPERO 公开 REST 搜索 API（/api/PROSPERO/search?q=）对所有参数名与方法
    恒定返回 {"status":"error","errormessage":"Error code: header value undefined"}
    —— 属服务端故障，非本模块问题。
  - PROSPERO 网站检索页已改为 React SPA，仅返回 ~1.3KB 外壳 HTML，结果靠前端
    JS 拉取，服务端无渲染结果，HTML 抓取不可行。
因此本模块设计为先「真实尝试」再「优雅降级」：
  - 若上游恢复，会自动解析并返回真实 hit_count + 样本（PROSPERO ID / 标题）。
  - 若上游故障，明确 status="unavailable" + error（上游原因）+ manual_url
    （一键手动核查深链），绝不编造命中数。
"""
import json
import re
import urllib.request
import urllib.parse

API = "https://www.crd.york.ac.uk/prospero/api/PROSPERO/search"
WEB = "https://www.crd.york.ac.uk/prospero/search"


def manual_url(topic):
    """构造 PROSPERO 高级检索一键深链（手动核查用）。"""
    return "https://www.crd.york.ac.uk/prospero/#searchadvanced?search=" + urllib.parse.quote(topic)


def _parse_body(data):
    """尝试解析 API 返回体，返回 (ok, hit_count, sample) 或 (False, None, None)。"""
    # JSON 形态（PROSPERO 文档约定）
    try:
        j = json.loads(data)
        if isinstance(j, dict) and j.get("status") == "ok":
            res = j.get("results") or j.get("data") or j.get("reviews") or []
            if isinstance(res, list):
                sample = []
                for it in res[:5]:
                    if isinstance(it, dict):
                        sample.append({
                            "id": it.get("id") or it.get("PROSPERO_ID") or it.get("review_id"),
                            "title": it.get("title") or it.get("PUBLICATION_TITLE")
                                     or it.get("plain_english_summary", "")[:120],
                        })
                return True, len(res), sample
    except (ValueError, TypeError):
        pass
    # XML / 文本形态：直接抓 PROSPERO 编号
    ids = re.findall(r"CRD\d{6}", data)
    if ids:
        sample = [{"id": i} for i in ids[:5]]
        return True, len(ids), sample
    return False, None, None


def probe(topic, timeout=20, max_sample=5):
    """自动检索 PROSPERO 是否已注册同类系统评价。

    Returns dict:
        status      : "available" | "unavailable"
        hit_count   : int | None
        sample      : [{"id":..., "title":...}, ...]
        error       : str | None   （上游原因，便于透明展示）
        source      : str | None   （"api" / "api_xml" / "web" / None）
        manual_url  : 一键手动核查深链
        note        : 说明
    """
    out = {
        "status": "unavailable",
        "hit_count": None,
        "sample": [],
        "error": None,
        "source": None,
        "manual_url": manual_url(topic),
        "note": "",
    }
    if not topic or not topic.strip():
        out["error"] = "empty topic"
        out["note"] = "主题为空白，无法检索 PROSPERO。"
        return out

    # 1) REST API（真实尝试）
    try:
        url = API + "?q=" + urllib.parse.quote(topic)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (meta-analysis skill probe)"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read().decode("utf-8", "replace")
        ok, cnt, sample = _parse_body(data)
        if ok:
            out.update(status="available", hit_count=cnt, sample=sample, source="api")
            return out
        # 命中但解析不出（多为服务端错误 JSON）
        try:
            j = json.loads(data)
            out["error"] = "api: " + str(j.get("errormessage") or j.get("error") or "non-ok body")
        except (ValueError, TypeError):
            out["error"] = "api returned non-parsable body (%d bytes)" % len(data)
    except Exception as e:  # 网络/超时/拒绝
        out["error"] = "api request failed: %s: %s" % (type(e).__name__, e)

    # 2) 网站 SPA 抓取（兜底真实尝试，通常不可行）
    try:
        url = WEB + "?q=" + urllib.parse.quote(topic)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (meta-analysis skill probe)"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            html = r.read().decode("utf-8", "replace")
        ids = re.findall(r"CRD\d{6}", html)
        if ids:
            out.update(status="available", hit_count=len(ids),
                       sample=[{"id": i} for i in ids[:max_sample]], source="web")
            return out
    except Exception:
        pass  # 网站 SPA 失败不覆盖 API 的错误信息

    out["note"] = ("PROSPERO 自动检索上游暂不可用（REST API 服务端报错 / 网站改为 SPA 无服务端结果）；"
                   "请使用 manual_url 手动核查，或待上游恢复后本探针将自动返回真实命中数。")
    return out


if __name__ == "__main__":
    import sys
    _t = sys.argv[1] if len(sys.argv) > 1 else "SGLT2 inhibitors heart failure"
    print(json.dumps(probe(_t), ensure_ascii=False, indent=2))
