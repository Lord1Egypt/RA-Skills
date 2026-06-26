#!/usr/bin/env python3
"""
Find likely Investor Relations PDF URLs.

Scope:
- Discover PDF URLs from IR domains
- Optionally use SEC EDGAR as a PDF-discovery source
- Do NOT fetch structured financial data (use sec-finance for that)
"""

import argparse
import json
import sys
import time
import urllib.parse
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' module not found. Install with: pip3 install requests", file=sys.stderr)
    sys.exit(1)

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
DEFAULT_TIMEOUT = 20
HEAD_TIMEOUT = 10
ISSUERS_FILE = Path(__file__).resolve().parent.parent / "references" / "issuers.json"


def log(msg: str, level: str = "INFO"):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {msg}")


def load_issuers() -> list[dict]:
    if not ISSUERS_FILE.exists():
        return []
    return json.loads(ISSUERS_FILE.read_text())


ISSUERS = load_issuers()
ALIAS_MAP = {}
DOMAIN_MAP = {}
for issuer in ISSUERS:
    for alias in issuer.get("aliases", []):
        ALIAS_MAP[alias.lower()] = issuer
    if issuer.get("name"):
        ALIAS_MAP[issuer["name"].lower()] = issuer
    if issuer.get("ticker"):
        ALIAS_MAP[issuer["ticker"].lower()] = issuer
    if issuer.get("ir_domain"):
        DOMAIN_MAP[issuer["ir_domain"].lower()] = issuer


def resolve_issuer(company_or_domain: str | None = None, domain: str | None = None) -> dict | None:
    if company_or_domain:
        key = company_or_domain.strip().lower()
        if key in ALIAS_MAP:
            return ALIAS_MAP[key]
        if "." in key and key in DOMAIN_MAP:
            return DOMAIN_MAP[key]
    if domain:
        return DOMAIN_MAP.get(domain.strip().lower())
    return None


def infer_ir_domain(company_or_domain: str | None) -> str | None:
    if not company_or_domain:
        return None
    issuer = resolve_issuer(company_or_domain=company_or_domain)
    if issuer and issuer.get("ir_domain"):
        return issuer["ir_domain"]
    key = company_or_domain.strip().lower()
    if "." in key:
        return key
    return None


def infer_cik(company: str | None = None, domain: str | None = None) -> str | None:
    issuer = resolve_issuer(company_or_domain=company, domain=domain)
    return issuer.get("cik") if issuer else None


