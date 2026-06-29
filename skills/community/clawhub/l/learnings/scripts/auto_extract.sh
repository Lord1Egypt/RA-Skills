#!/bin/bash
# Auto-extract learnings from daily notes
# Usage: bash auto_extract.sh [--days 7] [--apply]
#
# Default is dry-run. Use --apply to actually log entries.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load shared config
source "$SKILL_DIR/lib/config.sh" 2>/dev/null || source "/root/.openclaw/workspace/skills/lib/config.sh"

WORKSPACE="${WORKSPACE:-/root/.openclaw/workspace}"
DAYS=7
DRY_RUN=true

while [[ $# -gt 0 ]]; do
  case $1 in
    --days) DAYS="$2"; shift 2;;
    --apply) DRY_RUN=false;;
    --dry-run) DRY_RUN=true;;
    *) shift;;
  esac
done

echo "=== Auto-Extract Learnings (last ${DAYS} days) ==="
if [ "$DRY_RUN" = true ]; then
  echo "[DRY RUN] No entries will be logged. Use --apply to log."
fi

python3 - "$WORKSPACE" "$DAYS" "$DRY_RUN" "$MEILI_HOST" "$MEILI_KEY" << 'PYEOF'
import json, os, glob, sys, subprocess, re, tempfile
from datetime import datetime, timedelta

workspace = sys.argv[1]
days = int(sys.argv[2])
dry_run = sys.argv[3] == "true"
ms_host = sys.argv[4]
ms_key = sys.argv[5]

daily_dir = f"{workspace}/memory"
cutoff = datetime.now() - timedelta(days=days)

# Patterns that indicate a learning-worthy event
LEARNING_PATTERNS = [
    r'(?:failed|error|broke|crashed|timeout|rejected|denied)',
    r'(?:fixed|resolved|patched|worked|solved)',
    r'(?:should|must|never|always|don\'t)\s+\w+',
    r'(?:lesson|learned|mistake|issue|problem|bug)',
    r'(?:version|v\d+\.\d+)',
    r'(?:prefer|preference|likes?|wants?)',
]

# Sensitive patterns to skip
SENSITIVE = [
    r'ghp_[A-Za-z0-9]{36}',
    r'ms-[A-Za-z0-9]{32}',
    r'AKIA[0-9A-Z]{16}',
    r'-----BEGIN',
    r'password\s*[:=]\s*\S+',
    r'api[_-]?key\s*[:=]\s*\S+',
    r'token\s*[:=]\s*\S+',
    r'secret\s*[:=]\s*\S+',
    r'credential\s*[:=]\s*\S+',
]

def contains_sensitive(text):
    for p in SENSITIVE:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False

def categorize(text):
    text_lower = text.lower()
    if any(w in text_lower for w in ["fail", "error", "broke", "crash", "timeout", "reject"]):
        return "failure"
    if any(w in text_lower for w in ["fix", "resolv", "patch", "solv"]):
        return "correction"
    if any(w in text_lower for w in ["version", "v1.", "v2.", "semver"]):
        return "version_rule"
    if any(w in text_lower for w in ["prefer", "like", "want", "should always", "must"]):
        return "preference"
    if any(w in text_lower for w in ["lesson", "learned", "mistake"]):
        return "learning"
    return "approach"

def is_learning_worthy(line):
    if len(line) < 20 or len(line) > 300:
        return False
    if contains_sensitive(line):
        return False
    for p in LEARNING_PATTERNS:
        if re.search(p, line, re.IGNORECASE):
            return True
    return False

def clean_line(line):
    line = line.strip()
    line = line.lstrip("-*•▪▸→ ").strip()
    line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
    line = re.sub(r'\*(.+?)\*', r'\1', line)
    line = re.sub(r'`(.+?)`', r'\1', line)
    return line

found = []
seen = set()

for fname in sorted(glob.glob(f"{daily_dir}/*.md")):
    try:
        file_date = datetime.strptime(os.path.basename(fname)[:10], "%Y-%m-%d")
    except:
        continue
    if file_date < cutoff:
        continue

    with open(fname, "r") as f:
        content = f.read()

    for line in content.split("\n"):
        clean = clean_line(line)
        if not clean:
            continue
        key = clean[:40].lower()
        if key in seen:
            continue
        if is_learning_worthy(clean):
            seen.add(key)
            found.append({
                "text": clean,
                "category": categorize(clean),
                "source": os.path.basename(fname),
                "date": file_date.strftime("%Y-%m-%d")
            })

print(f"Found {len(found)} potential learnings")

if found and not dry_run:
    logged = 0
    for item in found:
        doc_id = f"auto-{datetime.now().strftime('%Y%m%d')}-{hash(item['text']) % 10000:04d}"
        doc = [{
            "id": doc_id,
            "category": item["category"],
            "what_happened": item["text"],
            "fix": "(auto-extracted)",
            "context": f"From {item['source']}",
            "importance": 0.6,
            "tags": ["auto-extracted", f"category/{item['category']}", f"date/{item['date']}"],
            "date": item["date"],
            "source": "auto_extract"
        }]
        doc_file = tempfile.mktemp(prefix='learn-auto-', suffix='.json')
        os.chmod(doc_file, 0o600)
        with open(doc_file, "w") as f:
            json.dump(doc, f)
        subprocess.run([
            "curl", "-s", "-X", "POST",
            f"{ms_host}/indexes/learnings/documents",
            "-H", f"Authorization: Bearer {ms_key}",
            "-H", "Content-Type: application/json",
            "-d", f"@{doc_file}"
        ], capture_output=True)
        os.unlink(doc_file)
        logged += 1
    print(f"Logged {logged} learnings")
elif found and dry_run:
    print("\n[DRY RUN] Would log:")
    for item in found[:10]:
        print(f"  [{item['category']}] {item['text'][:80]}")
    print(f"\nRun with --apply to log these")
else:
    print("No new learnings found.")
PYEOF

echo "=== Done ==="
