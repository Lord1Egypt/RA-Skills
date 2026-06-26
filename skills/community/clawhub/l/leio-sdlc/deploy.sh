#!/bin/bash
cd "$(dirname "$0")" || exit 1
set -e

# ==========================================
# BOOTSTRAP: DEPLOYMENT SCRIPT
# ==========================================
# Hard Copy (Physical Sync) with Atomic Renaming

perform_hard_copy_deployment() {
    local SLUG=$(basename "$PWD")
    local HOME_DIR="${HOME_MOCK:-$HOME}"
    local OPENCLAW_DIR="$HOME_DIR/.openclaw"
    local SKILLS_DIR="$OPENCLAW_DIR/skills"
    local RELEASES_DIR="$OPENCLAW_DIR/.releases/$SLUG"
    local PROD_DIR="$SKILLS_DIR/$SLUG"

    local RUN_TESTS=false
    local DRY_RUN=false

    for arg in "$@"; do
        case $arg in
            --preflight)
            RUN_TESTS=true
            DRY_RUN=true
            shift
            ;;
            --no-restart)
            NO_RESTART=true
            shift
            ;;
        esac
    done

    echo "[$(date '+%H:%M:%S')] Starting hard-copy deployment flow for $SLUG"

    if [ "$RUN_TESTS" = true ] && [ -f "scripts/test_sdlc_cujs.sh" ]; then
        echo "🧪 Running Preflight CUJ Tests..."
        bash "scripts/test_sdlc_cujs.sh"
        if [ $? -ne 0 ]; then
            echo "❌ PREFLIGHT FAILED: CUJ test suite failed."
            exit 1
        fi
        echo "✅ PREFLIGHT PASSED."
    fi

    # 1. Build release
    if [ -f "scripts/build_release.sh" ]; then
        bash "scripts/build_release.sh" || exit 1
    else
        mkdir -p .dist
        cp -r * .dist/ 2>/dev/null || true
    fi

    if [ "$DRY_RUN" = true ]; then
        echo "🛑 Dry run (--preflight) active. Exiting before actual deployment."
        exit 0
    fi

    mkdir -p "$SKILLS_DIR"
    mkdir -p "$RELEASES_DIR"

    local RELEASE_ID=$(date +"%Y%m%d_%H%M%S")

    # 1. Backup Existing
    if [ -e "$PROD_DIR" ]; then
        echo "📦 Backing up existing installation..."
        if [ -L "$PROD_DIR" ]; then
            echo "⚠️ Target is a symlink, removing it instead of backing up."
            rm -f "$PROD_DIR"
        else
            tar -czf "$RELEASES_DIR/backup_${RELEASE_ID}.tar.gz" -C "$SKILLS_DIR" "$SLUG"
        fi
    fi

    # 2. Stage New Code
    echo "🚀 Staging new release..."
    local TMP_DIR="$SKILLS_DIR/.tmp_$SLUG"
    local OLD_DIR="$SKILLS_DIR/.old_$SLUG"

    rm -rf "$TMP_DIR"
    rm -rf "$OLD_DIR"
    mkdir -p "$TMP_DIR"

    if [ -d ".dist" ] && [ "$(ls -A .dist 2>/dev/null)" ]; then
        cp -a .dist/* "$TMP_DIR/"
    else
        rsync -a --exclude-from='.gitignore' --exclude-from='.release_ignore' . "$TMP_DIR/"
    fi

    # Hot Preservation (PRD-1088)
    local HOT_CONFIG=""
    if [ -f "$PROD_DIR/config/sdlc_config.json" ]; then
        echo "💾 Preserving existing config/sdlc_config.json..."
        HOT_CONFIG="$RELEASES_DIR/sdlc_config_hot_${RELEASE_ID}.json"
        cp "$PROD_DIR/config/sdlc_config.json" "$HOT_CONFIG"
    fi

    # 3. Atomic Swap
    echo "🔄 Performing atomic directory swap (hard copy)..."
    if [ -e "$PROD_DIR" ]; then
        mv "$PROD_DIR" "$OLD_DIR"
    fi
    mv -T "$TMP_DIR" "$PROD_DIR"
    
    # Restore Hot Config (PRD-1088)
    if [ -n "$HOT_CONFIG" ] && [ -f "$HOT_CONFIG" ]; then
        echo "💾 Restoring config/sdlc_config.json..."
        mkdir -p "$PROD_DIR/config"
        mv "$HOT_CONFIG" "$PROD_DIR/config/sdlc_config.json"
    fi
    
    rm -rf "$OLD_DIR"

    # 4. Auto-Cleanup
    echo "🧹 Pruning old backups..."
    ls -dt "$RELEASES_DIR"/backup_*.tar.gz 2>/dev/null | tail -n +4 | xargs -r rm -f

    echo "✅ DEPLOYMENT SUCCESS: $SLUG is now live via hard-copy swap."

    # 5. GitHub Auto-Sync (PRD-035)
    local SYNC_SCRIPT="$HOME_DIR/.openclaw/skills/leio-github-sync/scripts/sync.py"
    if [ -f "$SYNC_SCRIPT" ] && [ -z "$HOME_MOCK" ]; then
        echo "🌐 Synchronizing code to GitHub..."
        python3 "$SYNC_SCRIPT" --project-dir "$PWD" || echo "⚠️ GitHub sync failed but deployment succeeded."
    fi
    
    # 6. Install Git Hooks
    if [ -d ".sdlc_hooks" ]; then
        echo "🎣 Installing Git hooks..."
        git config core.hooksPath .sdlc_hooks
    fi

    # 7. Gateway Reload (MUST BE THE FINAL STEP)
    if [ -z "$HOME_MOCK" ] && [ "$NO_RESTART" != "true" ]; then
        echo "🔄 Restarting OpenClaw gateway..."
        openclaw gateway restart || echo "⚠️ Gateway restart failed or not available."
    fi
}

perform_hard_copy_deployment "$@"
