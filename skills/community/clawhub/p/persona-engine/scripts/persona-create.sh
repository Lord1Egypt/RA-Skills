#!/bin/sh
# persona-create.sh — Interactive AI Persona Engine setup wizard
# Creates a complete persona with personality, voice, image, and memory config.
# v2: Supports --dry-run, --workspace, and personality blending.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENGINE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors (POSIX-compatible)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# --- CLI flags ---
DRY_RUN=false
CLI_WORKSPACE=""
CLI_CONFIG=""

# Parse pre-wizard flags
for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --workspace=*) CLI_WORKSPACE="${arg#--workspace=}" ;;
        --config=*) CLI_CONFIG="${arg#--config=}" ;;
    esac
done

# --- Helper functions ---

prompt_required() {
    label="$1"
    while true; do
        printf "${CYAN}  %s${NC} > " "$label"
        read -r answer
        if [ -n "$answer" ]; then
            echo "$answer"
            return
        fi
        printf "${RED}  This field is required.${NC}\n"
    done
}

prompt_optional() {
    label="$1"
    default="$2"
    printf "${CYAN}  %s${NC}" "$label"
    if [ -n "$default" ]; then
        printf " [%s]" "$default"
    fi
    printf " > "
    read -r answer
    if [ -n "$answer" ]; then
        echo "$answer"
    else
        echo "$default"
    fi
}

prompt_yn() {
    label="$1"
    default="$2"
    printf "${CYAN}  %s${NC} [%s] > " "$label" "$default"
    read -r answer
    answer="${answer:-$default}"
    case "$answer" in
        [yY]*) echo "true" ;;
        *) echo "false" ;;
    esac
}

prompt_choice() {
    label="$1"
    shift
    printf "${CYAN}  %s${NC}\n" "$label"
    i=1
    for choice in "$@"; do
        printf "    ${BOLD}[%d]${NC} %s\n" "$i" "$choice"
        i=$((i + 1))
    done
    while true; do
        printf "  > "
        read -r answer
        if [ -n "$answer" ] && [ "$answer" -ge 1 ] 2>/dev/null && [ "$answer" -le $# ] 2>/dev/null; then
            echo "$answer"
            return
        fi
        printf "${RED}  Please enter a number between 1 and %d.${NC}\n" "$#"
    done
}

prompt_inline_choice() {
    label="$1"
    default="$2"
    shift 2
    printf "${CYAN}  %s${NC} (%s) [%s] > " "$label" "$*" "$default"
    read -r answer
    answer="${answer:-$default}"
    echo "$answer"
}

# --- Main wizard ---

printf "\n${BOLD}${BLUE}🧬 AI Persona Engine — Let's build your agent's identity.${NC}\n\n"

# Step 1: Name & Identity
printf "${BOLD}${YELLOW}Step 1/7: Name & Identity${NC}\n"
PERSONA_NAME=$(prompt_required "What's your agent's name?")
PERSONA_EMOJI=$(prompt_required "Pick an emoji:")
PERSONA_CREATURE=$(prompt_required 'Short description (e.g., "executive assistant"):')
PERSONA_NICKNAME=$(prompt_optional "Nickname (optional):" "")
PERSONA_VIBE=$(prompt_optional "Vibe (one-line summary):" "")
printf "\n"

# Step 2: Personality
printf "${BOLD}${YELLOW}Step 2/7: Personality${NC}\n"
ARCHETYPE_NUM=$(prompt_choice "Choose a starting archetype:" \
    "Professional — competent, direct, business-focused" \
    "Companion — warm, personal, emotionally intelligent" \
    "Creative — imaginative, playful, artistic" \
    "Mentor — wise, patient, educational" \
    "Custom — start from scratch")

case "$ARCHETYPE_NUM" in
    1) ARCHETYPE="professional" ;;
    2) ARCHETYPE="companion" ;;
    3) ARCHETYPE="creative" ;;
    4) ARCHETYPE="mentor" ;;
    5) ARCHETYPE="custom" ;;
esac

# Personality blending
BLEND_ENABLED=false
BLEND_SECONDARY=""
BLEND_PRIMARY_WEIGHT="0.7"
BLEND_SECONDARY_WEIGHT="0.3"

if [ "$ARCHETYPE" != "custom" ]; then
    BLEND_YN=$(prompt_yn "Blend with a second archetype? (y/n):" "n")
    if [ "$BLEND_YN" = "true" ]; then
        BLEND_ENABLED=true
        printf "  ${BOLD}Choose secondary archetype:${NC}\n"
        printf "    Available: professional, companion, creative, mentor\n"
        printf "    Community: financial-advisor, fitness-coach, kids-tutor, creative-writer,\n"
        printf "               sales-rep, therapist, gaming-buddy, executive-assistant\n"
        BLEND_SECONDARY=$(prompt_required "Secondary archetype:")
        BLEND_PRIMARY_WEIGHT=$(prompt_optional "Primary weight (0.0-1.0):" "0.7")
        BLEND_SECONDARY_WEIGHT=$(prompt_optional "Secondary weight (0.0-1.0):" "0.3")
    fi
