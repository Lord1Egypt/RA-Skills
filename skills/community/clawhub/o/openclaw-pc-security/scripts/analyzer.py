import requests
import re
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pathlib import Path
import csv
import kbmap
import datetime

DEFAULT_CREDS = [
    ("admin", "openclaw"),
]

VULNERABLE_VERSIONS = {
    "1.0.0": ["CVE-2021-41617"],
    "1.1.0": ["CVE-2021-41617"],
    "1.2.0": ["CVE-2025-26465"],
    "v2026.3.2": []
}

SENSITIVE_PATHS = [
    "/api/status",
    "/api/v1/status",
    "/status",
    "/api/config",
    "/api/v1/config",
    "/config",
]

SENSITIVE_KEYWORDS_RE = re.compile(r"(token|api[_-]?key|secret|authorization|bearer|password|private[_-]?key)", re.IGNORECASE)

def _sev_rank(x):
    s = (x or "").strip().lower()
    if s == "critical":
        return 50
    if s == "high":
        return 40
    if s == "medium":
        return 30
    if s == "low":
        return 20
    if s == "info":
        return 10
    return 0

def _parse_version_nums(v):
    if not v or not isinstance(v, str):
        return None
    s = v.strip()
    if not s:
        return None
    s = s.lstrip("vV")
    parts = s.split(".")
    nums = []
    for p in parts:
        if not p.isdigit():
            return None
        nums.append(int(p))
    return tuple(nums) if nums else None

def _cmp_versions(a, b):
    va = _parse_version_nums(a)
    vb = _parse_version_nums(b)
    if va is None or vb is None:
        return None
    n = max(len(va), len(vb))
    va = va + (0,) * (n - len(va))
    vb = vb + (0,) * (n - len(vb))
    if va < vb:
        return -1
    if va > vb:
        return 1
    return 0

