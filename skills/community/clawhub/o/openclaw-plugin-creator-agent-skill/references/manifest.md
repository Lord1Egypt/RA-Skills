# Plugin Manifest (openclaw.plugin.json) — Complete Reference

Every native OpenClaw plugin MUST have this file in the plugin root.
OpenClaw reads it to validate config WITHOUT executing plugin code.

---

## Minimal valid manifest

```json
{
  "id": "my-plugin",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

## Full manifest example (provider with API key auth)

```json
{
  "id": "openrouter",
  "name": "OpenRouter",
  "description": "OpenRouter provider plugin",
  "version": "1.0.0",
  "providers": ["openrouter"],
  "providerAuthEnvVars": {
    "openrouter": ["OPENROUTER_API_KEY"]
  },
  "providerAuthChoices": [
    {
      "provider": "openrouter",
      "method": "api-key",
      "choiceId": "openrouter-api-key",
      "choiceLabel": "OpenRouter API key",
      "groupId": "openrouter",
      "groupLabel": "OpenRouter",
      "optionKey": "openrouterApiKey",
      "cliFlag": "--openrouter-api-key",
      "cliOption": "--openrouter-api-key <key>",
      "cliDescription": "OpenRouter API key",
      "onboardingScopes": ["text-inference"]
    }
  ],
  "uiHints": {
    "apiKey": {
      "label": "API key",
      "placeholder": "sk-or-v1-...",
      "sensitive": true,
      "help": "From your OpenRouter dashboard"
    }
  },
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "apiKey": { "type": "string" }
    }
  }
}
```

## Channel manifest example

```json
{
  "id": "my-channel",
  "name": "My Channel",
  "kind": "channel",
  "channels": ["my-channel"],
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

## Memory/context-engine manifest

```json
{
  "id": "my-memory",
  "kind": "memory",
  "configSchema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {}
  }
}
```

---

## Top-level field reference

| Field | Required | Type | Description |
|---|---|---|---|
| `id` | ✅ | `string` | Canonical plugin id — matches `plugins.entries.<id>` in config |
| `configSchema` | ✅ | JSON Schema object | Config validation schema — even if no config, must be present |
| `name` | No | `string` | Human-readable plugin name |
| `description` | No | `string` | Short summary shown in plugin surfaces |
| `version` | No | `string` | Informational version |
| `enabledByDefault` | No | `true` | Marks a bundled plugin as enabled by default |
| `kind` | No | `"memory"` \| `"context-engine"` | Declares exclusive plugin kind for `plugins.slots.*` |
| `channels` | No | `string[]` | Channel ids owned by this plugin |
| `providers` | No | `string[]` | Provider ids owned by this plugin |
| `providerAuthEnvVars` | No | `Record<string, string[]>` | Env var names for auth probes (no plugin code needed) |
| `providerAuthChoices` | No | `object[]` | Auth choice metadata for onboarding pickers |
| `skills` | No | `string[]` | Skill directories to load (relative to plugin root) |
| `uiHints` | No | `Record<string, object>` | UI labels, placeholders, and sensitivity hints |

---

## providerAuthChoices field reference

| Field | Required | Type | Description |
|---|---|---|---|
| `provider` | ✅ | `string` | Provider id this choice belongs to |
| `method` | ✅ | `string` | Auth method id to dispatch to |
| `choiceId` | ✅ | `string` | Stable auth-choice id for onboarding and CLI flows |
| `choiceLabel` | No | `string` | User-facing label (falls back to `choiceId`) |
| `choiceHint` | No | `string` | Short helper text for the picker |
| `groupId` | No | `string` | Group id for grouping related choices |
| `groupLabel` | No | `string` | User-facing label for the group |
| `groupHint` | No | `string` | Short helper text for the group |
| `optionKey` | No | `string` | Internal option key for simple one-flag auth flows |
| `cliFlag` | No | `string` | CLI flag name, e.g. `--openrouter-api-key` |
| `cliOption` | No | `string` | Full CLI option shape, e.g. `--openrouter-api-key <key>` |
| `cliDescription` | No | `string` | Description used in CLI help |
| `onboardingScopes` | No | `Array<"text-inference" \| "image-generation">` | Which onboarding surfaces this choice appears in (default: `["text-inference"]`) |

---

## uiHints field reference

```json
{
  "uiHints": {
    "fieldName": {
      "label": "Display label",
      "help": "Short helper text",
      "placeholder": "e.g. sk-...",
      "sensitive": true,
      "advanced": false,
      "tags": ["optional"]
    }
  }
}
```

| Field | Type | Description |
|---|---|---|
| `label` | `string` | User-facing field label |
| `help` | `string` | Short helper text shown below field |
| `placeholder` | `string` | Placeholder text for form inputs |
| `sensitive` | `boolean` | Marks field as secret (masked in UI) |
| `advanced` | `boolean` | Marks field as advanced (collapsed by default) |
| `tags` | `string[]` | Optional UI tags |

---

## Validation rules

- `channels.*` keys that match no plugin manifest → **error**
- `plugins.entries.<id>`, `plugins.allow`, `plugins.deny`, `plugins.slots.*` must reference discoverable ids → **error** for unknown ids
- Broken or missing manifest → validation fails, Doctor reports error
- Disabled plugin config → **preserved**, warning surfaced in Doctor + logs
- `openclaw doctor --fix` → removes stale channel/plugin entries automatically

## What goes where

| Need | Put it in |
|---|---|
| OpenClaw must know before loading plugin code | `openclaw.plugin.json` |
| npm metadata, dependency installation, entry files | `package.json` |
| Runtime behavior, tool registration, channel logic | Plugin TypeScript code |