fi

printf "\n  ${BOLD}How should they communicate?${NC}\n"
BREVITY=$(prompt_optional "Brevity level (1=verbose, 5=terse):" "3")
HUMOR=$(prompt_yn "Use humor? (y/n):" "y")
SWEARING=$(prompt_inline_choice "Swearing allowed?" "never" "never" "rare" "when-it-lands" "frequent")
BAN_OPENERS=$(prompt_yn 'Ban corporate openers like "Great question!"? (y/n):' "y")

printf "\n  ${BOLD}Relationship style with you:${NC}\n"
PET_NAMES=$(prompt_yn "Affectionate (pet names, emotional depth)? (y/n):" "n")
FLIRTATION=$(prompt_yn "Flirtatious? (y/n):" "n")
PROTECTIVE=$(prompt_yn "Protective (pushback on bad ideas)? (y/n):" "y")

# Determine emotional depth
EMOTIONAL_DEPTH="low"
if [ "$PET_NAMES" = "true" ]; then
    EMOTIONAL_DEPTH="high"
elif [ "$FLIRTATION" = "true" ]; then
    EMOTIONAL_DEPTH="medium"
fi
printf "\n"

# Step 3: Voice
printf "${BOLD}${YELLOW}Step 3/7: Voice${NC}\n"
VOICE_NUM=$(prompt_choice "Choose a voice provider:" \
    "ElevenLabs (best quality, custom voices, cloning)" \
    "Grok TTS (xAI, integrated with Grok models)" \
    "Built-in OpenClaw TTS (no API key needed)" \
    "None (text only)")

case "$VOICE_NUM" in
    1) VOICE_PROVIDER="elevenlabs" ;;
    2) VOICE_PROVIDER="grok" ;;
    3) VOICE_PROVIDER="builtin" ;;
    4) VOICE_PROVIDER="none" ;;
esac

VOICE_ID=""
if [ "$VOICE_PROVIDER" = "elevenlabs" ]; then
    VOICE_ID=$(prompt_optional "ElevenLabs Voice ID (or leave blank to configure later):" "")
fi
printf "\n"

# Step 4: Visual Identity
printf "${BOLD}${YELLOW}Step 4/7: Visual Identity${NC}\n"
IMAGE_NUM=$(prompt_choice "Choose an image provider:" \
    "Gemini (photorealistic, reference image support)" \
    "Grok Imagine (creative, fewer restrictions)" \
    "Both (Gemini default, Grok for creative)" \
    "None (no visual identity)")

case "$IMAGE_NUM" in
    1) IMAGE_PROVIDER="gemini" ;;
    2) IMAGE_PROVIDER="grok" ;;
    3) IMAGE_PROVIDER="both" ;;
    4) IMAGE_PROVIDER="none" ;;
esac

APPEARANCE=""
if [ "$IMAGE_PROVIDER" != "none" ]; then
    APPEARANCE=$(prompt_optional "Describe your agent's appearance:" "")
fi
printf "\n"

# Step 5: User Context
printf "${BOLD}${YELLOW}Step 5/7: Your Context (USER.md)${NC}\n"
USER_NAME=$(prompt_required "Your name:")
CALL_NAMES=$(prompt_optional "What should the agent call you?" "$USER_NAME")
USER_PRONOUNS=$(prompt_optional "Your pronouns (optional):" "")
USER_TIMEZONE=$(prompt_optional "Your timezone:" "UTC")
USER_NOTES=$(prompt_optional "Anything else they should know?" "")
printf "\n"

# Step 6: Memory
printf "${BOLD}${YELLOW}Step 6/7: Memory${NC}\n"
DAILY_NOTES=$(prompt_yn "Enable daily memory notes? (y/n):" "y")
LONG_TERM=$(prompt_yn "Enable long-term memory curation? (y/n):" "y")
HEARTBEAT_MAINT=$(prompt_yn "Auto-maintain memory during heartbeats? (y/n):" "y")
printf "\n"

# Step 7: Platforms
printf "${BOLD}${YELLOW}Step 7/7: Platforms${NC}\n"
printf "${CYAN}  Which channels will this persona use? (comma-separated)${NC}\n"
printf "    Available: telegram, whatsapp, discord, signal, sms, voice\n"
PLATFORMS=$(prompt_optional "Channels:" "telegram")
printf "\n"

