# Edicts

Ground truth for AI agents.

Edicts is a small TypeScript library for storing cheap, verified facts that your agent should treat as non-negotiable. Instead of stuffing long documents into every prompt or building a full retrieval stack for a handful of critical facts, you keep a compact set of assertions in YAML or JSON, render them into prompt context, and give agents optional tool access for runtime reads and updates.

Docs: https://edicts.ai  
License: MIT

## The problem

Agents are surprisingly good at sounding certain about things they should never improvise: launch dates, product limitations, compliance constraints, internal naming, migration status, embargoes, and "definitely not" statements. Those facts are usually tiny, high-value, and expensive to get wrong. Edicts gives you a lightweight ground-truth layer for exactly that class of information.

## 30-second quick start

Install the package:

```bash
npm install edicts
```

Create an edicts file:

```bash
npx edicts init
# Creates ./edicts.yaml with a starter template
```

Or write one manually:

```yaml
version: 1
edicts:
  - text: "Product v2.0 launches April 15, NOT before."
    category: product
    confidence: verified
    ttl: event
    expiresAt: "2026-04-16"
```

List it with the CLI:

```bash
npx edicts list
```

Use it in your system prompt:

```ts
import { EdictStore } from 'edicts';

const store = new EdictStore({ path: './edicts.yaml' });
await store.load();

const edicts = await store.all();
const rules = edicts.map(e => `- [${e.category}] ${e.text}`).join('\n');

const systemPrompt = `You are a helpful assistant.

## Standing Rules
${rules}`;
```

That is the whole idea: small verified facts, cheap enough to include all the time.

## Why Edicts?

- **Built for high-value facts, not conversational memory.** Edicts is for "this is true" and "this is not true," not giant transcript recall.
- **Tiny context footprint.** A few critical edicts cost tens of tokens, not thousands.
- **Time-aware by default.** Ephemeral and event-based facts expire automatically.
- **Framework-agnostic.** Use it with any LLM stack that can prepend text or expose tools.
- **Simple storage.** YAML or JSON on disk, atomic writes, optimistic concurrency, minimal dependencies.

## Key features

- YAML and JSON storage
- Automatic expiry pruning on load/render
- Sequential IDs (`e_001`, `e_002`) or stable user-provided keys
- Key-based supersession for facts that change over time
- Token budget enforcement with rollback on overflow
- Category allowlists and category soft limits
- Built-in plain, markdown, and JSON renderers
- Optional custom tokenizer and custom renderer hooks
- Full CLI for all store operations
- First-party [OpenClaw plugin](https://www.npmjs.com/package/openclaw-plugin-edicts) for automatic prompt injection

## Installation

```bash
npm install edicts
```

For CLI usage, install globally:

```bash
npm install -g edicts
```

Requirements:

- Node.js >= 20
- TypeScript recommended, but not required

## Core API

```ts
import { EdictStore } from 'edicts';

const store = new EdictStore({
  path: './edicts.yaml',
  tokenBudget: 4000,
  categories: ['product', 'compliance', 'operations'],
});

await store.load();

await store.add({
  text: 'The public launch date is April 15, NOT earlier.',
  category: 'product',
  confidence: 'verified',
  ttl: 'event',
  expiresAt: '2026-04-16T00:00:00.000Z',
});

const edicts = await store.all();
const stats = await store.stats();
```

The primary interface is the `EdictStore` class. See the full [API reference](https://edicts.ai/docs/reference/api/).

## CLI

The CLI covers all store operations:

```bash
edicts init                          # Bootstrap edicts.yaml
edicts add --text "..." --category product  # Add an edict
edicts list                          # List active edicts
edicts get <id>                      # Get a single edict
edicts remove <id>                   # Remove an edict
edicts update <id> --text "..."      # Update an edict
edicts search <query>                # Search by text
edicts stats                         # Store statistics
edicts review                        # Health check (stale, expiring)
edicts export --output backup.yaml   # Export store
edicts import backup.yaml            # Import from file
```

Full [CLI reference](https://edicts.ai/docs/reference/cli/).

## OpenClaw integration

If you use [OpenClaw](https://openclaw.ai), install the plugin for automatic prompt injection:

```bash
openclaw plugins install openclaw-plugin-edicts
openclaw gateway restart
```

Every agent session will automatically receive your edicts as ground truth — no code changes needed. The plugin also registers tools so agents can read, create, and manage edicts at runtime.

See the [OpenClaw integration guide](https://edicts.ai/docs/integrations/openclaw/).

## Documentation

Full docs at **https://edicts.ai**:

- [Installation](https://edicts.ai/docs/getting-started/installation/)
- [Quick Start](https://edicts.ai/docs/getting-started/quick-start/)
- [Best Practices](https://edicts.ai/docs/guides/best-practices/)
- [Memory Hierarchy](https://edicts.ai/docs/guides/memory-hierarchy/)
- [Configuration](https://edicts.ai/docs/reference/configuration/)
- [YAML Schema](https://edicts.ai/docs/reference/yaml-schema/)
- [API Reference](https://edicts.ai/docs/reference/api/)
- [CLI Reference](https://edicts.ai/docs/reference/cli/)
- [Generic Integration](https://edicts.ai/docs/integrations/generic/)
- [OpenClaw Integration](https://edicts.ai/docs/integrations/openclaw/)

## Security and Trust Model

Edicts injects content into your agent's system prompt. This is the core feature — it's how ground truth reaches the model. Here's how trust works:

**You control what gets injected.** Edicts are stored in a local YAML or JSON file in your workspace. Only content you (or your agent, if you grant tool access) write to that file appears in prompts. There is no remote fetch, no external data source, and no network calls — it's your file, your facts, your system prompt.

**Runtime tools are opt-in and configurable.** The OpenClaw plugin exposes tools that let agents add, update, and remove edicts at runtime. This is powerful (agents can establish persistent ground truth) but also a privileged capability. You can:

- **Disable write tools entirely:** set `tools.enabled: false` in plugin config
- **Whitelist specific tools:** use `tools.names` to allow only read operations (`edicts_list`, `edicts_search`, `edicts_stats`)
- **Disable auto-save:** set `autoSave: false` so runtime changes don't persist across sessions
- **Disable context injection:** set `includeSystemContext: false` to use tools without prompt injection
- **Audit edicts regularly:** use `edicts review` (CLI or tool) to catch stale or suspicious entries

**If you don't trust runtime mutation, don't enable it.** The safest configuration is `tools.enabled: false` with `autoSave: false` — edicts are injected from your curated file, and nothing can modify them at runtime. Enable write tools only when you want agents to establish persistent facts (e.g., learning user preferences, recording decisions).

## Contributing

PRs are welcome. Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before sending changes.

## License

MIT
