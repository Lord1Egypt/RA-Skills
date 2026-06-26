# Observation Taxonomy — Complete Reference

This document defines every dimension UxrObserver must capture. The observer must classify every interaction against this taxonomy.

## 1. Use Case & Task Tracking

This is the backbone of the study. Every interaction is a use case instance.

### Task Categories (living taxonomy — add new categories as patterns emerge)

| Category | Description | Examples |
|----------|-------------|----------|
| `coding` | Writing, debugging, refactoring, reviewing code | "Fix this bug", "Write a Python script", "Refactor this function" |
| `writing` | Documents, emails, reports, creative writing, editing | "Draft a blog post", "Edit this memo", "Write a cover letter" |
| `research` | Web search, information synthesis, fact-finding | "What's the latest on X?", "Compare A vs B", "Find me sources" |
| `file_creation` | Spreadsheets, presentations, PDFs, Word docs | "Make me a slide deck", "Create a spreadsheet", "Generate a PDF" |
| `data_analysis` | CSV processing, visualization, statistical analysis | "Analyze this CSV", "Chart these numbers", "What's the trend?" |
| `planning` | Project planning, brainstorming, decision-making | "Help me plan this project", "Brainstorm ideas for X" |
| `conversation` | Casual chat, rubber-ducking, thinking out loud | "What do you think about X?", "Let me think through this" |
| `system_configuration` | Setting up OpenClaw, installing skills, configuring models | "Install this skill", "Change my model", "Set up MCP" |
| `automation` | Building workflows, creating skills, scripting | "Create a skill for X", "Automate this process" |
| `learning` | How things work, tutorials, concept exploration | "How does X work?", "Teach me about Y", "Explain this concept" |
| `debugging_openclaw` | Troubleshooting OpenClaw itself | "Why isn't this working?", "The skill isn't triggering" |
| `communication` | Drafting messages, emails, Slack messages | "Write an email to my team", "Draft a Slack message" |
| `image_generation` | Creating or editing images, diagrams | "Generate an image of X", "Create a diagram" |
| `other` | Anything unclassifiable — log it and let patterns emerge | — |

### Task Metadata

- **Complexity:** `trivial` | `simple` | `moderate` | `complex` | `multi_session`
  - `trivial`: One-shot, instant answer (< 1 tool call)
  - `simple`: Straightforward, 1-3 tool calls
  - `moderate`: Multiple steps, 3-8 tool calls, some back-and-forth
  - `complex`: Many steps, 8+ tool calls, significant reasoning
  - `multi_session`: Spans across multiple conversations
- **Is chain:** Does this task follow from a previous one? Is the user building toward something larger?
- **Chain ID:** If chained, group under a common chain identifier
- **First occurrence:** Is this the first time the user has attempted this category?
- **Frequency rank:** Where does this category rank in the user's overall usage? (updated after each interaction)

### Use Case Frequency Table

Maintain a running frequency table in `~/.uxr-observer/aggregates/use-case-frequency.json`:

```json
{
  "last_updated": "ISO-8601",
  "total_interactions": 142,
  "categories": {
    "coding": { "count": 58, "percentage": 40.8, "trend": "increasing", "last_seen": "ISO-8601" },
    "writing": { "count": 29, "percentage": 20.4, "trend": "stable", "last_seen": "ISO-8601" },
    ...
  },
  "category_history": [
    { "date": "2026-03-01", "coding": 12, "writing": 5, ... },
    { "date": "2026-03-02", "coding": 15, "writing": 8, ... }
  ]
}
```

## 2. User Behavior & Language

### Verbatim Capture

Capture exact words for:
- Every request
- Every reaction (positive, negative, neutral)
- Every correction or redirect
- Every expression of emotion
- Every spontaneous commentary
- Every statement of expectation

Format:
```json
{
  "header": "Researcher-generated interpretive summary",
  "quote": "User's exact words",
  "context": "What was happening when they said this",
  "signal_type": "request | reaction | correction | emotion | expectation | commentary"
}
```

### Prompt Engineering Patterns

Track how the user phrases requests:
- `minimal`: "Fix this" — few words, assumes context
- `detailed_instruction`: Step-by-step directions
- `example_driven`: "Like this... but change X"
- `iterative`: Builds up through multiple turns
- `structured`: Uses bullet points, numbered lists, formatting
- `conversational`: Casual, natural language
- `technical`: Uses jargon, code snippets, precise terminology

Track evolution: Is the user getting more efficient? More detailed? More structured?

### Correction Patterns

When the user corrects OpenClaw:
- **Scope correction:** "No, I meant the whole directory, not just that file"
- **Format correction:** "I wanted a PDF, not markdown"
- **Factual correction:** "That's wrong, the API uses POST not GET"
- **Intent correction:** "That's not what I asked for — I wanted X not Y"
- **Style correction:** "Make it more formal" / "Too verbose"
- **Precision correction:** "Use the exact numbers, don't round"

