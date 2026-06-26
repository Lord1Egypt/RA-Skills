#!/bin/bash

# OSNK Trainer Skill - Main Script
# OSK/OSNK Practice with Performance Tracking

COMMAND="$1"
shift

# Get script directory for skill-embedded question bank
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Dynamic path detection with local fallback (skill folder + workspace)
if [ -n "$OPENCLAW_WORKSPACE" ]; then
    DATA_DIR="$OPENCLAW_WORKSPACE/memory"
    KB_DIR="$OPENCLAW_WORKSPACE/knowledge"
    REPO_DIR="$OPENCLAW_WORKSPACE"
elif [ -d "/root/.openclaw/workspace/memory" ]; then
    DATA_DIR="/root/.openclaw/workspace/memory"
    KB_DIR="/root/.openclaw/workspace/knowledge"
    REPO_DIR="/root/.openclaw/workspace"
else
    DATA_DIR="./memory"
    KB_DIR="./knowledge"
    REPO_DIR="."
fi

mkdir -p "$DATA_DIR"

# Question bank sources (priority: local > skill folder > GitHub fallback)
KB_REPO="https://raw.githubusercontent.com/jrrqd/osnk-question-bank/master"

get_kb_file() {
    local file="$1"
    # 1. Check workspace knowledge folder
    if [ -f "$KB_DIR/$file" ]; then
        cat "$KB_DIR/$file"
    # 2. Check skill folder (embedded)
    elif [ -f "$SCRIPT_DIR/$file" ]; then
        cat "$SCRIPT_DIR/$file"
    # 3. Fallback to GitHub
    else
        curl -s "$KB_REPO/$file" 2>/dev/null || echo ""
    fi
}

# Files
STATS_FILE="$DATA_DIR/osnk-stats.json"
PROGRESS_FILE="$DATA_DIR/osnk-progress.json"
CONFIG_FILE="$DATA_DIR/osnk-config.json"

init_stats() {
    if [ ! -f "$STATS_FILE" ]; then
        echo '{"total_attempted":0,"correct":0,"wrong":0,"by_category":{},"by_year":{},"sessions":0,"last_session":""}' > "$STATS_FILE"
    fi
}

get_random_question() {
    year="$1"
    category="$2"
    
    if [ -z "$year" ]; then
        # Get random files from local or skill folder
        local files=$(find "$KB_DIR" -name "osk-*.md" -o -name "osnk-*.md" 2>/dev/null | shuf | head -3)
        if [ -z "$files" ]; then
            files=$(find "$SCRIPT_DIR" -maxdepth 1 -name "osk-*.md" -o -name "osnk-*.md" 2>/dev/null | shuf | head -3)
        fi
        if [ -z "$files" ]; then
            files="osk-2018.md osk-2019.md osnk-2024.md"
        fi
        for f in $files; do
            if [ -f "$f" ]; then
                grep -A10 "^## " "$f" | head -20 || echo "No questions found"
            fi
        done
    else
        if [ -f "$KB_DIR/osk-$year.md" ]; then
            shuf -n 1 "$KB_DIR/osk-$year.md" | head -15
        elif [ -f "$SCRIPT_DIR/osk-$year.md" ]; then
            shuf -n 1 "$SCRIPT_DIR/osk-$year.md" | head -15
        elif [ -f "$KB_DIR/osnk-$year.md" ]; then
            shuf -n 1 "$KB_DIR/osnk-$year.md" | head -15
        elif [ -f "$SCRIPT_DIR/osnk-$year.md" ]; then
            shuf -n 1 "$SCRIPT_DIR/osnk-$year.md" | head -15
        else
            curl -s "$KB_REPO/osk-$year.md" | head -15 || echo "Year $year not found"
        fi
    fi
}

show_stats() {
    init_stats
    total=$(cat "$STATS_FILE" 2>/dev/null | grep -o '"total_attempted":[0-9]*' | cut -d: -f2)
    correct=$(cat "$STATS_FILE" 2>/dev/null | grep -o '"correct":[0-9]*' | cut -d: -f2)
    wrong=$(cat "$STATS_FILE" 2>/dev/null | grep -o '"wrong":[0-9]*' | cut -d: -f2)
    
    if [ -z "$total" ] || [ "$total" = "0" ]; then
        echo "📊 OSNK Training Stats"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Belum ada sesi latihan!"
        echo ""
        echo "Mulai: openclaw, give me 5 questions"
    else
        accuracy=$((correct * 100 / total))
        echo "📊 OSNK Training Stats"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📝 Total: $total | ✅ $correct | ❌ $wrong"
        echo "📈 Accuracy: $accuracy%"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    fi
}

show_help() {
    echo "🧠 OSNK Trainer - Latihan OSNK Informatika"
    echo ""
    echo "📝 Contoh perintah:"
    echo "  openclaw, give me 5 questions"
    echo "  openclaw, 10 graph questions"
    echo "  openclaw, random osk 2018"
    echo ""
    echo "⏱️ Speed Run:"
    echo "  openclaw, start speed run 30 minutes"
    echo ""
    echo "📊 Stats:"
    echo "  openclaw, show my stats"
    echo "  openclaw, my progress"
    echo ""
    echo "📚 Included: 700+ questions OSK/OSNK (2006-2025)"
}

case "$COMMAND" in
    "stats"|"performance"|"my-stats")
        show_stats
        ;;
        
    "random"|"questions"|"give")
        num="${1:-5}"
        topic="$*"
        
        echo "🎯 $num random questions:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        for i in $(seq 1 $num); do
            echo ""
            echo "Question $i:"
            get_random_question "" "" | head -8
        done
        echo ""
        echo "Ketik: openclaw, answer [your_answer]"
        ;;
        
    "speed"|"speedrun"|"timed")
        duration="${1:-30}"
        echo "⏱️ Speed Run - $duration menit!"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        get_random_question "" "" | head -10
        ;;
        
    "explain"|"what"|"define")
        topic="$*"
        case "$topic" in
            *dynamic*|*dp*)
                echo "📖 Dynamic Programming"
                echo "Teknik optimasi: pecah masalah jadi subproblem"
                echo "- Memoization (top-down)"
                echo "- Tabulation (bottom-up)"
                ;;
            *graph*|*bfs*|*dfs*)
                echo "📖 Graph Traversal"
                echo "BFS: Level by level (Queue)"
                echo "DFS: Deep first (Stack)"
                ;;
            *)
                echo "📚 Gunakan: openclaw, explain [topik]"
                ;;
        esac
        ;;
        
    "help"|"--help"|"-h")
        show_help
        ;;
        
    *)
        echo "🧠 OSNK Trainer"
        echo "Ketik: openclaw, help"
        ;;
esac