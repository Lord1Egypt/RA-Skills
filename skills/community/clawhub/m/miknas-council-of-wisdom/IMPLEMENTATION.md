# Council of Wisdom - Implementation Guide

This guide explains how to implement the Council of Wisdom system using OpenClaw's ACP (Agent Control Panel) for agent orchestration.

## Overview

The Council of Wisdom requires multi-agent orchestration using OpenClaw's `sessions_spawn` runtime. This guide shows how to implement the full debate flow with automatic cleanup.

## Prerequisites

- OpenClaw with ACP runtime enabled
- Agent IDs configured for:
  - Referee agent
  - Debater agents (2)
  - Council member agents (9)
- GitHub CLI (`gh`) for repo integration

## Agent Setup

### 1. Create Agent Prompts

Copy the template prompts to your workspace:

```bash
# Copy referee prompt
cp ~/.openclaw/workspace/skills/council-of-wisdom/templates/referee-prompt.md \
   ~/.openclaw/workspace/council-of-wisdom/<project>/workspace/prompts/referee.md

# Copy debater prompts
cp ~/.openclaw/workspace/skills/council-of-wisdom/templates/debater-prompt.md \
   ~/.openclaw/workspace/council-of-wisdom/<project>/workspace/prompts/debater-a.md
cp ~/.openclaw/workspace/skills/council-of-wisdom/templates/debater-prompt.md \
   ~/.openclaw/workspace/council-of-wisdom/<project>/workspace/prompts/debater-b.md

# Copy council prompts (create individual files)
mkdir -p ~/.openclaw/workspace/council-of-wisdom/<project>/workspace/prompts/council
# Then create 9 files from templates/council-prompts.md
```

### 2. Configure Agent IDs

Create agent configuration files:

```json
// workspace/agents/referee.json
{
  "agentId": "council-referee",
  "promptFile": "workspace/prompts/referee.md",
  "model": "zai/glm-4.7",
  "runtime": "acp",
  "thinking": "high"
}
```

```json
// workspace/agents/debater-a.json
{
  "agentId": "council-debater-a",
  "promptFile": "workspace/prompts/debater-a.md",
  "model": "zai/glm-4.7",
  "runtime": "acp",
  "thinking": "medium"
}
```

```json
// workspace/agents/council.json
{
  "members": [
    {"name": "logician", "agentId": "council-logician", "model": "openai/gpt-4"},
    {"name": "empiricist", "agentId": "council-empiricist", "model": "anthropic/claude-3-opus"},
    {"name": "pragmatist", "agentId": "council-pragmatist", "model": "zai/glm-4.7"},
    {"name": "ethicist", "agentId": "council-ethicist", "model": "google/gemini-pro"},
    {"name": "futurist", "agentId": "council-futurist", "model": "openai/gpt-4"},
    {"name": "historian", "agentId": "council-historian", "model": "anthropic/claude-3-opus"},
    {"name": "systems-thinker", "agentId": "council-systems", "model": "zai/glm-4.7"},
    {"name": "risk-analyst", "agentId": "council-risk", "model": "google/gemini-pro"},
    {"name": "synthesizer", "agentId": "council-synthesizer", "model": "openai/gpt-4"}
  ]
}
```

## Implementation Approach

### Option 1: Single Orchestrator Agent

Spawn one Referee agent that orchestrates everything:

```bash
# Spawn referee with full debate parameters
sessions_spawn \
  runtime=acp \
  agentId=council-referee \
  task="Orchestrate a debate on: '${TOPIC}'
   Domain: ${DOMAIN}
   Perspective A: ${PERSPECTIVE_A}
   Perspective B: ${PERSPECTIVE_B}
   Multi-provider: ${MULTI_PROVIDER}" \
  thread=true \
  timeoutSeconds=300
```

**Pros:** Simple, single session to manage
**Cons:** Referee needs to handle all spawning logic

### Option 2: Multi-Agent with Orchestrator

Use a lightweight orchestrator script:

```bash
#!/usr/bin/bash

# Start debate
echo "Starting Council of Wisdom debate..."

# Step 1: Spawn Referee
REF_SESSION=$(sessions_spawn \
  runtime=acp \
  agentId=council-referee \
  task="You are orchestrating a debate on: ${TOPIC}" \
  mode=session \
  thread=true)

echo "Referee session: ${REF_SESSION}"

# Step 2: Send debate parameters to referee
sessions_send \
  sessionKey=${REF_SESSION} \
  message="Start debate with:
  - Topic: ${TOPIC}
  - Domain: ${DOMAIN}
  - Perspective A: ${PERSPECTIVE_A}
  - Perspective B: ${PERSPECTIVE_B}
  - Multi-provider: ${MULTI_PROVIDER}"

# Step 3: Wait for debate completion
# (This would be managed by the referee)

echo "Debate initiated. Check ${REF_SESSION} for progress."
```

**Pros:** More control, can monitor each step
**Cons:** More complex orchestration

## Referee Agent Implementation

The referee agent should follow this flow:

### 1. Receive Debate Parameters

The referee receives the topic, domain, and perspectives.

### 2. Setup Phase

Referee creates debate structure and saves metadata.

### 3. Spawn Debaters

Referee spawns two debater agents:

```bash
# In Referee's task execution
spawn_debater_a() {
  sessions_spawn \
    runtime=acp \
    agentId=council-debater-a \
    task="Present opening argument for perspective: ${PERSPECTIVE_A}
          on topic: ${TOPIC}
          Domain: ${DOMAIN}" \
    mode=run \
    timeoutSeconds=60
}

spawn_debater_b() {
  sessions_spawn \
    runtime=acp \
    agentId=council-debater-b \
    task="Present opening argument for perspective: ${PERSPECTIVE_B}
          on topic: ${TOPIC}
          Domain: ${DOMAIN}" \
    mode=run \
    timeoutSeconds=60
}
```

