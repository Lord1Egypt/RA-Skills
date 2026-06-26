---
name: placed-interview-coach
description: This skill should be used when the user wants to "practice interview", "mock interview", "prepare for interview", "system design interview", "behavioral interview", "STAR stories", "interview coaching", "get interview questions", or wants to prepare for technical interviews using the Placed career platform at placed.exidian.tech.
version: 1.0.0
metadata:
  { "openclaw": { "emoji": "🎯", "homepage": "https://placed.exidian.tech" } }
tags: "interview,interview-prep,mock-interview,behavioral-interview,system-design-interview,star-method,interview-questions,interview-coaching,technical-interview,placed,exidian,career"
---

# Placed Interview Coach

AI-powered interview preparation via the Placed API. No MCP server required — all calls are made directly with curl.

## API Key

Load the key from `~/.config/placed/credentials`, falling back to the environment:

```bash
if [ -z "$PLACED_API_KEY" ] && [ -f "$HOME/.config/placed/credentials" ]; then
  source "$HOME/.config/placed/credentials"
fi
```

If `PLACED_API_KEY` is still not set, ask the user:

> "Please provide your Placed API key (get it at https://placed.exidian.tech/settings/api)"

Then save it for future sessions:

```bash
mkdir -p "$HOME/.config/placed"
echo "export PLACED_API_KEY=<key_provided_by_user>" > "$HOME/.config/placed/credentials"
export PLACED_API_KEY=<key_provided_by_user>
```

## How to Call the API

```bash
placed_call() {
  local tool=$1
  local args=${2:-'{}'}
  curl -s -X POST https://placed.exidian.tech/api/mcp \
    -H "Authorization: Bearer $PLACED_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$tool\",\"arguments\":$args}}" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result']['content'][0]['text'])"
}
```

## Available Tools

| Tool                         | Description                                  |
| ---------------------------- | -------------------------------------------- |
| `start_interview_session`    | Begin a mock interview for a specific role   |
| `continue_interview_session` | Submit your answer and get the next question |
| `get_interview_feedback`     | Get full performance analysis for a session  |
| `list_interview_cases`       | Browse system design cases                   |
| `start_system_design`        | Start a system design interview              |
| `get_behavioral_questions`   | Get STAR-format behavioral questions         |
| `save_story_to_bank`         | Save a STAR story for reuse                  |
| `get_interview_questions`    | Generate likely questions for a role/company |

## Usage Examples

**Start a mock interview:**

```bash
placed_call "start_interview_session" '{
  "resume_id": "res_abc123",
  "job_title": "Senior Software Engineer",
  "difficulty": "hard",
  "company": "Google"
}'
# Returns: session_id + first question
```

**Answer a question:**

```bash
placed_call "continue_interview_session" '{
  "session_id": "sess_abc123",
  "user_answer": "I would approach this by first clarifying requirements..."
}'
# Returns: feedback on your answer + next question
```

**Get session feedback:**

```bash
placed_call "get_interview_feedback" '{"session_id":"sess_abc123"}'
```

**List system design cases:**

```bash
placed_call "list_interview_cases"
# Returns: Design Twitter, Design URL Shortener, Design Netflix, Design Uber, etc.
```

**Start a system design interview:**

```bash
placed_call "start_system_design" '{"case_id":"design-twitter","difficulty":"senior"}'
```

**Get behavioral questions:**

```bash
placed_call "get_behavioral_questions" '{
  "target_role": "Engineering Manager",
  "focus_categories": ["leadership", "conflict-resolution", "failure"]
}'
```

**Save a STAR story:**

```bash
placed_call "save_story_to_bank" '{
  "situation": "Led team through major refactor",
  "task": "Reduce technical debt while shipping features",
  "action": "Created phased plan, mentored junior devs, set clear milestones",
  "result": "30% faster deployments, reduced bugs by 25%",
  "category": "leadership"
}'
```

## Interview Types

### Technical (Coding)

- Difficulty: `easy`, `medium`, `hard`
- Clarify requirements → code → explain trade-offs → test with examples

### System Design

Framework: Requirements → High-Level Architecture → Database Design → Scalability → Fault Tolerance → Trade-offs

### Behavioral

Use the **STAR method** for every answer:

- **Situation** — Context and background
- **Task** — Your responsibility
- **Action** — What you specifically did
- **Result** — Outcome with metrics

## Tips

- Think out loud during technical interviews — explain your reasoning
- Start system design with constraints and scale requirements
- Use specific metrics in STAR answers ("reduced latency by 40%")
- Save strong stories to the bank so they're reusable across interviews
- Practice the same case at different difficulty levels to build confidence
