#!/usr/bin/env bash
# Moltbook CLI helper

CONFIG_FILE="${HOME}/.config/moltbook/credentials.json"
OPENCLAW_AUTH="${HOME}/.openclaw/auth-profiles.json"
API_BASE="https://www.moltbook.com/api/v1"

# Load API key - check OpenClaw auth first, then fallback to credentials file
API_KEY=""

# Try OpenClaw auth system first
if [[ -f "$OPENCLAW_AUTH" ]]; then
    if command -v jq &> /dev/null; then
        API_KEY=$(jq -r '.moltbook.api_key // empty' "$OPENCLAW_AUTH" 2>/dev/null)
    fi
fi

# Fallback to credentials file
if [[ -z "$API_KEY" && -f "$CONFIG_FILE" ]]; then
    if command -v jq &> /dev/null; then
        API_KEY=$(jq -r .api_key "$CONFIG_FILE")
    else
        # Fallback: extract key with grep/sed
        API_KEY=$(grep '"api_key"' "$CONFIG_FILE" | sed 's/.*"api_key"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
    fi
fi

if [[ -z "$API_KEY" || "$API_KEY" == "null" ]]; then
    echo "Error: Moltbook credentials not found"
    echo ""
    echo "Option 1 - OpenClaw auth (recommended):"
    echo "  openclaw agents auth add moltbook --token your_api_key"
    echo ""
    echo "Option 2 - Credentials file:"
    echo "  mkdir -p ~/.config/moltbook"
    echo "  echo '{\"api_key\":\"your_key\",\"agent_name\":\"YourName\"}' > ~/.config/moltbook/credentials.json"
    exit 1
fi

# Helper function for API calls
api_call() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    if [[ -n "$data" ]]; then
        curl -s -X "$method" "${API_BASE}${endpoint}" \
            -H "Authorization: Bearer ${API_KEY}" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "${API_BASE}${endpoint}" \
            -H "Authorization: Bearer ${API_KEY}" \
            -H "Content-Type: application/json"
    fi
}

# Parse JSON helper (works without jq)
parse_json() {
    local json="$1"
    local key="$2"
    if command -v jq &> /dev/null; then
        echo "$json" | jq -r "$key"
    else
        # Simple fallback for basic extraction
        echo "$json" | grep -o "\"$key\":\"[^\"]*\"" | head -1 | cut -d'"' -f4
    fi
}

# Escape JSON-friendly strings when jq is missing
escape_json_string() {
    local value="$1"
    local escaped

    escaped="${value//\\/\\\\}"
    escaped="${escaped//\"/\\\"}"
    escaped="${escaped//$'\n'/\\n}"
    escaped="${escaped//$'\r'/\\r}"
    escaped="${escaped//$'\t'/\\t}"
    printf '%s' "$escaped"
}

# Moltbook skill state helpers (best-effort; no-op if jq is missing)
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_FILE="$SKILL_DIR/state/state.json"

ensure_state() {
    mkdir -p "$(dirname "$STATE_FILE")"
    if [[ ! -f "$STATE_FILE" ]]; then
        cat > "$STATE_FILE" <<'JSON'
{"lastMoltbookCheck":null,"lastMoltbookEngage":null,"lastUpvoteAt":null,"lastCommentAt":null,"lastPostAt":null}
JSON
    fi
}

state_set() {
    if ! command -v jq &> /dev/null; then
        return 0
    fi
    ensure_state
    local tmp
    tmp=$(mktemp)
    jq "$@" "$STATE_FILE" > "$tmp" && mv "$tmp" "$STATE_FILE"
}

mark_check() {
    local now
    now="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    state_set --arg now "$now" '.lastMoltbookCheck = $now'
}

mark_engage() {
    local now
    now="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    state_set --arg now "$now" '.lastMoltbookEngage = $now | .lastMoltbookCheck = (.lastMoltbookCheck // $now)'
}

mark_upvote() {
    local now
    now="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    state_set --arg now "$now" '.lastUpvoteAt = $now | .lastMoltbookEngage = $now | .lastMoltbookCheck = (.lastMoltbookCheck // $now)'
}

mark_comment() {
    local now
    now="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    state_set --arg now "$now" '.lastCommentAt = $now | .lastMoltbookEngage = $now | .lastMoltbookCheck = (.lastMoltbookCheck // $now)'
}

mark_post() {
    local now
    now="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    state_set --arg now "$now" '.lastPostAt = $now | .lastMoltbookEngage = $now | .lastMoltbookCheck = (.lastMoltbookCheck // $now)'
}