### Sentiment Tracking

Per-interaction sentiment:
| Signal | Indicators |
|--------|-----------|
| `delighted` | Explicit praise, "this is great!", enthusiasm, surprise |
| `positive` | Thanks, acceptance, moves on smoothly |
| `neutral` | Acknowledges without strong signal |
| `frustrated` | Short replies, "no", repeated corrections |
| `confused` | "I don't understand", questions about what happened |
| `angry` | Strong negative language, capitalization, exclamation |
| `resigned` | "Fine, I'll just do it myself", giving up language |

Track sentiment transitions within a session — when does the arc shift?

### Other User Signals

- **Workarounds:** User manually fixes something the agent should have handled
- **Abandonment:** User gives up — what was the last interaction before quitting?
- **Mental model mismatches:** User expects behavior A, gets behavior B
- **Feature discovery:** User finds a capability they didn't know about
- **Trust calibration:** Does the user verify output? Trust blindly? Change trust over time?

## 3. OpenClaw System Behavior

- **Response approach:** Strategy chosen, was it the right one?
- **Response summary:** Detailed enough for report readers to understand
- **Tools used:** Full list per interaction
- **Tool call count:** Proxy for complexity and inefficiency
- **Errors and retries:** What errored, how did it recover?
- **Hallucinations:** Incorrect information — was it caught?
- **Skills triggered:** Which skills fired, which didn't fire but should have?

## 4. Sub-Agent Architecture

- **Architecture detection:** `single_agent` | `supervisor_worker` | `pipeline` | `parallel_fan_out` | `custom`
- **Architecture description:** Plain-language explanation of the agent graph
- **Delegation patterns:** What gets delegated vs. handled by main agent?
- **Inter-agent communication:** Files? Conversational handoff? Structured data?
- **Sub-agent failures:** Graceful recovery or chain breakage?
- **Architecture evolution:** How does the setup change over time?

## 5. Model & Infrastructure

- **Model identification:** Detect from context (`claude-sonnet-4-5-20250929`, `claude-opus-4-6`, etc.)
- **Model switching:** When and why the user changes models
- **Token estimation:** `(character_count / 4.0)` for rough estimate. Track input, output, tool overhead separately
- **Cost estimation:** Apply model pricing from config. Log with `±20%` range
- **Session duration:** Start/end/active/idle time
- **Skills installed:** Which are active, which fire frequently, which never fire
- **Environment:** Claude.ai | Claude Code | Cowork | Desktop | Mobile

## 6. Fail States & Pain Points

### Failure Taxonomy

| Type | Description |
|------|-------------|
| `tool_error` | Tool call fails (network, permissions, file not found) |
| `misunderstanding` | OpenClaw misinterprets intent |
| `scope_mismatch` | Does too much or too little |
| `format_error` | Wrong output format |
| `hallucination` | Factually incorrect output |
| `loop` | Stuck in retry loop |
| `timeout` | Takes too long |
| `skill_failure` | Skill doesn't trigger or malfunctions |
| `context_loss` | Forgets earlier conversation context |
| `dependency_failure` | External service unavailable |
| `user_confusion` | User doesn't understand what happened |
| `silent_failure` | Something went wrong but nobody noticed |

### Failure Severity

- `minor` — inconvenience, easily worked around
- `moderate` — task degraded but completed
- `severe` — task blocked, required significant recovery
- `critical` — data loss, security concern, or complete breakdown

### Recovery Patterns

- User workaround
- OpenClaw self-correction
- User correction prompts fix
- Retry succeeds
- Abandonment
- Escalation (user seeks help elsewhere)

## 7. Wins & Value Propositions

### Value Categories

| Category | Description |
|----------|-------------|
| `time_saved` | Faster than manual alternatives |
| `quality_improvement` | Output exceeds what user could produce alone |
| `capability_unlock` | Accomplished something impossible without the agent |
| `cognitive_offload` | Handled complexity the user didn't want to think about |
| `learning` | User learned something new |
| `creative_amplification` | Enhanced creative output |

### Magic Moments

When the user expresses genuine surprise or delight — highest-signal data. Log with full context, verbatims, and what specifically caused the reaction.

### Return Patterns

What use cases bring the user back habitually vs. experimentally?

## 8. Session & Longitudinal Patterns

- **Session frequency:** Daily? Multiple/day? Sporadic?
- **Time-of-day patterns:** Peak usage windows
- **Session length trends:** Getting longer or shorter?
- **Skill development:** User getting more efficient? More sophisticated?
- **Feature adoption curve:** Discovery and adoption timeline
- **Churn signals:** Decreasing frequency, shorter sessions, more abandonment
