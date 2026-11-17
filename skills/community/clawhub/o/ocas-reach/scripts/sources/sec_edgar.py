"""SEC EDGAR connector — multi-step lookups with required User-Agent."""
import os
from . import _http

BASE = "https://data.sec.gov"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"


def _headers(auth):
    # SEC rejects requests without a real User-Agent identifying caller.
    return {"User-Agent": auth.get("user_agent", "ocas-reach (contact: os.environ.get("OCAS_AGENT_EMAIL", "agent@example.com"))")}


def _pad_cik(cik):
    return str(cik).lstrip("0").zfill(10)


def query(action, params, auth):
    h = _headers(auth)

    if action == "ticker_lookup":
        ticker = (params.get("ticker") or "").upper()
        if not ticker:
            raise ValueError("ticker_lookup requires {'ticker': '<symbol>'}")
        data = _http.get(TICKERS_URL, headers=h)
        # data is a dict of "0", "1", ... entries
        for _, row in data.items():
            if row.get("ticker", "").upper() == ticker:
                return {"ticker": ticker, "cik": _pad_cik(row["cik_str"]), "title": row.get("title")}
        return {"ticker": ticker, "cik": None, "title": None, "error": "not_found"}

    if action == "submissions":
        cik = _pad_cik(params.get("cik") or "")
        if not cik:
            raise ValueError("submissions requires {'cik': '<digits>'}")
        return _http.get(f"{BASE}/submissions/CIK{cik}.json", headers=h)

    if action == "facts":
        cik = _pad_cik(params.get("cik") or "")
        if not cik:
            raise ValueError("facts requires {'cik': '<digits>'}")
        return _http.get(f"{BASE}/api/xbrl/companyfacts/CIK{cik}.json", headers=h)

    if action == "filing":
        cik = _pad_cik(params.get("cik") or "")
        accession = (params.get("accession") or "").replace("-", "")
        if not cik or not accession:
            raise ValueError("filing requires {'cik': '<digits>', 'accession': '<no-dashes-or-with>'}")
        # Index of the filing
        return _http.get(f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/index.json", headers=h)

    raise ValueError(f"Unknown action: {action}")
