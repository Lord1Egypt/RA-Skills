## Agents

oh-my-openagent provides 11 specialized agents. Each has a default model, fallback chain, and specific role.

### Sisyphus (Main Orchestrator)

- Default model: claude-opus-4-6
- Fallback chain: glm-5 → big-pickle
- Role: Primary agent the user interacts with. Orchestrates work by delegating to other agents. Parses implicit requirements, assesses codebase maturity, delegates specialized work.
- Key behaviors: Creates todo lists for multi-step tasks, fires explore/librarian agents in background, delegates frontend to visual-engineering category, consults Oracle for architecture decisions.

### Hephaestus (Deep Worker)

- Default model: gpt-5.3-codex
- Fallback chain: none (GPT required)
- Role: Heavy implementation agent for code-intensive tasks. Used via `/start-work` command with Prometheus plans.
- Variant: medium

### Oracle (Architecture Consultant)

- Default model: gpt-5.4
- Fallback chain: gemini-3.1-pro → claude-opus-4-6
- Role: Read-only, expensive, high-quality reasoning model. Consultation only — never writes code directly.
- When to use: Complex architecture design, 2+ failed fix attempts, unfamiliar code patterns, security/performance concerns, multi-system tradeoffs, self-review after significant work.
- When NOT to use: Simple file operations, first attempt at any fix, questions answerable from code already read, trivial decisions.

### Librarian (Reference Search)

- Default model: gemini-3-flash
- Fallback chain: minimax-m2.5-free → big-pickle
- Role: External reference search agent. Searches documentation, OSS repos, web resources.
- Always runs in background (`run_in_background=true`)
- Trigger phrases: "How do I use [library]?", "What's the best practice for [feature]?", "Find examples of [library] usage"

### Explore (Codebase Grep)

- Default model: grok-code-fast-1
- Fallback chain: minimax-m2.5-free → claude-haiku-4-5 → gpt-5-nano
- Role: Fast internal codebase search. Use as a peer tool, not a fallback.
- Always runs in background (`run_in_background=true`)
- Use when: Multiple search angles needed, unfamiliar module structure, cross-layer pattern discovery.

### Multimodal-Looker (Vision)

- Default model: gpt-5.3-codex
- Fallback chain: k2p5 → gemini-3-flash → glm-4.6v → gpt-5-nano
- Role: Analyzes images, PDFs, diagrams, screenshots. Called via `look_at` tool.

### Prometheus (Planner)

- Default model: claude-opus-4-6
- Fallback chain: gpt-5.4 → gemini-3.1-pro
- Role: Creates detailed work plans. Used via `/start-work` command flow.

### Metis (Plan Consultant)

- Default model: claude-opus-4-6
- Fallback chain: gpt-5.4 → gemini-3.1-pro
- Role: Pre-planning consultant. Analyzes requests to identify hidden intentions, ambiguities, and AI failure points. Invoked before Prometheus for complex tasks.

### Momus (Plan Reviewer)

- Default model: gpt-5.4
- Fallback chain: claude-opus-4-6 → gemini-3.1-pro
- Role: Expert reviewer for evaluating work plans against clarity, verifiability, and completeness standards. Invoked after Prometheus creates a plan.

### Atlas (Todo Orchestrator)

- Default model: claude-sonnet-4-6
- Fallback chain: gpt-5.4
- Role: Manages todo list continuation. Monitors completed tasks and continues work automatically.

### Sisyphus-Junior (Delegated Worker)

- Default model: category-dependent (automatic)
- Role: Executes delegated tasks from Sisyphus. Model is determined by the category parameter in `task()`.

## Agent configuration options

All agents support these override options in `oh-my-opencode.json`:

| Option | Type | Description |
|--------|------|-------------|
| model | string | Override default model |
| fallback_models | string[] | Override fallback chain |
| temperature | number | Sampling temperature |
| top_p | number | Nucleus sampling |
| prompt | string | Replace entire system prompt |
| prompt_append | string | Append to system prompt |
| tools | string[] | Restrict available tools |
| disable | boolean | Disable the agent entirely |
| mode | string | Agent mode |
| color | string | TUI display color |
| permission | object | Permission overrides |
| category | string | Default category |
| variant | string | Cost variant (low/medium/high/xhigh/max) |
| maxTokens | number | Max output tokens |
| thinking | boolean | Enable extended thinking |
| reasoningEffort | string | Reasoning effort level |
| textVerbosity | string | Output verbosity |
| providerOptions | object | Provider-specific options |

Example:
```json
{
  "agents": {
    "oracle": {
      "model": "claude-opus-4-6",
      "temperature": 0.3,
      "thinking": true
    },
    "explore": {
      "model": "gemini-3-flash",
      "fallback_models": ["gpt-5-nano"]
    }
  }
}
```
