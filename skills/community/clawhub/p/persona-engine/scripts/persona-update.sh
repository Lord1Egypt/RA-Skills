#!/bin/sh
# persona-update.sh — Update individual persona fields without re-running the full wizard.
# v2: Safe update pipeline with backup, diff preview, and --force flag.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Defaults
CONFIG_PATH="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
FORCE=false

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

usage() {
    cat << 'EOF'
Usage: persona-update.sh [OPTIONS]

Update specific persona fields without re-running the full wizard.

Options:
  --voice-provider PROVIDER    Set voice provider (elevenlabs|grok|builtin|none)
  --voice-id ID                Set ElevenLabs voice ID
  --add-trait TRAIT            Add a personality trait
  --remove-trait TRAIT         Remove a personality trait
  --appearance DESC            Update appearance description
  --regen-soul                 Regenerate SOUL.md from current config
  --regen-image                Regenerate reference image
  --name NAME                  Update agent name
  --emoji EMOJI                Update agent emoji
  --config PATH                Config file path (default: ~/.openclaw/openclaw.json)
  --workspace PATH             Workspace directory (default: ~/.openclaw/workspace)
  --force                      Skip diff review for --regen operations
  -i, --interactive            Interactive mode — walk through each field
  -h, --help                   Show this help
EOF
}

# --- Safe Update Pipeline ---

create_backup() {
    BACKUP_DIR="$WORKSPACE/.persona-backup"
    mkdir -p "$BACKUP_DIR"
    for f in SOUL.md USER.md IDENTITY.md MEMORY.md AGENTS.md HEARTBEAT.md; do
        if [ -f "$WORKSPACE/$f" ]; then
            cp "$WORKSPACE/$f" "$BACKUP_DIR/$f"
        fi
    done
    printf "${GREEN}  Backup created: $BACKUP_DIR${NC}\n"
}

show_diff_and_confirm() {
    file="$1"
    if [ "$FORCE" = "true" ]; then
        return 0
    fi
    if [ -f "$WORKSPACE/.persona-backup/$file" ] && [ -f "$WORKSPACE/$file" ]; then
        DIFF_OUT=$(diff -u "$WORKSPACE/.persona-backup/$file" "$WORKSPACE/$file" 2>/dev/null || true)
        if [ -n "$DIFF_OUT" ]; then
            printf "\n${YELLOW}  Changes to $file:${NC}\n"
            echo "$DIFF_OUT" | head -30
            printf "\n${CYAN}  Apply these changes? (y/n)${NC} > "
            read -r answer
            case "$answer" in
                [yY]*) return 0 ;;
                *)
                    cp "$WORKSPACE/.persona-backup/$file" "$WORKSPACE/$file"
                    printf "${RED}  Reverted $file${NC}\n"
                    return 1 ;;
            esac
        fi
    fi
    return 0
}

update_config_field() {
    field_path="$1"
    value="$2"
    python3 -c "
import json, sys
sys.path.insert(0, '$SCRIPT_DIR')
from lib.config import read_config, write_config

config = read_config('$CONFIG_PATH')
keys = '$field_path'.split('.')
d = config
for k in keys[:-1]:
    d = d.setdefault(k, {})
try:
    d[keys[-1]] = json.loads('$value')
except (json.JSONDecodeError, ValueError):
    d[keys[-1]] = '$value'
write_config(config, '$CONFIG_PATH')
"
}

regen_soul() {
    # Create backup before regeneration
    create_backup

    python3 -c "
import json, sys
sys.path.insert(0, '$SCRIPT_DIR')
from lib.config import read_config

config = read_config('$CONFIG_PATH')
persona = config.get('persona', {})

# Build profile from config
profile = {
    'name': persona.get('name', 'Agent'),
    'emoji': persona.get('emoji', ''),
    'creature': persona.get('identity', {}).get('creature', ''),
    'vibe': persona.get('identity', {}).get('vibe', ''),
    'archetype': persona.get('personality', {}).get('archetype', 'custom'),
}

# Include blend sources if present
archetypes = persona.get('personality', {}).get('archetypes')
if archetypes:
    profile['archetypes'] = archetypes

json.dump(profile, sys.stdout)
" | python3 "$SCRIPT_DIR/generate-soul.py" --output "$WORKSPACE/SOUL.md"

    # Show diff and confirm
    if show_diff_and_confirm "SOUL.md"; then
        printf "${GREEN}✅ SOUL.md regenerated${NC}\n"
    fi
}

