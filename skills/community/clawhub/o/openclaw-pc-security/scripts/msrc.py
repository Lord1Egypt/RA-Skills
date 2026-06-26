import requests
import time
import json
from pathlib import Path


def fetch_cvrf_document(cvrf_id, timeout_s=15):
    if not cvrf_id or not isinstance(cvrf_id, str) or not cvrf_id.strip():
        raise ValueError("cvrf_id is required")
    cid = cvrf_id.strip()
    url = f"https://api.msrc.microsoft.com/cvrf/v2.0/cvrf/{cid}"
    with requests.Session() as session:
        session.trust_env = False
        r = session.get(
            url,
            headers={"Accept": "application/json"},
            timeout=timeout_s,
            allow_redirects=False,
        )
        r.raise_for_status()
        return r.json()


def generate_cvrf_ids(start_id, end_id):
    def _parse(x):
        if not x or not isinstance(x, str) or not x.strip():
            raise ValueError("cvrf id is required")
        s = x.strip()
        parts = s.split("-", 1)
        if len(parts) != 2:
            raise ValueError(f"invalid cvrf id: {x}")
        y = int(parts[0])
        mmm = parts[1].strip().lower()
        months = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
        if mmm not in months:
            raise ValueError(f"invalid cvrf month: {x}")
        return y, months.index(mmm) + 1
    def _fmt(y, m):
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        return f"{y}-{months[m-1]}"
    sy, sm = _parse(start_id)
    ey, em = _parse(end_id)
    if (sy, sm) > (ey, em):
        raise ValueError("start_id must be <= end_id")
    out = []
    y, m = sy, sm
    while (y, m) <= (ey, em):
        out.append(_fmt(y, m))
        m += 1
        if m == 13:
            y += 1
            m = 1
    return out


def fetch_cvrf_document_cached(cvrf_id, cache_dir, timeout_s=15, rate_limit_s=0.6, retries=4):
    cid = (cvrf_id or "").strip()
    if not cid:
        raise ValueError("cvrf_id is required")
    cache_base = Path(cache_dir) if cache_dir else None
    cache_path = None
    missing_path = None
    if cache_base:
        cache_base.mkdir(parents=True, exist_ok=True)
        cache_path = cache_base / f"{cid}.json"
        missing_path = cache_base / f"{cid}.missing"
        if missing_path.exists():
            return None
        if cache_path.exists():
            try:
                return json.loads(cache_path.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                pass

    url = f"https://api.msrc.microsoft.com/cvrf/v2.0/cvrf/{cid}"
    last_exc = None
    for attempt in range(max(1, int(retries) + 1)):
        if rate_limit_s and rate_limit_s > 0:
            time.sleep(float(rate_limit_s))
        try:
            with requests.Session() as session:
                session.trust_env = False
                r = session.get(
                    url,
                    headers={"Accept": "application/json"},
                    timeout=timeout_s,
                    allow_redirects=False,
                )
                if r.status_code == 404:
                    r.close()
                    if missing_path:
                        try:
                            missing_path.write_text("404", encoding="utf-8")
                        except Exception:
                            pass
                    return None
                if r.status_code == 429:
                    ra = r.headers.get("Retry-After")
                    try:
                        wait_s = float(ra) if ra else 2.0
                    except Exception:
                        wait_s = 2.0
                    r.close()
                    time.sleep(max(0.5, min(30.0, wait_s)))
                    continue
                r.raise_for_status()
                data = r.json()
            if cache_path:
                try:
                    cache_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
                except Exception:
                    pass
            return data
        except Exception as e:
            last_exc = e
            time.sleep(min(2.0 ** attempt, 15.0))
    raise last_exc if last_exc else RuntimeError("fetch failed")


def fetch_kbs_by_cve_sug(cve_id, api_key, timeout_s=20, locale="en-US"):
    cid = (cve_id or "").strip().upper()
    if not cid:
        raise ValueError("cve_id is required")
    key = (api_key or "").strip()
    if not key:
        raise ValueError("api_key is required")
    loc = (locale or "en-US").strip()
    url = f"https://api.msrc.microsoft.com/sug/v2.0/{loc}/updates"
    params = {
        "$filter": f"cveId eq '{cid}'",
        "$select": "cveId,releaseDate,severity,impact,kbArticles,productName",
        "$top": "100",
    }
    with requests.Session() as session:
        session.trust_env = False
        r = session.get(
            url,
            params=params,
            headers={"Accept": "application/json", "api-key": key},
            timeout=timeout_s,
        )
        r.raise_for_status()
        data = r.json()
    kbs = set()
    if isinstance(data, dict) and isinstance(data.get("value"), list):
        for item in data["value"]:
            if not isinstance(item, dict):
                continue
            kb_articles = item.get("kbArticles")
            if isinstance(kb_articles, list):
                for a in kb_articles:
                    if not isinstance(a, dict):
                        continue
                    kb_num = a.get("kbNumber")
                    if kb_num:
                        kb_str = str(kb_num).strip()
                        if kb_str.isdigit():
                            kbs.add(f"KB{kb_str}")
                        else:
                            kbs.add(kb_str.upper())
    return {x.upper() for x in kbs if x}


def fetch_kbs_by_cves_sug(cve_ids, api_key, timeout_s=25, locale="en-US"):
    ids = [str(x).strip().upper() for x in (cve_ids or []) if x]
    ids = [x for i, x in enumerate(ids) if x and x not in ids[:i]]
    key = (api_key or "").strip()
    if not ids:
        return {}
    if not key:
        raise ValueError("api_key is required")
    loc = (locale or "en-US").strip()
    url = f"https://api.msrc.microsoft.com/sug/v2.0/{loc}/updates"
    filt = " or ".join([f"cveId eq '{cid}'" for cid in ids])
    params = {
        "$filter": f"({filt})" if len(ids) > 1 else filt,
        "$select": "cveId,kbArticles",
        "$top": "1000",
    }
    with requests.Session() as session:
        session.trust_env = False
        r = session.get(
            url,
            params=params,
            headers={"Accept": "application/json", "api-key": key},
            timeout=timeout_s,
        )
        r.raise_for_status()
        data = r.json()
    out = {cid: set() for cid in ids}
    if isinstance(data, dict) and isinstance(data.get("value"), list):
        for item in data["value"]:
            if not isinstance(item, dict):
                continue
            cid = str(item.get("cveId") or "").strip().upper()
            if not cid:
                continue
            kb_articles = item.get("kbArticles")
            if isinstance(kb_articles, list):
                for a in kb_articles:
                    if not isinstance(a, dict):
                        continue
                    kb_num = a.get("kbNumber")
                    if not kb_num:
                        continue
                    kb_str = str(kb_num).strip()
                    if kb_str.isdigit():
                        out.setdefault(cid, set()).add(f"KB{kb_str}")
                    else:
                        out.setdefault(cid, set()).add(kb_str.upper())
    return {k: {x.upper() for x in v if x} for k, v in out.items()}
