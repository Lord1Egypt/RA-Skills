# Official Documentation Entry Points

Read docs first, source second. For native OpenClaw plugin development, these are the most useful starting points.

## First-line docs

### Getting started and overview

- `docs/plugins/building-plugins.md`
  - first page to read
  - covers the minimum plugin skeleton, `package.json`, `openclaw.plugin.json`, `definePluginEntry(...)`, and `api.registerTool(...)`
- `docs/tools/plugin.md`
  - covers plugin install, enablement, scan order, `openclaw plugins inspect`, and local directory/archive installs

### SDK and registration APIs

- `docs/plugins/sdk-overview.md`
  - use this when deciding which `plugin-sdk/<subpath>` to import from
  - review what `OpenClawPluginApi` exposes through `register*` and `on(...)`
- `docs/plugins/sdk-entrypoints.md`
  - review `definePluginEntry`, `defineChannelPluginEntry`, `defineSetupPluginEntry`
  - review `registrationMode`
- `docs/plugins/sdk-runtime.md`
  - review what `api.runtime.*` can do

### Manifest, skills, and commands

- `docs/plugins/manifest.md`
  - check legal `openclaw.plugin.json` fields
  - verify whether `skills`, `configSchema`, or `uiHints` belong there
- `docs/tools/skills.md`
  - check supported skill frontmatter fields
  - review `user-invocable`, `command-dispatch: tool`, and `command-tool`
- `docs/tools/slash-commands.md`
  - review skill-command behavior and surface differences
- `docs/tools/index.md`
  - review the big picture for tool policy
  - understand `tools.profile`, `tools.allow`, and `tools.deny`
- `docs/gateway/configuration-reference.md`
  - use this for field-level config semantics
  - especially important for `tools.profile`, `tools.allow`, `tools.alsoAllow`, and `tools.byProvider`

### Testing and internal mechanics

- `docs/plugins/sdk-testing.md`
  - review plugin test guidance, scoped test commands, and repo-side constraints
- `docs/automation/hooks.md`
  - review hook intent layers and runtime semantics
  - good for navigation; field-level details still come from `src/plugins/types.ts`
- `docs/plugins/architecture.md`
  - especially useful when something “looks correct but still does not work”
  - explains the capability model, registry, legacy hooks, and load pipeline

## Public docs URLs

If you need public docs links, prefer these:

- `https://docs.openclaw.ai/plugins/building-plugins`
- `https://docs.openclaw.ai/plugins/sdk-overview`
- `https://docs.openclaw.ai/plugins/sdk-entrypoints`
- `https://docs.openclaw.ai/plugins/sdk-runtime`
- `https://docs.openclaw.ai/plugins/sdk-testing`
- `https://docs.openclaw.ai/plugins/manifest`
- `https://docs.openclaw.ai/tools/plugin`
- `https://docs.openclaw.ai/tools/skills`
- `https://docs.openclaw.ai/tools/slash-commands`
- `https://docs.openclaw.ai/tools`
- `https://docs.openclaw.ai/gateway/configuration-reference`
- `https://docs.openclaw.ai/automation/hooks`
- `https://docs.openclaw.ai/plugins/architecture`

## Most important source entrypoints

When docs are not specific enough and a local repo checkout is available, inspect these repo sources first:

- `src/plugins/registry.ts`
  - how plugin capabilities are recorded in the registry
- `src/plugins/tools.ts`
  - how plugin tools are resolved, filtered, and injected
- `src/plugins/types.ts`
  - authoritative typed-hook names, event structures, and return types
- `src/agents/pi-tools.ts`
  - how the final agent tool set is constructed and filtered by policy
- `src/agents/tool-catalog.ts`
  - what each `tools.profile` base allowlist contains
- `src/auto-reply/reply/get-reply-inline-actions.ts`
  - how skill commands are rewritten into normal agent requests or routed through `command-dispatch: tool`

## Recommended reading order

1. `docs/plugins/building-plugins.md`
2. `docs/plugins/sdk-overview.md`
3. `docs/plugins/manifest.md`
4. Then branch by task:
   - hook work: `docs/plugins/sdk-entrypoints.md` + `src/plugins/types.ts`
   - tool policy: `docs/tools/index.md` + `docs/gateway/configuration-reference.md`
   - skill / slash command work: `docs/tools/skills.md` + `docs/tools/slash-commands.md`
   - testing: `docs/plugins/sdk-testing.md`
   - difficult debugging: `docs/plugins/architecture.md`
