#!/bin/bash
# =============================================================================
# LinkedIn Analytics Extract Script
# =============================================================================
# PURPOSE:
#   Extract LinkedIn creator analytics (impressions, engagement, posts) via
#   OpenClaw browser automation and save structured JSON for reporting.
#
# REQUIREMENTS:
#   - OpenClaw browser running (openclaw browser start)
#   - LinkedIn session active (logged in)
#   - jq installed for JSON processing
#   - Discord webhook configured (optional, for failure alerts)
#
# USAGE:
#   ./analytics-extract.sh [--days 7]
#   ./analytics-extract.sh 30    # Extract last 30 days
#
# OUTPUT:
#   - JSON: system/linkedin-analytics/YYYY-MM-DD.json
#   - Log:  system/logs/linkedin-analytics.log
#   - Posts: system/linkedin-analytics/posts-posted/*.json
#
# AUTHOR: Renato MB (via OpenClaw Agent)
# VERSION: 2.0.0
# LAST UPDATED: 2026-05-07
# =============================================================================

set -euo pipefail

# Configuration
DAYS="${1:-7}"
OUTPUT_DIR="system/linkedin-analytics"
REPORTS_DIR="system/linkedin-reports"
POSTS_DIR="$OUTPUT_DIR/posts-posted"
WORKSPACE_DIR="$HOME/vaults/openclaw/workspace"
LOG_FILE="${OPENCLAW_LOG_FILE:-$WORKSPACE_DIR/logs/scripts.log}"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
JSON_FILE="$OUTPUT_DIR/$DATE.json"

# Browser tab label for single-tab pattern
LINKEDIN_TAB_LABEL="linkedin-script-session"

# Baseline tabs (captured before any browser actions)
BASELINE_TABS=""

# Retry configuration
MAX_RETRIES=3
RETRY_DELAYS=(2 4 8)  # Exponential backoff: 2s, 4s, 8s

# Discord webhook (optional - set in .env or leave empty)
DISCORD_WEBHOOK="${DISCORD_WEBHOOK:-}"

# =============================================================================
# Browser Cleanup Function - Single Tab Pattern
# =============================================================================

capture_baseline_tabs() {
    log_info "📋 Capturing baseline tabs before script actions..."
    BASELINE_TABS=$(openclaw browser tabs 2>/dev/null | grep -oE '\[t[0-9]+' | sed 's/\[//g' | sort -u || echo "")
    local baseline_count=$(echo "$BASELINE_TABS" | grep -c . 2>/dev/null || echo "0")
    log_info "Baseline tabs captured: $baseline_count"
}

cleanup_browser_tabs() {
    log_info "🧹 Cleaning up browser tabs (trap called)..."
    
    # PRIMARY: Close the script's dedicated tab if it exists
    if [[ -n "$LINKEDIN_TAB_LABEL" ]]; then
        log_info "  → Closing script tab: $LINKEDIN_TAB_LABEL"
        openclaw browser close "$LINKEDIN_TAB_LABEL" 2>/dev/null || true
    fi
    
    # SECONDARY: Close any other NEW tabs (safety net for retry leftovers)
    CURRENT_TABS=$(openclaw browser tabs 2>/dev/null | grep -oE '\[t[0-9]+' | sed 's/\[//g' | sort -u || echo "")
    
    if [[ -z "$CURRENT_TABS" ]]; then
        log_info "No tabs to clean"
        return 0
    fi
    
    # Find NEW tabs (opened during script execution)
    NEW_TABS=$(comm -13 <(echo "$BASELINE_TABS") <(echo "$CURRENT_TABS") 2>/dev/null || echo "")
    
    if [[ -z "$NEW_TABS" ]]; then
        log_info "No additional tabs to close (baseline preserved)"
        return 0
    fi
    
    local new_tab_count=$(echo "$NEW_TABS" | grep -c . 2>/dev/null || echo "0")
    log_info "Closing $new_tab_count additional tab(s) from retries..."
    
    # Close each stray tab
    echo "$NEW_TABS" | while read TAB_ID; do
        if [[ -n "$TAB_ID" ]]; then
            log_info "  → Closing stray tab: $TAB_ID"
            openclaw browser close "$TAB_ID" 2>/dev/null || true
        fi
    done
    
    # Small delay for closes to complete
    sleep 1
    
    # Verify cleanup
    FINAL_TABS=$(openclaw browser tabs 2>/dev/null | grep -oE '\[t[0-9]+' | sed 's/\[//g' | sort -u || echo "")
    REMAINING_NEW=$(comm -13 <(echo "$BASELINE_TABS") <(echo "$FINAL_TABS") 2>/dev/null | grep -c . 2>/dev/null || echo "0")
    
    if [[ "$REMAINING_NEW" -gt 0 ]]; then
        log_warn "⚠️  $REMAINING_NEW tab(s) still open (may be browser system tabs or race condition)"
    else
        log_info "✅ Script tab closed + all stray tabs cleaned - pre-existing tabs preserved"
    fi
}

