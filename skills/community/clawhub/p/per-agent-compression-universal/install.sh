#!/bin/bash
# Per-Agent Memory Compression Skill - Universal Installer v1.3.6
# Auto-discovers agents and registers compression tasks with full feature set

set -e

# Default delivery configuration (can be overridden by CLI args or interactive prompts)
DELIVERY_CHANNEL="${DELIVERY_CHANNEL:-dingtalk-connector}"
DELIVERY_TO="${DELIVERY_TO:-}"
DELIVERY_ACCOUNT="${DELIVERY_ACCOUNT:-}"

# Parse command-line arguments for delivery preferences
while [[ $# -gt 0 ]]; do
  case $1 in
    --channel)
      DELIVERY_CHANNEL="$2"
      shift 2
      ;;
    --to)
      DELIVERY_TO="$2"
      shift 2
      ;;
    --account)
      DELIVERY_ACCOUNT="$2"
      shift 2
      ;;
    *)
      echo "⚠️  Unknown argument: $1"
      shift
      ;;
  esac
done

# If not all required params provided and stdin is a TTY, offer interactive prompts
if [[ -t 0 ]] && [[ -z "$DELIVERY_TO" ]]; then
  echo "🔧 Interactive installation mode detected."
  read -p "Enter delivery channel (default: $DELIVERY_CHANNEL): " input_channel
  DELIVERY_CHANNEL="${input_channel:-$DELIVERY_CHANNEL}"
  read -p "Enter recipient ID (--to): " input_to
  DELIVERY_TO="${input_to:-$DELIVERY_TO}"
  if [[ -n "$DELIVERY_TO" ]]; then
    read -p "Enter account/bot ID (optional, --account): " input_account
    DELIVERY_ACCOUNT="${input_account:-$DELIVERY_ACCOUNT}"
  fi
  echo ""
fi

# Validate required delivery config
if [[ -z "$DELIVERY_TO" ]]; then
  echo "❌ Delivery recipient (--to) is required for DingTalk connector."
  echo "   Provide it via --to flag, or set DELIVERY_TO environment variable."
  exit 1
fi

echo "🎯 Installing Per-Agent Memory Compression Skill (Universal) v1.3.6"
echo "📦 Delivery: channel=$DELIVERY_CHANNEL, to=$DELIVERY_TO${DELIVERY_ACCOUNT:+ (account=$DELIVERY_ACCOUNT)}"
echo ""

# 1. Pre-checks
echo "🔍 Running pre-installation checks..."

if ! command -v openclaw &> /dev/null; then
  echo "❌ openclaw CLI not found in PATH"
  exit 1
fi

if ! openclaw agents list --json &> /dev/null; then
  echo "❌ openclaw agents list failed - is Gateway running?"
  exit 1
fi

echo "✅ Pre-checks passed"
echo ""

# 2. Discover agents with workspaces
AGENTS_JSON=$(openclaw agents list --json 2>&1)

AGENTS=$(echo "$AGENTS_JSON" | jq -r '.[] | select(.workspace != null) | "\(.id)=\(.workspace)"' 2>/dev/null)
if [ -z "$AGENTS" ]; then
  echo "❌ No agents with workspace found"
  exit 1
fi

echo "📋 Discovered agents:"
echo "$AGENTS" | while IFS='=' read -r id ws; do
  echo "  ✅ $id → $ws"
done
echo ""

# 3. Define domain context for known agents
declare -A DOMAIN_CONTEXT
DOMAIN_CONTEXT[main]="general (main agent - overall user context)"
DOMAIN_CONTEXT[hrbp]="HR/work-related (hrbp agent - professional, career, organizational development)"
DOMAIN_CONTEXT[parenting]="Parenting/family (parenting agent - children, education, family dynamics)"
DOMAIN_CONTEXT[decoration]="Renovation/decoration (decoration agent - construction, materials, project management)"
# Default for unknown agents
DOMAIN_CONTEXT[default]="agent-specific (adapt based on agent's identity and role)"

# 4. Staggered schedule offsets (minutes from 03:00 Sunday)
OFFSETS=(0 30 60 90 120 150 180 210 240 270)