def _load_csv_cve_watchlist():
    cves = []
    try:
        base = Path(__file__).resolve().parent.parent
        csv_path = base / "papar" / "cve_analysis_result.csv"
        if not csv_path.exists():
            return cves
        with csv_path.open("r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f)
            rows = list(reader)
            if not rows:
                return cves
            header = [h.strip().lower() for h in rows[0]] if rows and rows[0] else []
            cve_col = 0
            if header and "cve" in header:
                cve_col = header.index("cve")
                data_rows = rows[1:]
            else:
                data_rows = rows
            for r in data_rows:
                if not r:
                    continue
                try:
                    v = r[cve_col].strip()
                except Exception:
                    continue
                if v and v.upper().startswith("CVE-"):
                    cves.append(v.upper())
    except Exception:
        return []
    return sorted({x for x in cves})

CSV_CVE_WATCHLIST = _load_csv_cve_watchlist()

def _is_https(url):
    return url.lower().startswith("https://")

def check_weak_credentials(url, timeout_s=2, verify=True):
    if not verify:
        warnings.simplefilter("ignore", InsecureRequestWarning)
    login_url = f"{url}/login"
    with requests.Session() as session:
        session.trust_env = False
        for username, password in DEFAULT_CREDS:
            try:
                response = session.post(
                    login_url,
                    json={"username": username, "password": password},
                    headers={"Content-Type": "application/json"},
                    timeout=timeout_s,
                    verify=verify,
                    allow_redirects=False,
                )
                if response.status_code == 200 and ("token" in response.text or "success" in response.text):
                    return {"vulnerable": True, "creds": f"{username}:{password}"}
            except requests.RequestException:
                continue
            
    return {"vulnerable": False}

def analyze_version(version):
    issues = []
    if version == "unknown":
        issues.append({
            "type": "unknown_version",
            "details": "Version could not be determined, manual verification recommended",
            "severity": "Low"
        })
    elif version in VULNERABLE_VERSIONS:
        cves = VULNERABLE_VERSIONS[version]
        if cves:
            issues.append({
                "type": "outdated_version",
                "version": version,
                "cves": cves,
                "severity": "High"
            })
    return issues

def check_sensitive_exposure(url, timeout_s=2, verify=True, max_bytes=65536):
    if not verify:
        warnings.simplefilter("ignore", InsecureRequestWarning)
    hits = []
    with requests.Session() as session:
        session.trust_env = False
        for p in SENSITIVE_PATHS:
            try:
                r = session.get(url + p, timeout=timeout_s, verify=verify, allow_redirects=False, stream=True)
            except requests.RequestException:
                continue
            if not r.ok:
                r.close()
                continue
            content_type = (r.headers.get("Content-Type") or "").lower()
            if "text" not in content_type and "json" not in content_type and "html" not in content_type:
                r.close()
                continue
            try:
                buf = bytearray()
                for chunk in r.iter_content(chunk_size=4096):
                    if not chunk:
                        break
                    remain = max_bytes - len(buf)
                    if remain <= 0:
                        break
                    if len(chunk) > remain:
                        buf.extend(chunk[:remain])
                        break
                    buf.extend(chunk)
                enc = r.encoding or "utf-8"
                text = bytes(buf).decode(enc, errors="ignore")
            finally:
                r.close()
            kws = {m.group(1).lower().replace("-", "_") for m in SENSITIVE_KEYWORDS_RE.finditer(text)}
            if kws:
                hits.append({"path": p, "keywords": sorted(kws)})
    if not hits:
        return None
    return {
        "type": "potential_sensitive_exposure",
        "details": "Sensitive keywords detected on unauthenticated endpoints",
        "severity": "Medium",
        "hits": hits,
    }

def run_analysis(service_info, assume_version=None, enable_cred_check=True, enable_exposure_check=True, timeout_s=2):
    url = service_info['url']
    print(f"[*] Analyzing service at {url}...")
    
    version = service_info.get("version")
    if assume_version and (not version or version == "unknown"):
        version = assume_version
    
    verify = True
    if _is_https(url):
        verify = bool(service_info.get("tls_verify", True))

    findings = {
        "target": url,
        "service": service_info.get("service"),
        "version": version,
        "port": service_info.get("port"),
        "scheme": service_info.get("scheme"),
        "evidence": service_info.get("evidence"),
        "tls_verify": verify if _is_https(url) else None,
        "vulnerabilities": []
    }
    
    version_issues = analyze_version(version)
    if version_issues:
        findings["vulnerabilities"].extend(version_issues)
        for issue in version_issues:
            print(f"[!] Vulnerability Found: {issue['type']} (CVEs: {issue.get('cves', [])})")
    
    if CSV_CVE_WATCHLIST:
        findings["csv_cve_watchlist"] = CSV_CVE_WATCHLIST
        top = CSV_CVE_WATCHLIST[:20]
        findings["vulnerabilities"].append({
            "type": "cve_watchlist",
            "details": f"{len(CSV_CVE_WATCHLIST)} CVEs loaded from papar/cve_analysis_result.csv",
            "cves": top,
            "severity": "Low"
        })
            
    if enable_cred_check:
        print("[*] Checking for weak credentials...")
        cred_check = check_weak_credentials(url, timeout_s=timeout_s, verify=verify)
        if cred_check['vulnerable']:
            vuln = {
                "type": "weak_credentials",
                "details": "Default credentials accepted (credentials redacted)",
                "severity": "Critical"
            }
            findings["vulnerabilities"].append(vuln)
            print("[!!!] CRITICAL: Weak Credentials Found!")
        else:
            print("[+] Credential check passed (no default credentials found)")

    if enable_exposure_check:
        exposure = check_sensitive_exposure(url, timeout_s=timeout_s, verify=verify)
        if exposure:
            findings["vulnerabilities"].append(exposure)

    findings["vulnerabilities"].sort(key=lambda v: (-_sev_rank(v.get("severity")), str(v.get("type") or "")))
    return findings