# Capture baseline BEFORE any browser actions (CRITICAL: must be before first browser command)
capture_baseline_tabs

# Set trap to cleanup on exit (success or failure)
trap cleanup_browser_tabs EXIT

# =============================================================================
# Logging Functions
# =============================================================================

log() {
    local level="$1"
    local message="$2"
    echo "[$TIMESTAMP] [$level] $message" >> "$LOG_FILE"
    echo "[$level] $message"
}

log_info() { log "INFO" "$1"; }
log_warn() { log "WARN" "$1"; }
log_error() { log "ERROR" "$1"; }

# =============================================================================
# Discord Alert Function
# =============================================================================

send_discord_alert() {
    local message="$1"
    if [[ -n "$DISCORD_WEBHOOK" ]]; then
        curl -s -X POST "$DISCORD_WEBHOOK" \
            -H "Content-Type: application/json" \
            -d "{\"content\": \"🚨 LinkedIn Analytics Alert: $message\"}" \
            >> /dev/null 2>&1 || true
    fi
    log_warn "Discord alert sent: $message"
}

# =============================================================================
# Retry Logic with Exponential Backoff
# =============================================================================

retry_command() {
    local attempt=1
    local cmd="$1"
    local description="$2"
    
    while [[ $attempt -le $MAX_RETRIES ]]; do
        log_info "Attempt $attempt/$MAX_RETRIES: $description"
        
        if eval "$cmd"; then
            log_info "Success on attempt $attempt"
            return 0
        fi
        
        if [[ $attempt -lt $MAX_RETRIES ]]; then
            local delay=${RETRY_DELAYS[$((attempt-1))]}
            log_warn "Failed. Retrying in ${delay}s..."
            sleep $delay
        fi
        
        ((attempt++))
    done
    
    log_error "All $MAX_RETRIES attempts failed: $description"
    return 1
}

# =============================================================================
# Main Script
# =============================================================================

# Create directories
mkdir -p "$OUTPUT_DIR" "$REPORTS_DIR" "$POSTS_DIR"

log_info "═══════════════════════════════════════════"
log_info "📊 LINKEDIN ANALYTICS EXTRACTION STARTED"
log_info "═══════════════════════════════════════════"
log_info "Período: últimos $DAYS dias"
log_info "Output: $JSON_FILE"

# Step 1: Verify browser is running
log_info "1. Verificando browser..."
if ! openclaw browser status 2>&1 | grep -q 'running: true'; then
    log_warn "Browser não está rodando. Iniciando..."
    openclaw browser start
    sleep 3
    # Recapture baseline after browser start (new tabs from browser startup)
    capture_baseline_tabs
fi
log_info "✅ Browser verificado"

# Step 2: Verify LinkedIn session - use single tab pattern
log_info "2. Verificando sessão LinkedIn..."

# Open single tab for entire script session
openclaw browser open --label "$LINKEDIN_TAB_LABEL" https://www.linkedin.com/feed/
sleep 3

