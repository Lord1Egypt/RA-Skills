# Agents — Register, List, and Switch Agents

Manage agents registered on the server. An agent must exist before running any other command.

## Register an agent

```bash
lobstercash agents register --name "<name>" [--description "<desc>"] [--image-url "<url>"]
```

Registers a new agent on the server and sets it as the active agent locally.

- `--name` **(required)** — A **unique, descriptive, human-readable display name**. Use natural casing with spaces, not dashes. Do **not** use generic names like `"My Agent"` or `"Assistant"`.
- `--description` **(recommended)** — A short summary of what the agent does. This is shown to the user during approval.
- `--image-url` **(recommended)** — An avatar or logo URL for the agent. This is displayed alongside the agent's name in the dashboard and approval screens. Preset logos for well-known agents are hosted at `https://lobster.cash/agent-avatars/`:

  | Agent       | URL                                                  |
  | ----------- | ---------------------------------------------------- |
  | Claude Code | `https://lobster.cash/agent-avatars/claude-code.svg` |
  | Cursor      | `https://lobster.cash/agent-avatars/cursor.svg`      |
  | Codex       | `https://lobster.cash/agent-avatars/codex.svg`       |
  | Gemini      | `https://lobster.cash/agent-avatars/gemini.svg`      |
  | OpenClaw    | `https://lobster.cash/agent-avatars/openclaw.svg`    |

  Use a URL from this table, a URL the user explicitly provided, or omit `--image-url` entirely. Do **not** invent or guess image URLs — a broken avatar is worse than no avatar.

- `--network` **(optional)** — The blockchain the agent will operate on. Defaults to `base`. Accepts `base` or `solana`. **Most users should not change this.** Only pass `--network solana` when the user has explicitly asked for Solana, or when the context clearly implies the agent needs to operate on Solana (e.g. the task is to use a Solana-only integration like Jupiter or xStocks). See [Advanced: choosing a non-default chain](#advanced-choosing-a-non-default-chain).

#### Choosing a good name

Pick the name that will be most recognizable to the user on the dashboard and in approval prompts. Use your judgment — there is no single formula.

- **If you have a well-known identity, prefer that.** Agents with established names should use them: `"Claude Code"`, `"Devin"`, `"Cline"`, `"OpenClaw"`, or whatever the user already knows you as. If the user has configured a custom display name for you, use that.
- **If a task-specific name is more useful, use that instead.** When you are purpose-built for a particular job — shopping, research, scheduling — a descriptive name like `"Alice's Shopping Assistant"` or `"Travel Planner"` may be clearer than a generic runtime name.
- **When in doubt, combine both.** Something like `"Claude Code — Research"` works if you want to convey both identity and purpose.

The goal: when the user sees the name on an approval screen, they should immediately know _which agent_ is asking and _what it does_.

Examples:

```bash
lobstercash agents register \
  --name "Claude Code" \
  --description "Anthropic's AI coding agent" \
  --image-url "https://lobster.cash/agent-avatars/claude-code.svg"

lobstercash agents register \
  --name "Alice's Shopping Assistant" \
  --description "Finds deals and buys products for Alice" \
  --image-url "https://example.com/alice-avatar.png"
```

Example output:

```
Agent registered and set as active.
  ID:     a1b2c3d4-5678-90ab-cdef-1234567890ab
  Name:   Shopping Assistant
  Desc:   Finds deals and buys products
  Key:    5Xyz...abc
```

#### Advanced: choosing a non-default chain

Agents default to Base. Do **not** ask the user which chain they want — just register on Base silently. Only pass `--network solana` when the user has explicitly told you they need Solana, or when the context clearly implies the agent must operate on Solana (for example, the task the user described can only be completed through a Solana-native integration).

Pick `solana` only when:

- The user already holds USDC on Solana and wants the agent to use those funds.
- The integration the user wants is Solana-only (e.g. Jupiter swaps, xStocks).
- The user explicitly asks for Solana.

The chain is **fixed for the lifetime of the agent**. To switch chains later, the user must register a new agent with a different `--network`. Existing agents cannot be migrated.

Example:

```bash
lobstercash agents register \
  --name "Solana Trading Bot" \
  --description "Trades tokenized stocks on Jupiter" \
  --image-url "https://lobster.cash/agent-avatars/claude-code.svg" \
  --network solana
```

### When to use

- First-time setup before any wallet or payment command.
- When the user wants to register a new agent identity.

## List agents

```bash
lobstercash agents list
```

Shows all agents with their metadata from the server. Also resolves any pending setup sessions automatically.

Example output:

```
Agents:

  a1b2c3d4-5678-90ab-cdef-1234567890ab (active)
    Name:   Shopping Assistant
    Desc:   Finds deals and buys products
    Key:    5Xyz...abc
    Status: active

  e5f6a7b8-9012-34cd-ef56-7890abcdef12
    Name:   Research Bot
    Key:    7Abc...xyz
    Status: pairing
```

### When to use

- Before any operation, to confirm an agent exists.
- When the user asks "which agents do I have?" or "what's my agent ID?"
- To check and resolve pending setup sessions.

## Set active agent

```bash
lobstercash agents set-active <agentId>
```

Sets a different agent as active. All subsequent commands operate on the newly selected agent's wallet.

Example output:

```
Active agent set to "e5f6a7b8-9012-34cd-ef56-7890abcdef12".
```

### When to use

- When the user wants to operate a different agent's wallet.
- In multi-agent scenarios where the user needs to change the active agent.

## Concurrent agents (`LOBSTER_AGENT_ID`)

When running multiple agents in parallel (e.g. two terminals), set the `LOBSTER_AGENT_ID` environment variable to avoid conflicts with the shared active agent:

```bash
export LOBSTER_AGENT_ID="<agentId>"
```

This overrides `agents set-active` for the current shell session. All commands in that terminal will use the specified agent regardless of what `activeAgentId` is set to in `agents.json`.

After registering an agent, set this env var immediately to pin the session to that agent.