def find_via_wayback(domain: str, year: int | None = None, limit: int = 100) -> list[dict]:
    log(f"Searching Wayback Machine for PDFs under: {domain}")
    results = []
    seen = set()
    patterns = [
        f"*{domain}*/static-files/*.pdf",
        f"*{domain}*/assets/pdf/*.pdf",
        f"*{domain}*/en-US/assets/pdf/*.pdf",
        f"*{domain}*/annual-report/*.pdf",
        f"*{domain}*/annual-reports/*.pdf",
        f"*{domain}*/*.pdf",
    ]
    for pattern in patterns:
        cdx_url = (
            "https://web.archive.org/cdx/search/cdx"
            f"?url={urllib.parse.quote(pattern, safe='')}"
            "&output=json"
            f"&limit={limit}"
            "&fl=original,statuscode,mimetype,timestamp"
            "&filter=statuscode:200"
            "&filter=mimetype:application/pdf"
            "&collapse=original"
        )
        try:
            resp = requests.get(cdx_url, headers={"User-Agent": DEFAULT_USER_AGENT}, timeout=DEFAULT_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            for row in data[1:]:
                if len(row) < 4:
                    continue
                url, _, _, timestamp = row[:4]
                if url in seen:
                    continue
                if year and timestamp[:4] != str(year):
                    continue
                seen.add(url)
                results.append({
                    "url": url,
                    "year": timestamp[:4] if timestamp else None,
                    "timestamp": timestamp,
                    "source": "wayback",
                    "domain": domain,
                })
        except Exception as e:
            log(f"CDX query failed for pattern {pattern}: {e}", "WARN")
    log(f"Wayback Machine: found {len(results)} PDF(s)")
    return results


def find_via_edgar(cik: str, year: int | None = None, limit: int = 20) -> list[dict]:
    log(f"Searching SEC EDGAR filing index for PDF attachments: {cik}")
    results = []
    headers = {"User-Agent": DEFAULT_USER_AGENT, "Accept": "text/html,application/xhtml+xml"}
    forms = ["20-F", "6-K"]
    for form in forms:
        url = (
            "https://www.sec.gov/cgi-bin/browse-edgar"
            f"?action=getcompany&CIK={cik}&type={urllib.parse.quote(form)}"
            f"&owner=include&count={limit}"
        )
        try:
            resp = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
            resp.raise_for_status()
            html = resp.text
            import re
            pdf_links = re.findall(r'href="(/Archives/edgar/data/[^"]+\.pdf)"', html)
            dates = re.findall(r'(\d{4}-\d{2}-\d{2})', html)
            for i, link in enumerate(pdf_links[:limit]):
                filing_date = dates[i] if i < len(dates) else None
                filing_year = filing_date[:4] if filing_date else None
                if year and filing_year != str(year):
                    continue
                results.append({
                    "url": f"https://www.sec.gov{link}",
                    "year": filing_year,
                    "filing_date": filing_date,
                    "form": form,
                    "source": "sec-edgar",
                })
        except Exception as e:
            log(f"EDGAR search failed for {form}: {e}", "WARN")
    log(f"SEC EDGAR: found {len(results)} PDF(s)")
    return results


def probe_ir_direct(domain: str, year: int | None = None) -> list[dict]:
    log(f"Probing direct IR URLs on: {domain}")
    target_years = [str(year)] if year else ["2025", "2024", "2023"]
    templates = [
        "https://{domain}/en-US/assets/pdf/annual-report/{year}-Annual-Report.pdf",
        "https://{domain}/assets/pdf/annual-report/{year}-Annual-Report.pdf",
        "https://{domain}/annual-report-{year}.pdf",
        "https://{domain}/annual-reports/{year}.pdf",
    ]
    results = []
    for y in target_years:
        for tmpl in templates:
            url = tmpl.format(domain=domain, year=y)
            try:
                resp = requests.head(
                    url,
                    headers={"User-Agent": DEFAULT_USER_AGENT, "Referer": f"https://{domain}/"},
                    timeout=HEAD_TIMEOUT,
                    allow_redirects=True,
                )
                if resp.status_code == 200 and "pdf" in resp.headers.get("Content-Type", "").lower():
                    results.append({"url": url, "year": y, "source": "direct-probe", "domain": domain})
            except Exception:
                pass
    dedup = []
    seen = set()
    for item in results:
        if item["url"] not in seen:
            seen.add(item["url"])
            dedup.append(item)
    log(f"Direct probe: found {len(dedup)} accessible PDF(s)")
    return dedup


def find_pdfs(company: str | None = None, domain: str | None = None, year: int | None = None, sources: list[str] | None = None) -> list[dict]:
    sources = sources or ["wayback", "edgar", "direct"]
    domain = domain or infer_ir_domain(company)
    cik = infer_cik(company=company, domain=domain)
    all_results = []
    seen = set()

    def add(items: list[dict]):
        for item in items:
            if item["url"] not in seen:
                seen.add(item["url"])
                all_results.append(item)

    if domain and "wayback" in sources:
        add(find_via_wayback(domain, year=year))
    if cik and "edgar" in sources:
        add(find_via_edgar(cik, year=year))
    if domain and "direct" in sources:
        add(probe_ir_direct(domain, year=year))
    return all_results


def print_results(results: list[dict], output_format: str = "text"):
    if output_format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return
    if not results:
        print("No PDFs found.")
        return
    print(f"\nFound {len(results)} PDF URL(s):\n")
    print(f"{'#':<4} {'Year':<6} {'Form':<8} {'Source':<12} URL")
    print("-" * 100)
    for i, item in enumerate(results, 1):
        print(f"{i:<4} {str(item.get('year') or ''):<6} {str(item.get('form') or 'PDF'):<8} {item.get('source',''):<12} {item.get('url','')}")


def parse_args():
    parser = argparse.ArgumentParser(description="Find likely IR PDF URLs from IR domains and SEC EDGAR.")
    parser.add_argument("--company", type=str, help="Company name or ticker alias")
    parser.add_argument("--domain", type=str, help="IR domain to search")
    parser.add_argument("--year", type=int, help="Filter to a single year")
    parser.add_argument("--sources", nargs="+", choices=["wayback", "edgar", "direct"], default=["wayback", "edgar", "direct"])
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--output", type=str, help="Write JSON output to file")
    return parser.parse_args()


def main():
    args = parse_args()
    results = find_pdfs(company=args.company, domain=args.domain, year=args.year, sources=args.sources)
    if args.output:
        Path(args.output).write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print_results(results, output_format=args.format)


if __name__ == "__main__":
    main()