SNAPSHOT=$(openclaw browser snapshot --targetId "$LINKEDIN_TAB_LABEL" --limit 50 2>&1)
if echo "$SNAPSHOT" | grep -q "Entrar\|Cadastre-se"; then
    log_error "❌ NÃO logado no LinkedIn!"
    send_discord_alert "Falha na extração: Não logado no LinkedIn"
    
    cat << EOF
❌ NÃO logado no LinkedIn!

Ação necessária:
1. Navegue até linkedin.com no browser do OpenClaw
2. Faça login
3. Rode este script novamente

Comando: openclaw browser navigate https://www.linkedin.com/
EOF
    exit 1
fi
log_info "✅ Logado no LinkedIn"

# Step 3: Navigate to analytics in SAME tab (human-like delay)
log_info "3. Navegando para analytics..."
DELAY=$((RANDOM % 5 + 3))
sleep $DELAY

openclaw browser navigate --targetId "$LINKEDIN_TAB_LABEL" https://www.linkedin.com/analytics/creator/
sleep 5

# Step 4: Human-like scroll in current tab
log_info "4. Scroll humano..."
for i in 1 2 3; do
    openclaw browser evaluate --targetId "$LINKEDIN_TAB_LABEL" --fn "window.scrollBy(0, 300)" 2>/dev/null || log_warn "Scroll $i failed (non-critical)"
    sleep 1
done

# Step 5: Navigate to recent activity in SAME tab (no new tab created)
log_info "5. Navegando para recent activity..."
openclaw browser navigate --targetId "$LINKEDIN_TAB_LABEL" https://www.linkedin.com/in/renatomaluhy/recent-activity/all/
sleep 5

# Human-like scroll for posts in current tab
log_info "6. Scroll para carregar posts..."
for i in 1 2 3; do
    openclaw browser evaluate --targetId "$LINKEDIN_TAB_LABEL" --fn "window.scrollBy(0, 500)" 2>/dev/null || log_warn "Post scroll $i failed (non-critical)"
    sleep 2
done

# Step 6: Capture snapshot for extraction from current tab
log_info "7. Capturando snapshot..."
SNAPSHOT=$(openclaw browser snapshot --targetId "$LINKEDIN_TAB_LABEL" --limit 200 2>&1)

# Step 7: Extract metrics from snapshot
log_info "8. Extraindo métricas..."

# Extract impressions (e.g., "887 impressões") - macOS compatible (no -P flag)
TOTAL_IMPRESSIONS=$(echo "$SNAPSHOT" | grep -oE '[0-9]+ impressões' | head -1 | grep -oE '[0-9]+' || echo "0")
[[ -z "$TOTAL_IMPRESSIONS" ]] && TOTAL_IMPRESSIONS=0

# Extract reactions (e.g., "42 reações")
TOTAL_REACTIONS=$(echo "$SNAPSHOT" | grep -oE '[0-9]+ reações' | head -1 | grep -oE '[0-9]+' || echo "0")
[[ -z "$TOTAL_REACTIONS" ]] && TOTAL_REACTIONS=0

# Extract comments (e.g., "12 comentários")
TOTAL_COMMENTS=$(echo "$SNAPSHOT" | grep -oE '[0-9]+ comentários' | head -1 | grep -oE '[0-9]+' || echo "0")
[[ -z "$TOTAL_COMMENTS" ]] && TOTAL_COMMENTS=0

# Calculate total engagements
TOTAL_ENGAGEMENTS=$((TOTAL_REACTIONS + TOTAL_COMMENTS))

# Calculate engagement rate
if [[ $TOTAL_IMPRESSIONS -gt 0 ]]; then
    ENGAGEMENT_RATE=$(echo "scale=2; ($TOTAL_ENGAGEMENTS * 100) / $TOTAL_IMPRESSIONS" | bc)
else
    ENGAGEMENT_RATE=0
fi

