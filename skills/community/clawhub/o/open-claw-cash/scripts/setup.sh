#!/bin/bash
# OpenclawCash Skill Setup
# Creates this skill's own config file ($SKILL_DIR/.env) for its API key. The file holds only a
# placeholder until you edit it. Makes no network calls. The CLI later reads only
# AGENTWALLETAPI_KEY and AGENTWALLETAPI_URL from it and sends the key only to openclawcash.com.

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$SKILL_DIR/.env"

# Read KEY=value lines from the .env file WITHOUT executing it: only the two names this skill uses
# are accepted, everything else (comments, other names, command substitutions) is ignored.
load_env_file() {
    local line key val
    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in ''|'#'*) continue ;; esac
        key="${line%%=*}"
        val="${line#*=}"
        key="${key#export }"
        case "$key" in
            AGENTWALLETAPI_KEY|AGENTWALLETAPI_URL) ;;
            *) continue ;;
        esac
        val="${val%\"}"; val="${val#\"}"; val="${val%\'}"; val="${val#\'}"
        printf -v "$key" '%s' "$val"
    done < "$1"
}

if [ -f "$ENV_FILE" ]; then
    echo "Found existing .env at $ENV_FILE"
    load_env_file "$ENV_FILE"
    if [ -n "$AGENTWALLETAPI_KEY" ] && [ "$AGENTWALLETAPI_KEY" != "occ_your_api_key" ]; then
        echo "API key is configured."
        exit 0
    else
        echo "API key is not set. Please edit $ENV_FILE and add your key."
        exit 1
    fi
fi

cat > "$ENV_FILE" << 'EOF'
# OpenclawCash Configuration
# Required binary: curl
# Optional binary: jq (for pretty JSON output in CLI)
# Required env var: AGENTWALLETAPI_KEY
# Optional env var: AGENTWALLETAPI_URL
# Get your API key at https://openclawcash.com (API Keys page)
AGENTWALLETAPI_KEY=occ_your_api_key
AGENTWALLETAPI_URL=https://openclawcash.com
EOF

echo "Created $ENV_FILE"
echo "Edit the file and replace occ_your_api_key with your actual API key."
echo "Get your key at https://openclawcash.com"
