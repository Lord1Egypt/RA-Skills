#!/usr/bin/env python3
"""memory-shield: snapshot — collect memory state into a self-contained digest.

Usage:
  python3 snapshot.py --memory <file_or_dir> [--out <dir>] [--label <name>]

Reads the given memory sources, masks secrets, and writes one dated digest
file that survives compaction. Secrets are replaced with 🔒 placeholders.
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

def is_binary(fp, chunk=8192):
    try:
        with open(fp, 'rb') as f:
            return b'\x00' in f.read(chunk)
    except OSError:
        return False

def collect(paths, root):
    lines = []
    seen = set()
    for ap in paths:
        ap = os.path.abspath(ap)
        if ap in seen:
            continue
        seen.add(ap)
        if os.path.isfile(ap):
            rel = os.path.relpath(ap, root) if root else os.path.basename(ap)
            lines.append(f"\n<!-- memory-shield file: {rel} -->\n")
            if is_binary(ap):
                lines.append("(binary, skipped)\n")
                continue
            try:
                with open(ap, 'r', encoding='utf-8', errors='replace') as f:
                    lines.extend(mask(l.rstrip()) for l in f)
            except OSError as e:
                lines.append(f"(unreadable: {e})\n")
        elif os.path.isdir(ap):
            for dp, _, fs in os.walk(ap):
                for fn in sorted(fs):
                    fp = os.path.join(dp, fn)
                    if os.path.abspath(fp) in seen:
                        continue
                    seen.add(os.path.abspath(fp))
                    rel = os.path.relpath(fp, root) if root else fp
                    lines.append(f"\n<!-- memory-shield file: {rel} -->\n")
                    if is_binary(fp):
                        lines.append("(binary, skipped)\n")
                        continue
                    try:
                        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                            lines.extend(mask(l.rstrip()) for l in f)
                    except OSError as e:
                        lines.append(f"(unreadable: {e})\n")
        else:
            lines.append(f"\n## {ap}\n(missing)\n")
    return lines

def main():
    ap = argparse.ArgumentParser(description="Memory snapshot (memory-shield)")
    ap.add_argument("--memory", nargs="+", required=True, help="file(s) or dir(s) to snapshot")
    ap.add_argument("--out", default="./memory_snapshots", help="output dir")
    ap.add_argument("--label", default="snapshot", help="snapshot label (sanitized)")
    args = ap.parse_args()

    paths = [os.path.abspath(m) for m in args.memory]
    root = os.path.commonpath(paths) if len(paths) > 1 else os.path.dirname(paths[0])
    os.makedirs(args.out, exist_ok=True)
    now = datetime.datetime.now(datetime.timezone.utc)
    ts = now.strftime("%Y-%m-%d_%H%M%S")
    label = re.sub(r'[^A-Za-z0-9_.-]+', '_', args.label).strip('._') or 'snapshot'
    out = os.path.join(args.out, f"{label}-{ts}.md")

    body = collect(paths, root)
    header = [
        f"# Memory snapshot — {label}",
        f"taken: {now.isoformat(timespec='seconds')}",
        f"sources: {', '.join(args.memory)}",
        "secrets: masked (🔒 placeholder)\n",
    ]
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(header) + "\n")
        f.write("\n".join(body) + "\n")
    print(f"✅ snapshot: {out} ({len(body)} lines)")

if __name__ == "__main__":
    main()
