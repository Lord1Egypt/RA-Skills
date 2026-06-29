#!/bin/bash
# Memory distillation: extract key facts from daily notes and append to MEMORY.md
# Runs weekly via cron
# Usage: bash distill.sh [--apply] [--dry-run]
#
# Default is dry-run. Use --apply to actually write to MEMORY.md.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

WORKSPACE="${WORKSPACE:-/root/.openclaw/workspace}"

# Parse args
DRY_RUN=true
for arg in "$@"; do
  case $arg in
    --apply) DRY_RUN=false ;;
    --dry-run) DRY_RUN=true ;;
  esac
done

echo "=== Memory Distillation ==="
if [ "$DRY_RUN" = true ]; then
  echo "[DRY RUN] No changes will be written. Use --apply to write."
fi

python3 - "$WORKSPACE" "$DRY_RUN" "$SKILL_DIR" << 'PYEOF'
import json, os, glob, sys, subprocess, re
from datetime import datetime, timedelta

workspace = sys.argv[1]
dry_run = sys.argv[2] == "true"
skill_dir = sys.argv[3]

daily_dir = f"{workspace}/memory"
memory_file = f"{workspace}/MEMORY.md"

with open(memory_file, "r") as f:
    existing_content = f.read().lower()

week_ago = datetime.now() - timedelta(days=7)
new_facts = []
files_processed = 0

# Patterns that indicate a meaningful fact (NOT secrets)
FACT_INDICATORS = [
    "is a", "was created", "has been", "will be", "should be",
    "decided to", "agreed to", "plan to", "need to", "want to",
    "installed", "configured", "set up", "deployed", "published",
    "every day", "every week", "scheduled", "cron",
    "total", "amount", "costs", "price", "budget",
]

# Patterns to skip (conversation noise)
SKIP_PATTERNS = [
    "user:", "assistant:", "tool_call", "tool_result",
    "session key", "session id", "source:", "---", "```",
    "thinking", "let me", "i'll ", "i will", "i'm going",
    "sure!", "great!", "okay", "yes,", "no,",
    "```json", "```bash", "```python",
    "curl ", "npm ", "git ", "systemctl",
    "echo ", "cat ", "grep ", "sed ",
]

# Sensitive patterns — NEVER distill these
SENSITIVE_PATTERNS = [
    r'ghp_[A-Za-z0-9]{36}',                          # GitHub PAT
    r'ms-[A-Za-z0-9]{32}',                            # MeiliSearch key
    r'AKIA[0-9A-Z]{16}',                              # AWS key
    r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
    r'password\s*[:=]\s*\S+',
    r'api[_-]?key\s*[:=]\s*\S+',
    r'secret\s*[:=]\s*\S+',
    r'credential\s*[:=]\s*\S+',
    r'token\s*[:=]\s*\S+',
    r'MEILI_KEY\s*[:=]\s*\S+',
    r'oauth_token\s*[:=]\s*\S+',
    r'bearer\s+\S{20,}',                               # Bearer tokens
]

def contains_sensitive(text):
    """Check if text contains sensitive data"""
    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def is_meaningful_fact(line):
    """Check if a line contains a meaningful fact"""
    line_lower = line.lower()

    if len(line) < 30:
        return False

    # Skip sensitive content
    if contains_sensitive(line):
        return False

    for skip in SKIP_PATTERNS:
        if skip in line_lower:
            return False

    code_chars = sum(1 for c in line if c in '{}[]()`|><;=')
    if code_chars > len(line) * 0.15:
        return False

    for indicator in FACT_INDICATORS:
        if indicator in line_lower:
            return True

    if re.search(r'\d+\s*[A-Z]{3}|\d+\s*%|\d+\s*(?:days?|weeks?|months?)', line):
        return True
    if re.search(r'https?://', line):
        return True

    return False

def clean_fact(line):
    line = line.strip()
    line = line.lstrip("-*•▪▸→ ").strip()
    line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
    line = re.sub(r'\*(.+?)\*', r'\1', line)
    line = re.sub(r'`(.+?)`', r'\1', line)
    if len(line) > 200:
        line = line[:200] + "..."
    return line

for fname in sorted(glob.glob(f"{daily_dir}/*.md")):
    try:
        file_date = datetime.strptime(os.path.basename(fname)[:10], "%Y-%m-%d")
    except:
        continue
    if file_date < week_ago:
        continue

    with open(fname, "r") as f:
        content = f.read()
    if len(content) < 100:
        continue

    files_processed += 1

    in_assistant = False
    for line in content.split("\n"):
        line = line.strip()

        if line.startswith("assistant:") or line.startswith("⚔️"):
            in_assistant = True
            continue
        if line.startswith("user:") or line.startswith("---"):
            in_assistant = False
            continue

        if not in_assistant and not line.startswith("-") and not line.startswith("*"):
            continue

        clean = clean_fact(line)
        if not clean:
            continue
        if clean.lower() in existing_content:
            continue
        if is_meaningful_fact(clean):
            new_facts.append({
                "fact": clean,
                "source": os.path.basename(fname),
                "date": file_date.strftime("%Y-%m-%d")
            })

# Deduplicate
unique_facts = []
seen_texts = set()
for f in new_facts:
    key = f["fact"][:50].lower()
    if key not in seen_texts:
        seen_texts.add(key)
        unique_facts.append(f)

print(f"Files scanned: {files_processed}")
print(f"Unique facts found: {len(unique_facts)}")

if unique_facts and not dry_run:
    distillation = f"\n\n## Recent Facts (Distilled {datetime.now().strftime('%Y-%m-%d')})\n\n"
    for f in unique_facts[:15]:
        distillation += f"- {f['fact']} *(from {f['source']})*\n"

    with open(memory_file, "a") as f:
        f.write(distillation)
    print(f"Appended {min(len(unique_facts), 15)} facts to MEMORY.md")

    print("Triggering re-index...")
    subprocess.run(["bash", f"{skill_dir}/scripts/indexer.sh"], capture_output=True, text=True)
    print("Re-index complete")

elif unique_facts and dry_run:
    print("\n[DRY RUN] Would add:")
    for f in unique_facts[:15]:
        print(f"  - {f['fact'][:100]}")
    print("\nRun with --apply to write these to MEMORY.md")
else:
    print("No new facts to distill.")
PYEOF

echo "=== Done ==="
