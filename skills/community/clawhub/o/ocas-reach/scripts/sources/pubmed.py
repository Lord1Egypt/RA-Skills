"""PubMed E-utilities connector — esearch + efetch + esummary."""
from . import _http

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def _key_param(auth):
    val = auth.get("value")
    return {"api_key": val} if val else {}


def query(action, params, auth):
    if action == "search":
        term = params.get("term")
        if not term:
            raise ValueError("search requires {'term': '<query>'}")
        limit = int(params.get("limit", 20))
        q = {
            "db": params.get("db", "pubmed"),
            "term": term,
            "retmode": "json",
            "retmax": limit,
            "sort": params.get("sort", "relevance"),
        }
        q.update(_key_param(auth))
        url = f"{BASE}/esearch.fcgi?{_http.qs(q)}"
        result = _http.get(url)
        ids = ((result or {}).get("esearchresult") or {}).get("idlist") or []
        return {"esearch": result, "pmids": ids}

    if action == "fetch":
        pmids = params.get("pmids") or []
        if not pmids:
            raise ValueError("fetch requires {'pmids': [...]}")
        q = {
            "db": params.get("db", "pubmed"),
            "id": ",".join(str(p) for p in pmids),
            "rettype": params.get("rettype", "abstract"),
            "retmode": params.get("retmode", "xml"),
        }
        q.update(_key_param(auth))
        url = f"{BASE}/efetch.fcgi?{_http.qs(q)}"
        return {"efetch_raw": _http.get(url)}

    if action == "summary":
        pmids = params.get("pmids") or []
        if not pmids:
            raise ValueError("summary requires {'pmids': [...]}")
        q = {
            "db": params.get("db", "pubmed"),
            "id": ",".join(str(p) for p in pmids),
            "retmode": "json",
        }
        q.update(_key_param(auth))
        url = f"{BASE}/esummary.fcgi?{_http.qs(q)}"
        return _http.get(url)

    raise ValueError(f"Unknown action: {action}")
