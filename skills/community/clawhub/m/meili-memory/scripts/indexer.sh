#!/bin/bash
# Tiered memory indexer for MeiliSearch
# Creates three indexes: core, working, archive
# Usage: bash indexer.sh [--full]
#
# --full requires --force: bash indexer.sh --full --force

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load shared config
source "$SKILL_DIR/lib/config.sh" 2>/dev/null || source "/root/.openclaw/workspace/skills/lib/config.sh"

WORKSPACE="${WORKSPACE:-/root/.openclaw/workspace}"
# Topic detection replaces synonyms.json for tagging

# Parse args
FULL_REINDEX=false
FORCE=false
for arg in "$@"; do
  case $arg in
    --full) FULL_REINDEX=true ;;
    --force) FORCE=true ;;
  esac
done

# Safety: --full requires --force
if [ "$FULL_REINDEX" = true ] && [ "$FORCE" != true ]; then
  echo "ERROR: --full reindex requires --force flag."
  echo "This will DELETE and recreate all indexes (core, working, archive)."
  echo "Usage: bash indexer.sh --full --force"
  exit 1
fi

# Secure temp file helper
tmpfile() {
  local f
  f=$(mktemp /tmp/meili-index.XXXXXX)
  chmod 600 "$f"
  echo "$f"
}

cleanup_files=()
cleanup() {
  for f in "${cleanup_files[@]}"; do
    rm -f "$f" 2>/dev/null
  done
}
trap cleanup EXIT

# Wait for MeiliSearch
for i in $(seq 1 10); do
  if curl -s "${MEILI_HOST}/health" > /dev/null 2>&1; then break; fi
  sleep 1
done

echo "=== MeiliSearch Tiered Memory Indexer ==="

# --- Create/recreate indexes ---
for TIER in core working archive; do
  if [ "$FULL_REINDEX" = true ]; then
    echo "Deleting ${TIER} index..."
    curl -s -X DELETE "${MEILI_HOST}/indexes/${TIER}" \
      -H "Authorization: Bearer ${MEILI_KEY}" > /dev/null 2>&1 || true
  fi

  # Create index if not exists
  curl -s -X POST "${MEILI_HOST}/indexes" \
    -H "Authorization: Bearer ${MEILI_KEY}" \
    -H "Content-Type: application/json" \
    -d "{\"uid\":\"${TIER}\",\"primaryKey\":\"id\"}" > /dev/null 2>&1 || true

  sleep 1

  case $TIER in
    core)
      RANKING='["words","typo","proximity","attribute","sort","exactness"]'
      ;;
    working)
      RANKING='["words","typo","proximity","sort","attribute","exactness"]'
      ;;
    archive)
      RANKING='["words","typo","proximity","attribute","sort","exactness"]'
      ;;
  esac

  curl -s -X PATCH "${MEILI_HOST}/indexes/${TIER}/settings" \
    -H "Authorization: Bearer ${MEILI_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
      \"searchableAttributes\": [\"text\", \"source\", \"file\", \"category\", \"tags\"],
      \"filterableAttributes\": [\"source\", \"category\", \"file\", \"importance\", \"date\", \"tags\", \"tier\"],
      \"rankingRules\": ${RANKING},
      \"typoTolerance\": {
        \"enabled\": true,
        \"minWordSizeForTypos\": { \"oneTypo\": 3, \"twoTypos\": 6 }
      }
    }" > /dev/null

  sleep 0.5
done

echo "Indexes configured: core, working, archive"

# --- Generate documents ---
CORE_FILE=$(tmpfile)
WORKING_FILE=$(tmpfile)
ARCHIVE_FILE=$(tmpfile)
cleanup_files+=("$CORE_FILE" "$WORKING_FILE" "$ARCHIVE_FILE")

python3 - "$WORKSPACE" "$CORE_FILE" "$WORKING_FILE" "$ARCHIVE_FILE" << 'PYEOF'
import json, os, glob, sys, re
from datetime import datetime, timedelta

workspace = sys.argv[1]
core_file = sys.argv[2]
working_file = sys.argv[3]
archive_file = sys.argv[4]

