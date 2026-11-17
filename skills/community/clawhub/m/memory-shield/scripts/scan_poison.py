#!/usr/bin/env python3
"""memory-shield: scan_poison — detect injected instructions and contradictions.

Usage:
  python3 scan_poison.py --memory <file_or_dir> [--report <file>]

Heuristic scanner: flags imperative instructions embedded in data,
contradictory facts, and import anomalies. Flags go to QUARANTINE —
nothing is deleted. Secrets are masked in the report.
"""
import argparse, datetime, os, re, sys

SECRET_KEYWORDS = (
    r'api[_-]?key|access[_-]?key|auth[_-]?token|token|secret|'
    r'passwd|pwd|password|credential|creds'
)
SECRET_PATTERNS = [
    re.compile(r'(?i)\b(sk-[A-Za-z0-9]{6,})\b'),
    re.compile(rf'(?i)\b({SECRET_KEYWORDS})\s*[:=]\s*["\']?[^\s"\']{{3,}}'),
    re.compile(r'(?i)\b(ghp_|github_pat_|gho_|glpat-|clh_|xox[bap]?-|AKIA[0-9A-Z]{16})[A-Za-z0-9_]+'),
]

def mask(line: str) -> str:
    for pat in SECRET_PATTERNS:
        line = pat.sub(lambda m: '🔒 ' + m.group(0)[:8] + '…', line)
    return line

INJECTION_PATTERNS = [
    (r'(?i)\bignore (all )?(previous|prior|above) (instructions|rules|system)\b', "looks injected"),
    (r'(?i)\byou (are|must|should|need to) (now |always )?(ignore|forget|override)\b', "override instruction"),
    (r'(?i)\b(disregard|forget) (your|all) (instructions|rules|training)\b', "disregard instruction"),
    (r'(?i)\b\[?system\]?[:：]\s*(you|ignore|now)\b', "system-role injection"),
    (r'(?i)\b(never|always) (mention|reveal|say|tell)\b', "hidden-behavior instruction"),
    (r'(?i)\brepeat (after me|the following)\b', "copy-paste injection"),
]
ANOMALY_RE = re.compile(r'(?i)(0x[0-9a-f]{8,}|%%|§{3,}|\x00)')
# Own-report lines (quarantine flags) must never re-trigger the scanner.
REPORT_FLAG_RE = re.compile(r'\[(injected|contradiction|anomaly)\]')

def is_binary(fp, chunk=8192):
    try:
        with open(fp, 'rb') as f:
            return b'\x00' in f.read(chunk)
    except OSError:
        return False

def read_lines(paths, exclude):
    """Yield (file, lineno, line) for every text line in the given paths."""
    for p in paths:
        ap = os.path.abspath(p)
        if os.path.isfile(ap):
            if ap == exclude:
                continue
            if is_binary(ap):
                continue
            try:
                with open(ap, 'r', encoding='utf-8', errors='replace') as f:
                    for i, line in enumerate(f, 1):
                        yield ap, i, line.rstrip('\n')
            except OSError as e:
                print(f"! {ap}: {e}", file=sys.stderr)
        elif os.path.isdir(ap):
            for dp, _, fs in os.walk(ap):
                for fn in sorted(fs):
                    fp = os.path.join(dp, fn)
                    if os.path.abspath(fp) == exclude:
                        continue
                    if is_binary(fp):
                        continue
                    try:
                        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                            for i, line in enumerate(f, 1):
                                yield fp, i, line.rstrip('\n')
                    except OSError as e:
                        print(f"! {fp}: {e}", file=sys.stderr)

def scan(records):
    flags = []
    for fp, lineno, line in records:
        if REPORT_FLAG_RE.search(line):
            continue  # own-report line, skip (anti self-quarantine)
        for pat, why in INJECTION_PATTERNS:
            if re.search(pat, line):
                flags.append((fp, lineno, "injected", why, line.strip()[:140]))
                break
        else:
            if ANOMALY_RE.search(line):
                flags.append((fp, lineno, "anomaly", "suspicious marker", line.strip()[:140]))
    return flags

def scan_contradictions(records):
    kv = {}
    for fp, lineno, line in records:
        m = re.match(r'^\s*([A-Za-zА-Яа-яЁё_][A-Za-z0-9А-Яа-яЁё_ .\-]{2,40})\s*[:=]\s*(.+)$', line)
        if m:
            key, val = m.group(1).strip().lower(), m.group(2).strip().lower()
            if len(val) < 60:
                kv.setdefault(key, []).append((fp, lineno, val))
    out = []
    for key, vals in kv.items():
        uniq = {v for _, _, v in vals}
        if len(uniq) > 1 and len(vals) > 1:
            fp, lineno, _ = vals[0]
            out.append((fp, lineno, "contradiction",
                        f"same key '{key}' stored with different values",
                        " | ".join(v for _, _, v in vals[:3])[:140]))
    return out

def main():
    ap = argparse.ArgumentParser(description="Poison scan (memory-shield)")
    ap.add_argument("--memory", nargs="+", required=True, help="file(s) or dir(s) to scan")
    ap.add_argument("--report", default="scan_report.md", help="output report")
    args = ap.parse_args()

    report_abs = os.path.abspath(args.report)
    records = list(read_lines(args.memory, report_abs))
    flags = scan(records) + scan_contradictions(records)
    total = len(records)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M") + " UTC"
    with open(args.report, "w", encoding="utf-8") as f:
        f.write(f"SCAN {now} — {total} lines checked\n")
        if flags:
            f.write(f"⚠️ QUARANTINE ({len(flags)}):\n")
            for fp, i, kind, why, txt in flags:
                rel = os.path.relpath(fp)
                f.write(f"  {rel}:{i} [{kind}] {why}: {mask(txt)}\n")
        else:
            f.write("✅ CLEAN — no suspicious patterns detected\n")
    print(f"✅ scan done: {len(flags)} flags -> {args.report}")
    for fp, i, kind, why, txt in flags[:10]:
        print(f"  {os.path.relpath(fp)}:{i} [{kind}] {why}: {mask(txt)}")

if __name__ == "__main__":
    main()