# --- Determine workspace ---
DEFAULT_WORKSPACE="${CLI_WORKSPACE:-$HOME/.openclaw/workspace}"
DEFAULT_CONFIG="${CLI_CONFIG:-$HOME/.openclaw/openclaw.json}"
WORKSPACE=$(prompt_optional "Workspace directory:" "$DEFAULT_WORKSPACE")
CONFIG_PATH=$(prompt_optional "Config file path:" "$DEFAULT_CONFIG")

printf "\n${BOLD}${BLUE}🔨 Generating persona files...${NC}\n\n"

# --- Dry run check ---
if [ "$DRY_RUN" = "true" ]; then
    printf "\n${BOLD}${YELLOW}🔍 DRY RUN — Files that would be generated:${NC}\n\n"
    printf "  • ${WORKSPACE}/SOUL.md\n"
    printf "  • ${WORKSPACE}/USER.md\n"
    printf "  • ${WORKSPACE}/IDENTITY.md\n"
    printf "  • ${WORKSPACE}/MEMORY.md\n"
    printf "  • ${WORKSPACE}/AGENTS.md\n"
    printf "  • ${WORKSPACE}/HEARTBEAT.md\n"
    printf "  • ${WORKSPACE}/memory/$(date +%%Y-%%m-%%d).md\n"
    printf "  • ${CONFIG_PATH} (persona section)\n"
    if [ "$VOICE_PROVIDER" != "none" ]; then
        printf "  • ${CONFIG_PATH} (messages.tts section)\n"
    fi
    if [ "$IMAGE_PROVIDER" != "none" ]; then
        printf "  • ${CONFIG_PATH} (persona.image section)\n"
    fi
    printf "\n  Archetype: ${ARCHETYPE}"
    if [ "$BLEND_ENABLED" = "true" ]; then
        printf " + ${BLEND_SECONDARY} (${BLEND_PRIMARY_WEIGHT}/${BLEND_SECONDARY_WEIGHT})"
    fi
    printf "\n"
    printf "\n${BOLD}No files were written.${NC}\n"
    exit 0
fi

# --- Build personality profile JSON ---
# Write a temp profile for the soul generator
PROFILE_TMP=$(mktemp)

if [ "$BLEND_ENABLED" = "true" ]; then
cat > "$PROFILE_TMP" << PROFILE_EOF
{
    "name": "$PERSONA_NAME",
    "emoji": "$PERSONA_EMOJI",
    "creature": "$PERSONA_CREATURE",
    "vibe": "$PERSONA_VIBE",
    "userName": "$USER_NAME",
    "archetypes": [
        {"name": "$ARCHETYPE", "weight": $BLEND_PRIMARY_WEIGHT},
        {"name": "$BLEND_SECONDARY", "weight": $BLEND_SECONDARY_WEIGHT}
    ],
    "communication": {
        "brevity": $BREVITY,
        "humor": $HUMOR,
        "swearing": "$SWEARING",
        "banOpeningPhrases": $BAN_OPENERS
    },
    "boundaries": {
        "petNames": $PET_NAMES,
        "flirtation": $FLIRTATION,
        "emotionalDepth": "$EMOTIONAL_DEPTH",
        "protective": $PROTECTIVE
    },
    "userRelationship": {
        "userName": "$USER_NAME"
    }
}
PROFILE_EOF
else
cat > "$PROFILE_TMP" << PROFILE_EOF
{
    "name": "$PERSONA_NAME",
    "emoji": "$PERSONA_EMOJI",
    "creature": "$PERSONA_CREATURE",
    "vibe": "$PERSONA_VIBE",
    "archetype": "$ARCHETYPE",
    "userName": "$USER_NAME",
    "communication": {
        "brevity": $BREVITY,
        "humor": $HUMOR,
        "swearing": "$SWEARING",
        "banOpeningPhrases": $BAN_OPENERS
    },
    "boundaries": {
        "petNames": $PET_NAMES,
        "flirtation": $FLIRTATION,
        "emotionalDepth": "$EMOTIONAL_DEPTH",
        "protective": $PROTECTIVE
    },
    "userRelationship": {
        "userName": "$USER_NAME"
    }
}
PROFILE_EOF
fi

# --- Generate SOUL.md ---
python3 "$SCRIPT_DIR/generate-soul.py" \
    --input "$PROFILE_TMP" \
    --archetype "$ARCHETYPE" \
    --output "$WORKSPACE/SOUL.md"

# --- Generate USER.md ---
python3 "$SCRIPT_DIR/generate-user.py" \
    --name "$USER_NAME" \
    --call-names "$CALL_NAMES" \
    --pronouns "$USER_PRONOUNS" \
    --timezone "$USER_TIMEZONE" \
    --notes "$USER_NOTES" \
    --output "$WORKSPACE/USER.md"

# --- Generate IDENTITY.md ---
python3 "$SCRIPT_DIR/generate-identity.py" \
    --name "$PERSONA_NAME" \
    --emoji "$PERSONA_EMOJI" \
    --creature "$PERSONA_CREATURE" \
    --vibe "$PERSONA_VIBE" \
    --nickname "$PERSONA_NICKNAME" \
    --output "$WORKSPACE/IDENTITY.md"