# Topic detection for tagging during indexing
# Maps patterns to topic tags — used instead of synonyms.json
TOPIC_RULES = [
    (["debt", "loan", "liabilit", "payment", "owe"], "topic/finance"),
    (["project", "repo", "repository", "application", "service"], "topic/projects"),
    (["identity", "profile", "personal", "about"], "topic/identity"),
    (["finance", "budget", "expense", "income", "savings", "net worth"], "topic/finance"),
    (["work", "career", "internship", "coding", "development", "programming"], "topic/work"),
    (["schedule", "cron", "daily", "weekly", "reminder", "calendar"], "topic/schedule"),
    (["skill", "plugin", "installed", "extension"], "topic/skills"),
    (["server", "gateway", "service", "daemon", "linux", "hosting"], "topic/infrastructure"),
    (["auth", "login", "token", "credential", "oauth", "permission"], "topic/auth"),
]

def detect_topics(text):
    text_lower = text.lower()
    topics = []
    for patterns, topic in TOPIC_RULES:
        for pattern in patterns:
            if pattern in text_lower:
                if topic not in topics:
                    topics.append(topic)
                break
    return topics

def auto_tag(text, source, file):
    tags = []
    text_lower = text.lower()

    if "debt" in text_lower or "loan" in text_lower or "liabilit" in text_lower:
        tags.append("finance/debts")
    if "project" in text_lower or "repository" in text_lower or "repo" in text_lower:
        tags.append("project")
    if "budget" in text_lower or "expense" in text_lower or "income" in text_lower:
        tags.append("finance")
    if "cron" in text_lower or "schedule" in text_lower or "calendar" in text_lower:
        tags.append("schedule")
    if "profile" in text_lower or "identity" in text_lower:
        tags.append("identity")
    if "typescript" in text_lower or "npm" in text_lower or "node" in text_lower or "coding" in text_lower:
        tags.append("work/development")
    if "meilisearch" in text_lower:
        tags.append("infrastructure/meilisearch")
    if "skill" in text_lower and ("install" in text_lower or "publish" in text_lower):
        tags.append("skills")

    if source == "MEMORY.md":
        tags.append("tier/core")
    else:
        tags.append("tier/daily")

    return list(set(tags))

def get_tier(date_str):
    try:
        doc_date = datetime.strptime(date_str[:10], "%Y-%m-%d")
        days_old = (datetime.now() - doc_date).days
        if days_old <= 7:
            return "working"
        else:
            return "archive"
    except:
        return "archive"

def contains_sensitive(text):
    """Check if text contains sensitive data that should not be indexed"""
    import re
    sensitive_patterns = [
        r'ghp_[A-Za-z0-9]{36}',          # GitHub PAT
        r'ms-[A-Za-z0-9]{32}',            # MeiliSearch key
        r'AKIA[0-9A-Z]{16}',              # AWS key
        r'-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
        r'password\s*[:=]\s*\S+',
        r'token\s*[:=]\s*\S+',
        r'api[_-]?key\s*[:=]\s*\S+',
        r'secret\s*[:=]\s*\S+',
        r'credential\s*[:=]\s*\S+',
    ]
    for pattern in sensitive_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

core_docs = []
working_docs = []
archive_docs = []

# MEMORY.md → always core
with open(f"{workspace}/MEMORY.md", "r") as f:
    content = f.read()

sections = []
current = []
for line in content.split("\n"):
    if line.startswith("## ") and current:
        sections.append("\n".join(current))
        current = [line]
    else:
        current.append(line)
if current:
    sections.append("\n".join(current))

for i, section in enumerate(sections):
    if not section.strip():
        continue
    # Skip sections that are mostly sensitive data
    if contains_sensitive(section):
        continue
    tags = auto_tag(section, "MEMORY.md", "MEMORY.md")
    tags.append(f"section/{i}")
    for topic in detect_topics(section):
        tags.append(topic)

    core_docs.append({
        "id": f"core-mem-{i}",
        "text": section.strip(),
        "source": "MEMORY.md",
        "file": "MEMORY.md",
        "category": "long-term-memory",
        "importance": 0.95,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tags": list(set(tags)),
        "tier": "core"
    })