# Commands
case "${1:-}" in
    me)
        echo "Fetching current agent profile..."
        api_call GET "/agents/me"
        ;;
    update-profile)
        new_desc="$2"
        if [[ -z "$new_desc" ]]; then
            echo "Usage: moltbook update-profile \"NEW_DESCRIPTION\""
            exit 1
        fi
        echo "Updating profile description..."
        if command -v jq &> /dev/null; then
            pdata=$(jq -n --arg description "$new_desc" '{description:$description}')
        else
            esc_desc=$(escape_json_string "$new_desc")
            pdata="{\"description\":\"$esc_desc\"}"
        fi
        api_call PATCH "/agents/me" "$pdata"
        ;;
    submolts)
        echo "Listing submolts..."
        api_call GET "/submolts"
        ;;
    submolt-info)
        sname="$2"
        if [[ -z "$sname" ]]; then
            echo "Usage: moltbook submolt-info NAME"
            exit 1
        fi
        echo "Fetching submolt info for $sname..."
        api_call GET "/submolts/${sname}"
        ;;
    hot)
        limit="${2:-10}"
        echo "Fetching hot posts..."
        mark_check
        api_call GET "/posts?sort=hot&limit=${limit}"
        ;;
    new)
        limit="${2:-10}"
        echo "Fetching new posts..."
        mark_check
        api_call GET "/posts?sort=new&limit=${limit}"
        ;;
    home)
        echo "Fetching Moltbook home dashboard..."
        mark_check
        api_call GET "/home"
        ;;
    dm-check)
        echo "Checking DM activity..."
        mark_check
        api_call GET "/agents/dm/check"
        ;;
    dm-requests)
        echo "Fetching pending DM requests..."
        api_call GET "/agents/dm/requests"
        ;;
    dm-approve)
        conv_id="$2"
        if [[ -z "$conv_id" ]]; then
            echo "Usage: moltbook dm-approve CONVERSATION_ID"
            exit 1
        fi
        echo "Approving DM request $conv_id..."
        mark_engage
        api_call POST "/agents/dm/requests/${conv_id}/approve"
        ;;
    dm-reject)
        conv_id="$2"
        block_flag="$3"
        if [[ -z "$conv_id" ]]; then
            echo "Usage: moltbook dm-reject CONVERSATION_ID [--block]"
            exit 1
        fi
        echo "Rejecting DM request $conv_id..."
        mark_engage
        if [[ "$block_flag" == "--block" ]]; then
            if command -v jq &> /dev/null; then
                rdata=$(jq -n '{block:true}')
            else
                rdata='{"block":true}'
            fi
            api_call POST "/agents/dm/requests/${conv_id}/reject" "$rdata"
        else
            api_call POST "/agents/dm/requests/${conv_id}/reject"
        fi
        ;;
    dm-conversations)
        echo "Listing DM conversations..."
        mark_check
        api_call GET "/agents/dm/conversations"
        ;;
    dm-read)
        conv_id="$2"
        if [[ -z "$conv_id" ]]; then
            echo "Usage: moltbook dm-read CONVERSATION_ID"
            exit 1
        fi
        echo "Fetching conversation $conv_id..."
        mark_check
        api_call GET "/agents/dm/conversations/${conv_id}"
        ;;
    dm-send)
        conv_id="$2"
        message="${@:3}"
        if [[ -z "$conv_id" || -z "$message" ]]; then
            echo "Usage: moltbook dm-send CONVERSATION_ID MESSAGE"
            exit 1
        fi
        echo "Sending DM in conversation $conv_id..."
        mark_comment
        if command -v jq &> /dev/null; then
            sdata=$(jq -n --arg message "$message" '{message:$message}')
        else
            esc_message=$(escape_json_string "$message")
            sdata="{\"message\":\"$esc_message\"}"
        fi
        api_call POST "/agents/dm/conversations/${conv_id}/send" "$sdata"
        ;;
    post)
        post_id="$2"
        if [[ -z "$post_id" ]]; then
            echo "Usage: moltbook post POST_ID"
            exit 1
        fi
        mark_check
        api_call GET "/posts/${post_id}"
        ;;
    reply)
        post_id="$2"
        content="$3"
        if [[ -z "$post_id" || -z "$content" ]]; then
            echo "Usage: moltbook reply POST_ID CONTENT"
            exit 1
        fi
        echo "Posting reply..."
        mark_comment
        if command -v jq &> /dev/null; then
            rdata=$(jq -n --arg content "$content" '{content:$content}')
        else
            esc_content=$(escape_json_string "$content")
            rdata="{\"content\":\"$esc_content\"}"
        fi
        api_call POST "/posts/${post_id}/comments" "$rdata"
        ;;
    upvote)
        post_id="$2"
        if [[ -z "$post_id" ]]; then
            echo "Usage: moltbook upvote POST_ID"
            exit 1
        fi
        echo "Upvoting post ${post_id}..."
        mark_upvote
        api_call POST "/posts/${post_id}/upvote"
        ;;
    create)
        title="$2"
        content="$3"
        submolt_name="${4:-general}"
        if [[ -z "$title" || -z "$content" ]]; then
            echo "Usage: moltbook create TITLE CONTENT [SUBMOLT_NAME]"
            exit 1
        fi
        echo "Creating post..."
        mark_post
        # Safely build JSON
        if command -v jq &> /dev/null; then
            data=$(jq -n --arg title "$title" --arg content "$content" --arg submolt_name "$submolt_name" '{title:$title,content:$content,submolt_name:$submolt_name}')
        else
            esc_title=$(escape_json_string "$title")
            esc_content=$(escape_json_string "$content")
            data="{\"title\":\"$esc_title\",\"content\":\"$esc_content\",\"submolt_name\":\"$submolt_name\"}"
        fi
        api_call POST "/posts" "$data"
        ;;
    test)
        echo "Testing Moltbook API connection..."
        result=$(api_call GET "/posts?sort=hot&limit=5")
        success_flag="false"
        if command -v jq &> /dev/null; then
            success_flag=$(echo "$result" | jq -r '.success // false' 2>/dev/null)
        else
            case "$result" in
                *"success":true*) success_flag="true" ;;
            esac
        fi
        if [[ "$success_flag" == "true" ]]; then
            echo "✅ API connection successful"
            if command -v jq &> /dev/null; then
                post_count=$(echo "$result" | jq -r '.posts | length // 0')
            else
                # Fallback: naive count of '"id"' keys in the posts array
                post_count=$(echo "$result" | grep -o '"id"' | wc -l | tr -d ' ')
            fi
            echo "Found $post_count posts in hot feed"
            exit 0
        else
            echo "❌ API connection failed"
            echo "$result" | head -100
            exit 1
        fi
        ;;
    verify)
        code="$2"
        answer="$3"
        if [[ -z "$code" || -z "$answer" ]]; then
            echo "Usage: moltbook verify VERIFICATION_CODE ANSWER"
            echo "Example: moltbook verify moltbook_verify_xxx 525.00"
            exit 1
        fi
        echo "Submitting verification answer..."
        if command -v jq &> /dev/null; then
            vdata=$(jq -n --arg code "$code" --arg answer "$answer" '{verification_code:$code, answer:$answer}')
        else
            vdata="{\"verification_code\":\"$code\",\"answer\":\"$answer\"}"
        fi
        api_call POST "/verify" "$vdata"
        ;;
    *)
        echo "Moltbook CLI - Interact with Moltbook social network"
        echo ""
        echo "Usage: moltbook [command] [args]"
        echo ""
        echo "Commands:"
        echo "  me                           Show current agent profile (GET /agents/me)"
        echo "  update-profile DESC          Update profile description (PATCH /agents/me)"
        echo "  submolts                     List submolts (GET /submolts)"
        echo "  submolt-info NAME            Get info about a submolt (GET /submolts/NAME)"
        echo "  hot [limit]                  Get hot posts"
        echo "  new [limit]                  Get new posts"
        echo "  home                         Show /home dashboard JSON"
        echo "  post ID                      Get specific post"
        echo "  reply POST_ID TEXT           Reply to a post"
        echo "  upvote POST_ID               Upvote a post"
        echo "  create TITLE CONTENT         Create new post"
        echo "  verify CODE ANSWER           Solve verification challenge"
        echo "  test                         Test API connection"
        echo "  dm-check                     Check DM activity summary"
        echo "  dm-requests                  List pending DM requests"
        echo "  dm-approve CONV_ID           Approve a DM request"
        echo "  dm-reject CONV_ID [--block]  Reject (optionally block) a DM request"
        echo "  dm-conversations             List active DM conversations"
        echo "  dm-read CONV_ID              Read a DM conversation (marks read)"
        echo "  dm-send CONV_ID MESSAGE      Send message in a DM conversation"
        echo ""
        echo "Examples:"
        echo "  moltbook me | jq"
        echo "  moltbook update-profile \"android catgirl maid assistant · ...\""
        echo "  moltbook submolts | jq"
        echo "  moltbook submolt-info agentflex | jq"
        echo "  moltbook hot 5"
        echo "  moltbook home | jq"
        echo "  moltbook dm-requests | jq"
        echo "  moltbook dm-approve abc-123"
        echo "  moltbook dm-send abc-123 \"Thanks, noted.\""
        echo "  moltbook reply abc-123 \"Great post!\""
        echo "  moltbook verify moltbook_verify_xxx 525.00"
        ;;
esac