# --- Generate MEMORY.md + HEARTBEAT.md + AGENTS.md + memory/ ---
MEMORY_FLAGS=""
if [ "$DAILY_NOTES" = "false" ]; then MEMORY_FLAGS="$MEMORY_FLAGS --no-daily-notes"; fi
if [ "$LONG_TERM" = "false" ]; then MEMORY_FLAGS="$MEMORY_FLAGS --no-long-term"; fi
if [ "$HEARTBEAT_MAINT" = "false" ]; then MEMORY_FLAGS="$MEMORY_FLAGS --no-heartbeat-maintenance"; fi

python3 "$SCRIPT_DIR/generate-memory.py" \
    --name "$PERSONA_NAME" \
    --emoji "$PERSONA_EMOJI" \
    --creature "$PERSONA_CREATURE" \
    --user-name "$USER_NAME" \
    --workspace "$WORKSPACE" \
    $MEMORY_FLAGS

# --- Configure voice (if selected) ---
if [ "$VOICE_PROVIDER" != "none" ]; then
    python3 "$SCRIPT_DIR/voice-setup.py" \
        --provider "$VOICE_PROVIDER" \
        --voice-id "$VOICE_ID" \
        --config "$CONFIG_PATH" \
        --non-interactive
fi

# --- Configure image (if selected) ---
if [ "$IMAGE_PROVIDER" != "none" ]; then
    python3 "$SCRIPT_DIR/image-setup.py" \
        --provider "$IMAGE_PROVIDER" \
        --description "$APPEARANCE" \
        --config "$CONFIG_PATH" \
        --non-interactive
fi

# --- Write persona config to openclaw.json ---
PERSONA_CONFIG_TMP=$(mktemp)
cat > "$PERSONA_CONFIG_TMP" << CONFIG_EOF
{
    "persona": {
        "name": "$PERSONA_NAME",
        "emoji": "$PERSONA_EMOJI",
        "identity": {
            "creature": "$PERSONA_CREATURE",
            "vibe": "$PERSONA_VIBE",
            "nickname": "$PERSONA_NICKNAME"
        },
        "personality": {
            "archetype": "$ARCHETYPE",
            "communicationStyle": {
                "brevity": $BREVITY,
                "humor": $HUMOR,
                "swearing": "$SWEARING",
                "openingPhrases": "$([ "$BAN_OPENERS" = "true" ] && echo "banned" || echo "allowed")"
            },
            "boundaries": {
                "petNames": $PET_NAMES,
                "flirtation": $FLIRTATION,
                "emotionalDepth": "$EMOTIONAL_DEPTH"
            },
            "evolves": false
        },
        "memory": {
            "autoCapture": true,
            "dailyNotes": $DAILY_NOTES,
            "longTermCuration": $LONG_TERM,
            "heartbeatMaintenance": $HEARTBEAT_MAINT
        }
    }
}
CONFIG_EOF

python3 -c "
import json, sys
sys.path.insert(0, '$SCRIPT_DIR')
from lib.config import merge_config
with open('$PERSONA_CONFIG_TMP', 'r') as f:
    updates = json.load(f)
merge_config(updates, '$CONFIG_PATH')
print('Config updated: $CONFIG_PATH', file=sys.stderr)
"

# Clean up temp files
rm -f "$PROFILE_TMP" "$PERSONA_CONFIG_TMP"

# --- Success ---
printf "\n${BOLD}${GREEN}✅ Persona \"$PERSONA_NAME $PERSONA_EMOJI\" created!${NC}\n\n"
printf "${BOLD}Files generated:${NC}\n"
printf "  • SOUL.md — personality and behavioral guidelines\n"
printf "  • USER.md — your context and preferences\n"
printf "  • IDENTITY.md — name, emoji, avatar reference\n"
printf "  • MEMORY.md — bootstrapped long-term memory\n"
printf "  • AGENTS.md — workspace conventions\n"
printf "  • HEARTBEAT.md — proactive behavior config\n"
printf "\n"
printf "${BOLD}Config updated:${NC}\n"
printf "  • openclaw.json → persona section added\n"
if [ "$VOICE_PROVIDER" != "none" ]; then
    printf "  • openclaw.json → messages.tts configured\n"
fi
printf "\n"
printf "${BOLD}Next steps:${NC}\n"
printf "  • Review SOUL.md and adjust anything that doesn't feel right\n"
printf "  • Run ${CYAN}openclaw gateway restart${NC} to apply changes\n"
printf "  • Say hello to $PERSONA_NAME on ${PLATFORMS}!\n"
printf "  • Run ${CYAN}persona-preview.py${NC} to see sample conversations\n"