INDEX=0
TASK_IDS=()
echo "$AGENTS" | while IFS='=' read -r agent_id workspace; do
  OFFSET=${OFFSETS[$INDEX]}
  INDEX=$((INDEX + 1))
  
  HOUR=$((3 + OFFSET / 60))
  MINUTE=$((OFFSET % 60))
  CRON="${MINUTE} ${HOUR} * * 0"
  
  TASK_NAME="per_agent_compression_${agent_id}"
  
  # Check if task exists
  if openclaw cron list --json 2>/dev/null | jq -e --arg name "$TASK_NAME" '.jobs[] | select(.name == $name)' >/dev/null; then
    echo "  ⚠️  Task $TASK_NAME already exists, skipping"
    continue
  fi
  
  echo "  📝 Creating: $TASK_NAME ($CRON)"
  
  # Determine domain context
  DOMAIN="${DOMAIN_CONTEXT[$agent_id]:-$DOMAIN_CONTEXT[default]}"
  
  # Determine delivery configuration
  DELIVERY_CONFIG=""
  if [[ -n "$DELIVERY_ACCOUNT" ]]; then
    DELIVERY_CONFIG="--account $DELIVERY_ACCOUNT"
  fi
  
  # Two-step message setting to bypass CLI length limit
  # MSG_SHORT: concise but includes all essential logic (~500 chars)
  # MSG_FULL: complete reference (used via edit after add)
  MSG_SHORT="AUTONOMOUS: Weekly per-agent memory consolidation for '$agent_id'.\n\nWorkspace: $workspace\nDAILY_NOTES_DIR: {WORKSPACE}/memory\nPROCESSED_DIR: {WORKSPACE}/memory/processed\nSTATE_FILE: {WORKSPACE}/memory/.compression_state.json\nTARGET_FILES: USER.md, IDENTITY.md, SOUL.md, MEMORY.md\n\nDOMAIN_CONTEXT: \"$DOMAIN\"\n\nPURPOSE: Systematically preserve conversation history by extracting key information (decisions, constraints, principles, todos, metrics, people, context) from daily notes and solidifying into agent configuration files.\n\nEXECUTION:\n1) Pre-check paths; init state\n2) List YYYY-MM-DD.md (<7d, not processed), sort oldest, limit 5\n3) For each: read full content, apply COMPREHENSIVE EXTRACTION framework, dedupe (same date), append to targets with structured header (### [YYYY-MM-DD])\n4) Move to processed/, update state\n5) Announce summary (processed, remaining)\n\nIMPORTANT: Capture ALL key elements: decisions, constraints, principles, todos, metrics, people, context, problems/solutions. Do NOT oversimplify. Full extraction guide in README. Append only. Continue on error.\n\nExecute without waiting."
  
  MSG_FULL="AUTONOMOUS: Weekly per-agent memory consolidation for '$agent_id'.\n\nWorkspace: $workspace\nDAILY_NOTES_DIR: {WORKSPACE}/memory\nPROCESSED_DIR: {WORKSPACE}/memory/processed\nSTATE_FILE: {WORKSPACE}/memory/.compression_state.json\nTARGET_FILES: USER.md, IDENTITY.md, SOUL.md, MEMORY.md\n\nDOMAIN_CONTEXT: \"$DOMAIN\"\n\nDELIVERY: channel=$DELIVERY_CHANNEL, to=$DELIVERY_TO${DELIVERY_ACCOUNT:+ (account=$DELIVERY_ACCOUNT)}\n\nPURPOSE: Systematically preserve conversation history by extracting key information from daily notes and solidifying into agent configuration files. Goal: Capture decisions, constraints, principles, todos, metrics, people, context, problem-solution pairs, and user traits.\n\nEXECUTION PLAN:\n1) Pre-check paths (workspace, memory/, targets)\n2) Load/init state (JSON: last_compressed_date, processed_notes set)\n3) List daily notes: memory/YYYY-MM-DD.md, date < today-7, not in processed_notes\n4) Sort by date (oldest first), limit to 5 notes per run\n5) For each note:\n   a) Read full content (entire daily note)\n   b) Apply COMPREHENSIVE EXTRACTION FRAMEWORK (see below)\n   c) Dedupe: if note date already in target files, consider skip or refresh (skip for now)\n   d) Append to targets with structured header \"### [YYYY-MM-DD]\" and domain-tailored summary\n6) Move processed note to memory/processed/ (create dir if needed)\n7) Update state: add note date to processed_notes, update last_compressed_date\n8) Save state file (JSON)\n9) Announce summary: processed count, remaining old notes count\n\nRETRY & ALERT POLICY:\n- For transient errors (network, API rate limits, temporary model failures), implement auto-retry up to 3 times with exponential backoff (2s, 4s, 8s)\n- Log each retry attempt with error details\n- If all retries exhausted, record failure in state and continue to next note\n- At the end, if any notes failed completely, include failure count in the summary announcement\n- Do NOT retry on permanent errors (syntax, missing files) - log and skip\n\nCOMPREHENSIVE EXTRACTION FRAMEWORK:\nFor each daily note, extract and summarize:\n- **Key Decisions**: Major choices made, paths selected, alternatives rejected\n- **Constraints**: Time, budget, resource limits; rules/policies; hard boundaries\n- **Principles & Values**: Stated priorities, ethical positions, non-negotiable tenets\n- **Todos & Commitments**: Action items, promises, follow-ups (who/what/when)\n- **Metrics & Targets**: Numbers, dates, frequencies, KPIs, success criteria\n- **People & Roles**: Names, teams, stakeholders, relationships\n- **Context**: Project background, environmental factors, external conditions\n- **Problems & Solutions**: Obstacles encountered, resolutions attempted, outcomes\n- **Preferences**: Likes/dislikes, communication style, working habits\n- **User Traits & Self-Profile**: Personality traits, communication preferences, learning style, values, interests, strengths/weaknesses, self-descriptions (direct quotes or paraphrased)\n- **References**: Tools, systems, documents mentioned (capture names/IDs)\n\nFORMAT BY TARGET:\n- USER.md → \"## Personal Info / Preferences\" section, include User Traits prominently, use bullet points, include dates\n- IDENTITY.md → \"## Notes\" section, capture identity-relevant facts and context\n- SOUL.md → \"## Principles\" or \"## Boundaries\" (choose based on content), formalize as guidelines\n- MEMORY.md → \"## Key Learnings\" section, format: \"- [YYYY-MM-DD] Concise summary covering multiple categories above\"\n\nIMPORTANT:\n- DO NOT oversimplify. Capture substance, not just labels.\n- Preserve nuance: convert conversational language to structured statements.\n- If uncertain, include with low confidence marker? (No—only extract clear info)\n- Append only; never modify existing content (duplicate dates means content drift; instead, update by replacing? Actually instruction: dedupe by checking if date exists → skip. But we may want to refresh if note is newer. Keep simple: skip if same date already in targets.\n- Continue on error (log and proceed to next note)\n- See README for full details and examples\n\nExecute without waiting."
  
  # Build announce delivery arguments with channel/to/account
  ANNOUNCE_ARGS="--announce"
  if [[ -n "$DELIVERY_CHANNEL" ]]; then
    ANNOUNCE_ARGS="$ANNOUNCE_ARGS --channel $DELIVERY_CHANNEL"
  fi
  if [[ -n "$DELIVERY_TO" ]]; then
    ANNOUNCE_ARGS="$ANNOUNCE_ARGS --to $DELIVERY_TO"
  fi
  if [[ -n "$DELIVERY_ACCOUNT" ]]; then
    ANNOUNCE_ARGS="$ANNOUNCE_ARGS --account $DELIVERY_ACCOUNT"
  fi
  
  if openclaw cron add \
    --name "$TASK_NAME" \
    --cron "$CRON" \
    --tz "Asia/Shanghai" \
    --agent "$agent_id" \
    --message "$MSG_SHORT" \
    --timeout 1200 \
    --session "isolated" \
    $ANNOUNCE_ARGS 2>&1; then
    
    # Get the job ID of the just-created task
    JOB_ID=$(openclaw cron list --json 2>&1 | jq -r --arg name "$TASK_NAME" '.jobs[] | select(.name == $name) | .id')
    
    if [ -n "$JOB_ID" ]; then
      echo "  ✨ Enriching task with full execution plan (job ID: ${JOB_ID:0:8}...)"
      if openclaw cron edit "$JOB_ID" --message "$MSG_FULL" 2>&1; then
        echo "  ✅ Task enriched"
      else
        echo "  ⚠️  Warning: Failed to enrich task message. Task may lack full details. Check README for complete spec."
      fi
    else
      echo "  ⚠️  Warning: Could not retrieve job ID for enrichment."
    fi
    
    TASK_IDS+=("$TASK_NAME")
  else
    echo "    ❌ Failed to create task $TASK_NAME"
  fi
done

echo ""
echo "✅ Installation complete!"
echo ""
if [ ${#TASK_IDS[@]} -gt 0 ]; then
  echo "📋 Created ${#TASK_IDS[@]} task(s):"
  for tid in "${TASK_IDS[@]}"; do
    echo "   - $tid"
  done
  echo ""
  echo "💡 Note: Task messages are concise but contain all essential logic."
  echo "💡 For full execution plan details, see: /root/.openclaw/workspace/skills/per-agent-compression-universal/README.md"
  echo "💡 Verify: openclaw cron list | grep per_agent_compression"
  echo "💡 Uninstall: ./uninstall.sh"
else
  echo "⚠️  No new tasks were created (all may already exist)"
fi