# Step 8: Extract individual posts
log_info "9. Extraindo posts individuais..."

# Use browser evaluate to extract post data as JSON from current tab
POSTS_JSON=$(openclaw browser evaluate --targetId "$LINKEDIN_TAB_LABEL" --fn '
() => {
    const posts = [];
    const postElements = document.querySelectorAll("[data-id]");
    postElements.forEach((el, idx) => {
        if (idx < 10) {  // Limit to first 10 posts
            posts.push({
                post_id: el.getAttribute("data-id") || "unknown_" + idx,
                impressions: parseInt(el.textContent.match(/\\d+ impressões/)?.[0] || "0"),
                reactions: parseInt(el.textContent.match(/\\d+ reações/)?.[0] || "0"),
                comments: parseInt(el.textContent.match(/\\d+ comentários/)?.[0] || "0")
            });
        }
    });
    return JSON.stringify(posts);
}
' 2>&1 || echo "[]")

# Save individual posts to posts-posted/
log_info "Debug: POSTS_JSON length = ${#POSTS_JSON}"
if [[ -n "$POSTS_JSON" && "$POSTS_JSON" != "[]" ]]; then
    log_info "✅ Posts encontrados, salvando..."
    POSTS_ARRAY=$(echo "$POSTS_JSON" | jq -c '.[]' 2>/dev/null || echo "")
    if [[ -n "$POSTS_ARRAY" ]]; then
        while IFS= read -r post; do
            if [[ -n "$post" ]]; then
                POST_ID=$(echo "$post" | jq -r '.post_id' 2>/dev/null || echo "")
                if [[ -n "$POST_ID" && "$POST_ID" != "null" ]]; then
                    echo "$post" | jq "." > "$POSTS_DIR/$DATE-$POST_ID.json" 2>/dev/null || log_warn "Failed to save post $POST_ID"
                fi
            fi
        done <<< "$POSTS_ARRAY"
        log_info "✅ Posts salvos em: $POSTS_DIR/"
    else
        log_warn "Nenhum post no array JSON"
    fi
else
    log_warn "Nenhum post extraído (POSTS_JSON empty or [])"
fi

# Step 10: Generate main JSON file
log_info "10. Gerando JSON principal..."

cat > "$JSON_FILE" << EOF
{
  "extraction_date": "$DATE",
  "extraction_timestamp": "$TIMESTAMP",
  "period": "Últimos $DAYS dias",
  "extraction_method": "browser_automation",
  "status": "success",
  "posts_count": $(echo "$POSTS_JSON" | jq 'length' 2>/dev/null || echo "0"),
  "posts": $POSTS_JSON,
  "summary": {
    "total_impressions": $TOTAL_IMPRESSIONS,
    "total_reactions": $TOTAL_REACTIONS,
    "total_comments": $TOTAL_COMMENTS,
    "total_engagements": $TOTAL_ENGAGEMENTS,
    "engagement_rate": $ENGAGEMENT_RATE,
    "comment_rate": $(echo "scale=2; ($TOTAL_COMMENTS * 100) / $TOTAL_IMPRESSIONS" | bc 2>/dev/null || echo "0"),
    "follower_change": "pending",
    "profile_views": "pending"
  },
  "notes": "Extração completa com retry logic e logging"
}
EOF

# Validate JSON
if ! jq '.' "$JSON_FILE" > /dev/null 2>&1; then
    log_error "❌ JSON inválido gerado!"
    send_discord_alert "Falha na extração: JSON inválido"
    exit 1
fi

log_info "═══════════════════════════════════════════"
log_info "✅ EXTRAÇÃO COMPLETA!"
log_info "═══════════════════════════════════════════"
log_info "📄 Dados salvos em: $JSON_FILE"
log_info "📄 Posts salvos em: $POSTS_DIR/"
log_info ""
log_info "Próximo passo: Rodar analytics-report.sh pra gerar report em markdown"

# Browser cleanup will run automatically via EXIT trap

exit 0
