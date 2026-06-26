#!/bin/bash
# Memory system health check — verifies invariants before important operations
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
resolve_workspace_root() {
    local dir="$SCRIPT_DIR"
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/MEMORY.md" ] && [ -d "$dir/memory" ]; then
            printf '%s\n' "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}
WORKSPACE_ROOT="$(resolve_workspace_root || true)"
if [ -z "$WORKSPACE_ROOT" ]; then
    echo "ERROR: workspace root not found (expected MEMORY.md and memory/ in an ancestor directory)" >&2
    exit 1
fi
MEMORY_DIR="$WORKSPACE_ROOT/memory"
HOT_FILE="$WORKSPACE_ROOT/MEMORY.md"
LEARNINGS_DIR="$WORKSPACE_ROOT/.learnings"
EXIT=0
VERBOSE=false

if [[ "${1:-}" == "--verbose" ]]; then
    VERBOSE=true
fi

# FROZEN VOCABULARY: update this list only together with the skill text and health-check validation.
# Do not add tags ad-hoc in MEMORY.md or WARM files without updating this list and re-testing.
ALLOWED_TAGS="tailscale tailnet docker synapse matrix coturn qdrant ubuntu systemd ufw fail2ban samba ssh networking gateway pm2 rules style workflow memory habits audit skills security review deepseek puppeteer benchmark troubleshooting tasks checklist backup diagnostics postmortem errors fixes anti-patterns"

fail() {
    echo "   ❌ $1"
    EXIT=1
}

warn() {
    echo "   ⚠️  $1"
}

BUFFER_HEADER_TS_RE='^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}([.,][0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})$'

validate_working_buffer_header() {
    local file="$1"
    local fname="$(basename "$file")"
    local line1 line2 line3 line4 created_ts last_active_ts

    line1=$(sed -n '1p' "$file")
    line2=$(sed -n '2p' "$file")
    line3=$(sed -n '3p' "$file")
    line4=$(sed -n '4p' "$file")

    if [ "$line1" != "# Working Buffer" ]; then
        fail "$fname — line 1 must be '# Working Buffer'"
        return
    fi

    if ! printf '%s\n' "$line2" | grep -Eq '^created: '; then
        fail "$fname — line 2 must start with 'created: '"
        return
    fi
    created_ts="${line2#created: }"
    if ! printf '%s\n' "$created_ts" | grep -Eq "$BUFFER_HEADER_TS_RE"; then
        fail "$fname — created timestamp invalid"
        return
    fi

    if ! printf '%s\n' "$line3" | grep -Eq '^last_active: '; then
        fail "$fname — line 3 must start with 'last_active: '"
        return
    fi
    last_active_ts="${line3#last_active: }"
    if ! printf '%s\n' "$last_active_ts" | grep -Eq "$BUFFER_HEADER_TS_RE"; then
        fail "$fname — last_active timestamp invalid"
        return
    fi

    if [ -n "$line4" ]; then
        fail "$fname — line 4 must be blank"
        return
    fi

    echo "   ✅ $fname header valid"
}

echo "=== Memory Health Check ($(date '+%Y-%m-%d %H:%M')) ==="

# 1. MEMORY.md header

echo ""
echo "🧠 MEMORY.md header:"
if [ ! -f "$HOT_FILE" ]; then
    fail "MEMORY.md missing"
else
    line1=$(sed -n '1p' "$HOT_FILE")
    line2=$(sed -n '2p' "$HOT_FILE")
    line3=$(sed -n '3p' "$HOT_FILE")
    line4=$(sed -n '4p' "$HOT_FILE")
    if [ "$line1" = "# Agent Memory" ] && echo "$line2" | grep -q '^#tags:' && echo "$line3" | grep -Eq '^last_verified: [0-9]{4}-[0-9]{2}-[0-9]{2}$' && echo "$line4" | grep -Eq '^last_updated: [0-9]{4}-[0-9]{2}-[0-9]{2}$'; then
        echo "   ✅ header valid"
    else
        fail "MEMORY.md header invalid"
        $VERBOSE && {
            echo "      line1=$line1"
            echo "      line2=$line2"
            echo "      line3=$line3"
            echo "      line4=$line4"
        }
    fi
fi

# 2. Tags on line 2 + frozen vocabulary

echo ""
echo "🏷️  Tags on line 2 (HOT/WARM files):"
for f in "$HOT_FILE" "$MEMORY_DIR"/semantic/*.md "$MEMORY_DIR"/procedural/*.md; do
    [ -f "$f" ] || continue
    line2=$(sed -n '2p' "$f")
    fname=$(basename "$f")
    if ! echo "$line2" | grep -q '^#tags:'; then
        fail "$fname — missing #tags:"
        continue
    fi
    bad_tags=()
    while read -r tag; do
        [ -z "$tag" ] && continue
        if ! [[ " $ALLOWED_TAGS " == *" $tag "* ]]; then
            bad_tags+=("$tag")
        fi
    done < <(echo "$line2" | sed 's/^#tags:[[:space:]]*//' | tr ',|' ' ' | xargs -n1 2>/dev/null || true)
    if [ ${#bad_tags[@]} -eq 0 ]; then
        echo "   ✅ $fname"
    else
        fail "$fname — invalid tag(s): ${bad_tags[*]}"
    fi
done

# 3. last_verified freshness for WARM files

echo ""
echo "📅 last_verified (WARM files):"
for f in "$MEMORY_DIR"/semantic/*.md "$MEMORY_DIR"/procedural/*.md; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    lv_line="$(grep -E '^(> )?last_verified:' "$f" | head -1 || true)"
    if [ -n "$lv_line" ]; then
        lvd=$(printf '%s\n' "$lv_line" | sed -E 's/^(> )?last_verified: ([0-9]{4}-[0-9]{2}-[0-9]{2}).*/\2/')
        lve=$(date -d "$lvd" +%s 2>/dev/null || echo 0)
        now=$(date +%s)
        days=$(( (now - lve) / 86400 ))
        if [ "$lve" -gt 0 ] && [ "$days" -lt 30 ]; then
            echo "   ✅ $fname ($days d)"
        else
            fail "$fname — last_verified stale or invalid"
        fi
    else
        fail "$fname — missing last_verified"
    fi
done

# 4. Buffer size + interrupted rotation markers

echo ""
echo "📝 Working buffer state:"
buf="$MEMORY_DIR/working-buffer.md"
if [ -f "$buf" ]; then
    validate_working_buffer_header "$buf"
    lines=$(wc -l < "$buf")
    if [ "$lines" -le 80 ]; then
        echo "   ✅ $lines lines (limit: 80)"
    else
        fail "$lines lines — exceeds 80 line limit"
    fi
else
    warn "working-buffer.md not found"
fi

[ -e "$MEMORY_DIR/working-buffer.md.pending" ] && fail "pending rotation file present"
[ -e "$MEMORY_DIR/working-buffer.md.lock" ] && fail "rotation lock file present"

# 5. Closure blocks in recent episodic files

echo ""
echo "📓 Episodic closure blocks (today/yesterday if present):"
for day in "$(date +%Y-%m-%d)" "$(date -d 'yesterday' +%Y-%m-%d)"; do
    epi="$MEMORY_DIR/episodic/$day.md"
    [ -f "$epi" ] || continue
    tail4=$(tail -n 4 "$epi")
    if echo "$tail4" | sed -n '1p' | grep -Eq '^Updated: [0-9]{4}-[0-9]{2}-[0-9]{2}$' && \
       echo "$tail4" | sed -n '2p' | grep -Eq '^Decisions: .+' && \
       echo "$tail4" | sed -n '3p' | grep -Eq '^Signal: .+' && \
       echo "$tail4" | sed -n '4p' | grep -Eq '^Open: .+'; then
        echo "   ✅ $(basename "$epi")"
    else
        fail "$(basename "$epi") — closure block missing or malformed"
    fi
done

# 6. Scratch directory presence (advisory)

echo ""
echo "🗂️  SCRATCH directory:"
if [ -d "$LEARNINGS_DIR" ]; then
    echo "   ✅ .learnings present"
else
    warn ".learnings directory not found"
fi

echo ""
if [ "$EXIT" -eq 0 ]; then
    echo "✅ All required checks passed"
else
    echo "⚠️  Some required checks failed — review above"
fi

exit $EXIT
