import csv
import re
from pathlib import Path


_KB_RE = re.compile(r"\bKB\d{5,8}\b", re.IGNORECASE)
_CVE_RE = re.compile(r"\bCVE-\d{4}-\d{4,7}\b", re.IGNORECASE)


def extract_cve_kb_map_from_cvrf(cvrf_doc):
    mapping = {}
    vulns = []
    if isinstance(cvrf_doc, dict):
        vulns = cvrf_doc.get("Vulnerability") or []
    if not isinstance(vulns, list):
        return {}

    for v in vulns:
        if not isinstance(v, dict):
            continue
        cve = v.get("CVE")
        if not isinstance(cve, str) or not cve.strip():
            cves = []
            for k in ("Cves", "CVEs", "cves"):
                x = v.get(k)
                if isinstance(x, list):
                    cves = [str(i) for i in x if i]
                    break
            if cves:
                cve = cves[0]
        if not isinstance(cve, str) or not cve.strip():
            continue
        cve = cve.strip().upper()
        if not _CVE_RE.search(cve):
            continue

        kbs = set()
        rems = v.get("Remediations") or []
        if isinstance(rems, list):
            for r in rems:
                if not isinstance(r, dict):
                    continue
                for val in r.values():
                    if isinstance(val, str):
                        for kb in _KB_RE.findall(val):
                            kbs.add(kb.upper())

        if kbs:
            mapping.setdefault(cve, set()).update(kbs)

    return mapping


def save_cve_kb_map_csv(csv_path, mapping, source="msrc_cvrf"):
    p = Path(csv_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for cve, kbs in (mapping or {}).items():
        if not kbs:
            continue
        for kb in sorted({str(x).upper() for x in kbs if x}):
            rows.append([str(cve).upper(), kb, source])
    rows.sort(key=lambda r: (r[0], r[1]))

    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cve", "kb", "source"])
        w.writerows(rows)


def load_cve_kb_map_csv(csv_path):
    p = Path(csv_path)
    if not p.exists():
        return {}
    mapping = {}
    with p.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return {}
    header = [h.strip().lower() for h in rows[0]] if rows[0] else []
    start = 0
    cve_idx = 0
    kb_idx = 1 if len(header) > 1 else 0
    if header and ("cve" in header and "kb" in header):
        cve_idx = header.index("cve")
        kb_idx = header.index("kb")
        start = 1
    for r in rows[start:]:
        if not r:
            continue
        try:
            cve = str(r[cve_idx]).strip().upper()
            kb = str(r[kb_idx]).strip().upper()
        except Exception:
            continue
        if not cve or not kb:
            continue
        if not _CVE_RE.search(cve):
            continue
        if not _KB_RE.search(kb):
            continue
        mapping.setdefault(cve, set()).add(kb)
    return mapping


def load_cves_from_csv(csv_path):
    p = Path(csv_path)
    if not p.exists():
        return []
    cves = set()
    with p.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            for cell in row:
                if not cell:
                    continue
                for m in _CVE_RE.finditer(str(cell).upper()):
                    cves.add(m.group(0))
    return sorted(cves)


def merge_cve_kb_maps(base_map, new_map):
    merged = {k: set(v) for k, v in (base_map or {}).items()}
    for cve, kbs in (new_map or {}).items():
        merged.setdefault(str(cve).upper(), set()).update({str(x).upper() for x in (kbs or set()) if x})
    return merged


def evaluate_missing_kbs(installed_kbs, cve_kb_map, cves=None, include_unmapped=False, unmapped_limit=20):
    installed = {str(x).strip().upper() for x in (installed_kbs or []) if x}
    findings = []
    cve_list = [str(x).strip().upper() for x in (cves or []) if x]
    if cve_list:
        unmapped = []
        def _cve_year(c):
            try:
                return int(str(c).split("-")[1])
            except Exception:
                return -1
        for cve in cve_list:
            kbs = (cve_kb_map or {}).get(cve)
            if not kbs:
                if include_unmapped:
                    unmapped.append(cve)
                continue
            kb_set = {str(x).strip().upper() for x in (kbs or set()) if x}
            if not kb_set:
                continue
            if installed.intersection(kb_set):
                continue
            findings.append(
                {
                    "type": "windows_cve_unpatched",
                    "details": f"No KB found for {cve} (expected one of: {', '.join(sorted(kb_set))})",
                    "severity": "High",
                    "cve": cve,
                    "kbs": sorted(kb_set),
                }
            )
        if include_unmapped and unmapped:
            unmapped_sorted = sorted(
                {x for x in unmapped if x},
                key=lambda c: (-_cve_year(c), str(c)),
            )
            sample = unmapped_sorted[: max(0, int(unmapped_limit))]
            findings.append(
                {
                    "type": "windows_cve_no_kb_mapping",
                    "details": f"No KB mapping found for {len(unmapped_sorted)} CVEs (showing newest up to {unmapped_limit}): {', '.join(sample)}",
                    "severity": "Low",
                    "cves": sample,
                }
            )
        return findings

    for cve, kbs in sorted((cve_kb_map or {}).items(), key=lambda kv: kv[0]):
        kb_set = {str(x).strip().upper() for x in (kbs or set()) if x}
        if not kb_set:
            continue
        if installed.intersection(kb_set):
            continue
        findings.append(
            {
                "type": "windows_cve_unpatched",
                "details": f"No KB found for {cve} (expected one of: {', '.join(sorted(kb_set))})",
                "severity": "High",
                "cve": cve,
                "kbs": sorted(kb_set),
            }
        )
    return findings