# Parse arguments
INTERACTIVE=false
while [ $# -gt 0 ]; do
    case "$1" in
        --voice-provider)
            shift
            update_config_field "persona.voice.provider" "$1"
            printf "${GREEN}✅ Voice provider set to: $1${NC}\n"
            ;;
        --voice-id)
            shift
            update_config_field "persona.voice.elevenlabs.voiceId" "\"$1\""
            printf "${GREEN}✅ Voice ID updated${NC}\n"
            ;;
        --add-trait)
            shift
            python3 -c "
import json, sys
sys.path.insert(0, '$SCRIPT_DIR')
from lib.config import read_config, write_config
config = read_config('$CONFIG_PATH')
traits = config.setdefault('persona', {}).setdefault('personality', {}).setdefault('traits', [])
if '$1' not in traits:
    traits.append('$1')
write_config(config, '$CONFIG_PATH')
"
            printf "${GREEN}✅ Trait added: $1${NC}\n"
            ;;
        --remove-trait)
            shift
            python3 -c "
import json, sys
sys.path.insert(0, '$SCRIPT_DIR')
from lib.config import read_config, write_config
config = read_config('$CONFIG_PATH')
traits = config.get('persona', {}).get('personality', {}).get('traits', [])
if '$1' in traits:
    traits.remove('$1')
write_config(config, '$CONFIG_PATH')
"
            printf "${GREEN}✅ Trait removed: $1${NC}\n"
            ;;
        --appearance)
            shift
            update_config_field "persona.image.canonicalLook.description" "\"$1\""
            printf "${GREEN}✅ Appearance updated${NC}\n"
            ;;
        --regen-soul)
            regen_soul
            ;;
        --regen-image)
            python3 "$SCRIPT_DIR/image-setup.py" --config "$CONFIG_PATH" --regen
            printf "${GREEN}✅ Reference image regenerated${NC}\n"
            ;;
        --name)
            shift
            update_config_field "persona.name" "\"$1\""
            printf "${GREEN}✅ Name updated to: $1${NC}\n"
            ;;
        --emoji)
            shift
            update_config_field "persona.emoji" "\"$1\""
            printf "${GREEN}✅ Emoji updated to: $1${NC}\n"
            ;;
        --config)
            shift; CONFIG_PATH="$1" ;;
        --workspace)
            shift; WORKSPACE="$1" ;;
        --force)
            FORCE=true ;;
        -i|--interactive)
            INTERACTIVE=true ;;
        -h|--help)
            usage; exit 0 ;;
        *)
            printf "${RED}Unknown option: $1${NC}\n"
            usage; exit 1 ;;
    esac
    shift
done

if [ "$INTERACTIVE" = "true" ]; then
    printf "${BOLD}${CYAN}Interactive persona update${NC}\n\n"
    printf "Leave blank to keep current value.\n\n"

    printf "  Agent name > "
    read -r val
    if [ -n "$val" ]; then
        update_config_field "persona.name" "\"$val\""
        printf "${GREEN}  ✅ Updated${NC}\n"
    fi

    printf "  Emoji > "
    read -r val
    if [ -n "$val" ]; then
        update_config_field "persona.emoji" "\"$val\""
        printf "${GREEN}  ✅ Updated${NC}\n"
    fi

    printf "  Description > "
    read -r val
    if [ -n "$val" ]; then
        update_config_field "persona.identity.creature" "\"$val\""
        printf "${GREEN}  ✅ Updated${NC}\n"
    fi

    printf "\n  Regenerate SOUL.md? (y/n) > "
    read -r val
    case "$val" in
        [yY]*) regen_soul ;;
    esac

    printf "\n${GREEN}✅ Update complete${NC}\n"
fi
