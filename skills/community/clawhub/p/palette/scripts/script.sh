#!/usr/bin/env bash
set -euo pipefail

# palette — skill script
# Powered by BytesAgain | bytesagain.com | hello@bytesagain.com

DATA_DIR="${HOME}/.palette"
mkdir -p "$DATA_DIR"

show_help() {
    cat << 'HELPEOF'
palette — command-line tool

Commands:
  create         Run create operation
  random         Run random operation
  complementary  Run complementary operation
  analogous      Run analogous operation
  triadic        Run triadic operation
  export         Run export operation
  preview        Run preview operation
  list           Run list operation
  save           Run save operation
  config         Run config operation
  stats      Show statistics
  export     Export data (json|csv|txt)
  search     Search across entries
  recent     Show recent entries
  status     Show current status
  help       Show this help message
  version    Show version number

Data stored in: ~/.palette/
HELPEOF
}

show_version() {
    echo "palette v1.0.0 — Powered by BytesAgain"
}

cmd_stats() {
    echo "=== palette Statistics ==="
    local total=0
    for f in "$DATA_DIR"/*.log; do
        [ -f "$f" ] || continue
        local name=$(basename "$f" .log)
        local c=$(wc -l < "$f" 2>/dev/null || echo 0)
        total=$((total + c))
        echo "  $name: $c entries"
    done
    echo "  Total: $total entries"
    echo "  Data size: $(du -sh "$DATA_DIR" 2>/dev/null | cut -f1 || echo 'N/A')"
    echo "  Since: $(head -1 "$DATA_DIR/history.log" 2>/dev/null | cut -d'|' -f1 || echo 'N/A')"
}

cmd_export() {
    local fmt="${1:-json}"
    local out="palette-export.$fmt"
    case "$fmt" in
        json)
            echo "[" > "$out"
            local first=1
            for f in "$DATA_DIR"/*.log; do
                [ -f "$f" ] || continue
                while IFS= read -r line; do
                    [ $first -eq 1 ] && first=0 || echo "," >> "$out"
                    local ts=$(echo "$line" | cut -d'|' -f1)
                    local cmd=$(echo "$line" | cut -d'|' -f2)
                    local data=$(echo "$line" | cut -d'|' -f3-)
                    printf '  {"timestamp":"%s","command":"%s","data":"%s"}' "$ts" "$cmd" "$data" >> "$out"
                done < "$f"
            done
            echo "" >> "$out"
            echo "]" >> "$out"
            ;;
        csv)
            echo "timestamp,command,data" > "$out"
            for f in "$DATA_DIR"/*.log; do
                [ -f "$f" ] || continue
                while IFS= read -r line; do
                    echo "$line" | awk -F'|' '{printf "\"%s\",\"%s\",\"%s\"\n", $1, $2, $3}' >> "$out"
                done < "$f"
            done
            ;;
        txt)
            > "$out"
            for f in "$DATA_DIR"/*.log; do
                [ -f "$f" ] || continue
                echo "--- $(basename "$f" .log) ---" >> "$out"
                cat "$f" >> "$out"
                echo "" >> "$out"
            done
            ;;
        *)
            echo "Unknown format: $fmt (use json, csv, or txt)"
            return 1
            ;;
    esac
    echo "Exported to $out ($(wc -c < "$out" 2>/dev/null || echo 0) bytes)"
}

cmd_search() {
    local term="${1:-}"
    [ -z "$term" ] && { echo "Usage: palette search <term>"; return 1; }
    echo "=== Search: $term ==="
    local found=0
    for f in "$DATA_DIR"/*.log; do
        [ -f "$f" ] || continue
        local matches=$(grep -i "$term" "$f" 2>/dev/null || true)
        if [ -n "$matches" ]; then
            echo "--- $(basename "$f" .log) ---"
            echo "$matches"
            found=$((found + 1))
        fi
    done
    [ $found -eq 0 ] && echo "No matches found."
}

cmd_recent() {
    local n="${1:-10}"
    echo "=== Recent $n entries ==="
    for f in "$DATA_DIR"/*.log; do
        [ -f "$f" ] || continue
        tail -n "$n" "$f" 2>/dev/null
    done | sort -t'|' -k1 | tail -n "$n"
}

cmd_status() {
    echo "=== palette Status ==="
    echo "  Entries: $(cat "$DATA_DIR"/*.log 2>/dev/null | wc -l || echo 0)"
    echo "  Disk: $(du -sh "$DATA_DIR" 2>/dev/null | cut -f1 || echo 'N/A')"
    local last=$(tail -1 "$DATA_DIR/history.log" 2>/dev/null || echo "never")
    echo "  Last activity: $last"
}

# Main
CMD="${1:-help}"
shift 2>/dev/null || true

case "$CMD" in
    create)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|create|${*}" >> "$DATA_DIR/create.log"
        local total=$(wc -l < "$DATA_DIR/create.log" 2>/dev/null || echo 0)
        echo "[palette] create recorded (entry #$total)"
        ;;
    random)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|random|${*}" >> "$DATA_DIR/random.log"
        local total=$(wc -l < "$DATA_DIR/random.log" 2>/dev/null || echo 0)
        echo "[palette] random recorded (entry #$total)"
        ;;
    complementary)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|complementary|${*}" >> "$DATA_DIR/complementary.log"
        local total=$(wc -l < "$DATA_DIR/complementary.log" 2>/dev/null || echo 0)
        echo "[palette] complementary recorded (entry #$total)"
        ;;
    analogous)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|analogous|${*}" >> "$DATA_DIR/analogous.log"
        local total=$(wc -l < "$DATA_DIR/analogous.log" 2>/dev/null || echo 0)
        echo "[palette] analogous recorded (entry #$total)"
        ;;
    triadic)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|triadic|${*}" >> "$DATA_DIR/triadic.log"
        local total=$(wc -l < "$DATA_DIR/triadic.log" 2>/dev/null || echo 0)
        echo "[palette] triadic recorded (entry #$total)"
        ;;
    export)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|export|${*}" >> "$DATA_DIR/export.log"
        local total=$(wc -l < "$DATA_DIR/export.log" 2>/dev/null || echo 0)
        echo "[palette] export recorded (entry #$total)"
        ;;
    preview)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|preview|${*}" >> "$DATA_DIR/preview.log"
        local total=$(wc -l < "$DATA_DIR/preview.log" 2>/dev/null || echo 0)
        echo "[palette] preview recorded (entry #$total)"
        ;;
    list)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|list|${*}" >> "$DATA_DIR/list.log"
        local total=$(wc -l < "$DATA_DIR/list.log" 2>/dev/null || echo 0)
        echo "[palette] list recorded (entry #$total)"
        ;;
    save)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|save|${*}" >> "$DATA_DIR/save.log"
        local total=$(wc -l < "$DATA_DIR/save.log" 2>/dev/null || echo 0)
        echo "[palette] save recorded (entry #$total)"
        ;;
    config)
        local ts=$(date '+%Y-%m-%d %H:%M')
        echo "$ts|config|${*}" >> "$DATA_DIR/config.log"
        local total=$(wc -l < "$DATA_DIR/config.log" 2>/dev/null || echo 0)
        echo "[palette] config recorded (entry #$total)"
        ;;
    stats)
        cmd_stats
        ;;
    export)
        cmd_export "$@"
        ;;
    search)
        cmd_search "$@"
        ;;
    recent)
        cmd_recent "$@"
        ;;
    status)
        cmd_status
        ;;
    help|--help|-h)
        show_help
        ;;
    version|--version|-v)
        show_version
        ;;
    *)
        echo "Unknown command: $CMD"
        echo "Run 'palette help' for usage."
        exit 1
        ;;
esac