### 4. Collect Arguments

Referee collects and structures the debate transcript.

### 5. Spawn Council

Referee spawns all 9 council members:

```bash
spawn_council() {
  local transcript="$1"

  for member in "${COUNCIL_MEMBERS[@]}"; do
    local agent_id="council-${member}"
    local model=$(get_random_model)

    sessions_spawn \
      runtime=acp \
      agentId=${agent_id} \
      model=${model} \
      task="Review the following debate transcript and vote:

${transcript}

Provide your vote in JSON format:
{
  \"vote\": \"Perspective A\" or \"Perspective B\",
  \"score\": <1-10>,
  \"reasoning\": \"<2-3 sentences>\"
}" \
      mode=run \
      timeoutSeconds=90
  done
}
```

### 6. Collect Votes

Referee tallies votes and determines winner.

### 7. Generate Report

Referee creates structured outcome report.

### 8. Cleanup Council

Referee terminates all council sessions:

```bash
cleanup_council() {
  for member in "${COUNCIL_MEMBERS[@]}"; do
    subagents action=kill target="council-${member}"
  done
}
```

### 9. Return Result

Referee sends final report to user.

## Monitoring and Logging

### Debate Logging

Each debate should log to:

```
workspace/logs/
  └── debate-20260307-001/
      ├── metadata.json
      ├── transcript.md
      ├── votes.json
      └── report.md
```

### Metrics Tracking

Track metrics after each debate:

```bash
# Update metrics
update_metrics() {
  local debate_id="$1"
  local duration="$2"
  local vote_distribution="$3"

  jq --arg id "$debate_id" \
     --arg dur "$duration" \
     --arg votes "$vote_distribution" \
     '.debates += [{"id": $id, "duration": $dur, "votes": $votes}]' \
     workspace/monitoring/debate-metrics.json > tmp.json && mv tmp.json workspace/monitoring/debate-metrics.json
}
```

## Automatic Cleanup

Ensure cleanup always happens:

```bash
cleanup_on_exit() {
  # Cleanup all spawned agents
  subagents list | jq -r '.[].id' | while read agent_id; do
    if [[ $agent_id == council-* ]]; then
      subagents action=kill target="$agent_id"
    fi
  done

  # Log cleanup
  echo "Cleanup completed at $(date -u)" >> workspace/logs/cleanup.log
}

trap cleanup_on_exit EXIT
```

## Multi-Provider Implementation

### Provider Configuration

```bash
# Define available providers
PROVIDERS=(
  "openai:gpt-4"
  "anthropic:claude-3-opus"
  "zai:glm-4.7"
  "google:gemini-pro"
)

get_random_provider() {
  local providers_len=${#PROVIDERS[@]}
  local random_index=$((RANDOM % providers_len))
  echo "${PROVIDERS[$random_index]}"
}
```

### Usage in Council Spawn

```bash
spawn_council_member() {
  local member="$1"
  local transcript="$2"

  local provider_info=$(get_random_provider)
  local provider=$(echo "$provider_info" | cut -d: -f1)
  local model=$(echo "$provider_info" | cut -d: -f2)

  sessions_spawn \
    runtime=acp \
    agentId="council-${member}" \
    model="${provider}/${model}" \
    task="${transcript}" \
    mode=run \
    timeoutSeconds=90
}
```

## Testing

### Unit Tests

Test individual agent prompts:

```bash
test_agent_prompt() {
  local agent_id="$1"
  local test_input="$2"

  sessions_spawn \
    runtime=acp \
    agentId="$agent_id" \
    task="${test_input}" \
    mode=run \
    timeoutSeconds=60
}
```

### Integration Tests

Test full debate flow:

```bash
test_debate_flow() {
  local topic="Test topic for integration testing"

  # Start debate
  sessions_spawn \
    runtime=acp \
    agentId=council-referee \
    task="Test debate: ${topic}" \
    mode=session \
    thread=true

  # Verify outcome generated
  # Verify cleanup completed
  # Verify metrics updated
}
```

## Troubleshooting

### Agent Not Spawning

```bash
# Check agent configuration
cat workspace/agents/referee.json

# Check agent exists
agents_list

# Test spawn manually
sessions_spawn runtime=acp agentId=council-referee task="test" mode=run
```

### Cleanup Failing

```bash
# List active subagents
subagents list

# Kill specific agent
subagents action=kill target=council-logician

# Force cleanup all council agents
subagents list | jq -r '.[].id' | grep council- | while read id; do
  subagents action=kill target="$id"
done
```

### Context Not Clearing

```bash
# Check session status
sessions_list

# Kill session manually
# (Use OpenClaw session management tools)
```

## Next Steps

1. **Setup agents** - Create agent IDs and configure prompts
2. **Implement orchestrator** - Build referee agent with full debate flow
3. **Test end-to-end** - Run test debates and verify all components
4. **Monitor metrics** - Set up metrics tracking and dashboards
5. **Optimize** - Analyze performance and tune prompts/providers

## Resources

- OpenClaw Documentation: `~/.npm-global/lib/node_modules/openclaw/docs`
- ACP Guide: Check OpenClaw docs for ACP runtime details
- SKILL.md: Full skill documentation in `skills/council-of-wisdom/SKILL.md`

---

**For implementation support, refer to the main SKILL.md and use OpenClaw's `sessions_spawn` documentation.**