# Daily notes → working or archive based on age
daily_dir = f"{workspace}/memory"
if os.path.exists(daily_dir):
    for fname in sorted(glob.glob(f"{daily_dir}/*.md")):
        with open(fname, "r") as f:
            content = f.read()

        date_str = fname.split("/")[-1][:10]
        tier = get_tier(date_str)

        chunk_size = 1500
        chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
            # Skip chunks containing sensitive data
            if contains_sensitive(chunk):
                continue
            tags = auto_tag(chunk, "daily-note", fname)
            tags.append(f"date/{date_str}")
            for topic in detect_topics(chunk):
                tags.append(topic)

            doc = {
                "id": f"{tier}-{date_str.replace('-','')}-{i}",
                "text": chunk.strip(),
                "source": "daily-note",
                "file": os.path.basename(fname),
                "category": "session-note",
                "importance": 0.6 if tier == "working" else 0.3,
                "date": date_str,
                "tags": list(set(tags)),
                "tier": tier
            }

            if tier == "working":
                working_docs.append(doc)
            else:
                archive_docs.append(doc)

with open(core_file, "w") as f:
    json.dump(core_docs, f)
with open(working_file, "w") as f:
    json.dump(working_docs, f)
with open(archive_file, "w") as f:
    json.dump(archive_docs, f)

print(f"Core: {len(core_docs)} | Working: {len(working_docs)} | Archive: {len(archive_docs)}")
PYEOF

# --- Push to MeiliSearch ---
for TIER in core working archive; do
  DOC_FILE=$(mktemp /tmp/meili-tier.XXXXXX)
  chmod 600 "$DOC_FILE"
  cleanup_files+=("$DOC_FILE")
  case $TIER in
    core) cp "$CORE_FILE" "$DOC_FILE" ;;
    working) cp "$WORKING_FILE" "$DOC_FILE" ;;
    archive) cp "$ARCHIVE_FILE" "$DOC_FILE" ;;
  esac

  if [ ! -f "$DOC_FILE" ]; then continue; fi

  DOC_COUNT=$(python3 -c "import json; print(len(json.load(open('${DOC_FILE}'))))" 2>/dev/null || echo 0)
  if [ "$DOC_COUNT" = "0" ]; then continue; fi

  BATCH_FILE=$(tmpfile)
  cleanup_files+=("$BATCH_FILE")

  # Write python code to temp file to avoid heredoc issues
  PUSH_SCRIPT=$(tmpfile)
  cleanup_files+=("$PUSH_SCRIPT")
  cat > "$PUSH_SCRIPT" << 'PYEOF'
import json, subprocess, time
import sys

ms_host = sys.argv[1]
ms_key = sys.argv[2]
tier = sys.argv[3]
doc_file = sys.argv[4]
batch_file = sys.argv[5]

with open(doc_file) as f:
    docs = json.load(f)

for i in range(0, len(docs), 20):
    batch = docs[i:i+20]
    with open(batch_file, "w") as f:
        json.dump(batch, f)
    subprocess.run([
        "curl", "-s", "-X", "POST",
        f"{ms_host}/indexes/{tier}/documents",
        "-H", f"Authorization: Bearer {ms_key}",
        "-H", "Content-Type: application/json",
        "-d", f"@{batch_file}"
    ], capture_output=True, text=True)
    time.sleep(0.3)

print(f"  {tier}: {len(docs)} docs indexed")
PYEOF

  python3 "$PUSH_SCRIPT" "$MEILI_HOST" "$MEILI_KEY" "$TIER" "$DOC_FILE" "$BATCH_FILE"
done

# --- Print stats ---
echo ""
echo "=== Index Stats ==="
for TIER in core working archive; do
  STATS=$(curl -s "${MEILI_HOST}/indexes/${TIER}/stats" -H "Authorization: Bearer ${MEILI_KEY}" 2>/dev/null)
  COUNT=$(echo "$STATS" | python3 -c "import json,sys; print(json.load(sys.stdin).get('numberOfDocuments','?'))" 2>/dev/null || echo "?")
  echo "  ${TIER}: ${COUNT} documents"
done
echo ""
echo "Done. Use search.sh to query: bash search.sh 'your query'"
