#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
registry_probe.py — In-skill ClinicalTrials.gov registry probe for meta-analysis
topic selection (local, self-contained, no coze / no ct-registry deploy needed).

WHY THIS EXISTS
---------------
`a1_topic_selection` previously left the registry crowding dimension as
`registry_probe:"skipped"` in the local flow, so the "expected studies /
direction crowding" signal was unavailable without deploying ct-registry.
ClinicalTrials.gov exposes a public, unauthenticated v2 REST API
(https://clinicaltrials.gov/api/v2/studies) — we query it directly with the
standard library only (urllib), mirroring `literature_probe.py`'s zero-dependency
design. This fills the crowding dimension with REAL registered-trial counts.

Returns a dict shaped exactly like the legacy ct-registry probe consumed by
`block_a.a1_topic_selection` (reads `.get("total")`), so the two are drop-in
interchangeable:
    {"status", "total", "returned", "sample":[{nct,title,status}], "note"}

Degrades gracefully (status="error", total=None) on network failure — never
aborts the topic-selection stage.
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://clinicaltrials.gov/api/v2/studies"
UA = "meta-analysis-skill/2.1.1"

# 仅取选题查重需要的字段，减小响应体
_FIELDS = "NCTId,BriefTitle,OverallStatus,Condition,InterventionName"


def _get_json(url, timeout=30, max_retries=3, backoff=2.0):
    """GET `url`, parse JSON, with unified retry/backoff (mirrors literature_probe)."""
    last = None
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                ra = e.headers.get("Retry-After")
                wait = float(ra) if ra else backoff ** (attempt - 1)
                if attempt < max_retries:
                    time.sleep(wait)
                    continue
                last = e
                break
            if 500 <= e.code < 600:
                if attempt < max_retries:
                    time.sleep(backoff ** (attempt - 1))
                    continue
                last = e
                break
            raise  # 4xx other than 429 → non-retryable
        except (urllib.error.URLError, OSError, TimeoutError) as e:
            if attempt < max_retries:
                time.sleep(backoff ** (attempt - 1))
                continue
            last = e
            break
    raise RuntimeError("ClinicalTrials.gov request failed after %d retries: %s"
                       % (max_retries, last))


def probe(topic, max_results=5, condition=None, intervention=None):
    """Probe ClinicalTrials.gov for registered trials on a topic.

    Args:
        topic: free-text query (used as `query.term` when condition/intervention
               are not supplied). Europe PMC-style PICO strings work fine here
               because CT.gov `query.term` searches across all fields.
        max_results: cap on returned sample records (totalCount is always the
                     full API total, uncapped).
        condition / intervention: optional structured overrides — when given,
               mapped to `query.cond` / `query.int` for a tighter count.

    Returns:
        dict: {status, total, returned, sample[], note}
    """
    params = {
        "format": "json",
        "countTotal": "true",
        "pageSize": str(max(1, min(max_results, 50))),
        "fields": _FIELDS,
    }
    if condition or intervention:
        if condition:
            params["query.cond"] = condition
        if intervention:
            params["query.int"] = intervention
    else:
        params["query.term"] = topic

    url = BASE + "?" + urllib.parse.urlencode(params)
    try:
        j = _get_json(url)
    except Exception as e:  # noqa: BLE001 - degrade, never abort A1
        return {"status": "error", "total": None, "returned": None,
                "sample": [], "note": "ClinicalTrials.gov 探针失败: %s" % e}

    total = j.get("totalCount")
    studies = (j.get("studies") or []) if isinstance(j.get("studies"), list) else []
    sample = []
    for s in studies[:max_results]:
        ps = (s.get("protocolSection") or {}) if isinstance(s, dict) else {}
        ident = ps.get("identificationModule") or {}
        st = ps.get("statusModule") or {}
        sample.append({
            "nct": ident.get("nctId"),
            "title": ident.get("briefTitle"),
            "status": st.get("overallStatus"),
        })
    if total is None:
        note = "ClinicalTrials.gov 未返回 totalCount（响应异常）；样本 %d 条仍可用作参考。" % len(sample)
        status = "partial" if sample else "error"
    else:
        note = "已注册试验 %d 项（ClinicalTrials.gov 实时）。" % total
        status = "ok"
    return {"status": status, "total": total, "returned": len(sample),
            "sample": sample, "note": note}


def probe_local(topic, max_results=5):
    """Convenience wrapper used by `a1_topic_selection` when no coze/ct-registry
    probe is supplied. Same return shape as the legacy ct-registry probe."""
    return probe(topic, max_results=max_results)


if __name__ == "__main__":
    import sys
    _t = sys.argv[1] if len(sys.argv) > 1 else "SGLT2 inhibitors heart failure"
    print(json.dumps(probe_local(_t), ensure_ascii=False, indent=2))
