# SDK Subpath Import Reference

Always import from a focused subpath. Never use `openclaw/plugin-sdk` root barrel.

```typescript
// ✅ Correct
import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

// ❌ Wrong (deprecated, will be removed)
import { definePluginEntry } from "openclaw/plugin-sdk";
```

---

## Plugin Entry

| Subpath | Key exports |
|---|---|
| `plugin-sdk/plugin-entry` | `definePluginEntry`, `type OpenClawPluginApi` |
| `plugin-sdk/core` | `defineChannelPluginEntry`, `createChatChannelPlugin`, `createChannelPluginBase`, `defineSetupPluginEntry`, `buildChannelConfigSchema`, `buildChannelOutboundSessionRoute` |
| `plugin-sdk/provider-entry` | `defineSingleProviderPluginEntry` |

---

## Channel Subpaths

| Subpath | Key exports |
|---|---|
| `plugin-sdk/channel-setup` | `createOptionalChannelSetupSurface` |
| `plugin-sdk/channel-pairing` | `createChannelPairingController` |
| `plugin-sdk/channel-reply-pipeline` | `createChannelReplyPipeline` |
| `plugin-sdk/channel-config-helpers` | `createHybridChannelConfigAdapter` |
| `plugin-sdk/channel-config-schema` | Channel config schema types |
| `plugin-sdk/channel-policy` | `resolveChannelGroupRequireMention` |
| `plugin-sdk/channel-lifecycle` | `createAccountStatusSink` |
| `plugin-sdk/channel-inbound` | Debounce, mention matching, envelope helpers |
| `plugin-sdk/channel-send-result` | Reply result types |
| `plugin-sdk/channel-actions` | `createMessageToolButtonsSchema`, `createMessageToolCardSchema` |
| `plugin-sdk/channel-targets` | Target parsing/matching helpers |
| `plugin-sdk/channel-contract` | Channel contract types (for tests + local helpers) |
| `plugin-sdk/channel-feedback` | Feedback/reaction wiring |
| `plugin-sdk/setup` | `createPromptParsedAllowFromForAccount`, `createTopLevelChannelParsedAllowFromPrompt`, `createNestedChannelParsedAllowFromPrompt`, `createStandardChannelSetupStatus` |
| `plugin-sdk/webhook-ingress` | Webhook request/target helpers |

---

## Provider Subpaths

| Subpath | Key exports |
|---|---|
| `plugin-sdk/provider-auth` | `createProviderApiKeyAuthMethod`, `ensureApiKeyFromOptionEnvOrPrompt`, `upsertAuthProfile` |
| `plugin-sdk/provider-models` | `normalizeModelCompat` |
| `plugin-sdk/provider-catalog` | Catalog type re-exports |
| `plugin-sdk/provider-usage` | `fetchClaudeUsage` and similar |
| `plugin-sdk/provider-stream` | Stream wrapper types |
| `plugin-sdk/provider-onboard` | `createDefaultModelPresetAppliers`, `createDefaultModelsPresetAppliers`, `createModelCatalogPresetAppliers` |

---

## Auth & Security Subpaths

| Subpath | Key exports |
|---|---|
| `plugin-sdk/command-auth` | `resolveControlCommandGate` |
| `plugin-sdk/allow-from` | `formatAllowFromLowercase` |
| `plugin-sdk/secret-input` | Secret input parsing helpers |

---

## Runtime & Storage Subpaths

| Subpath | Key exports |
|---|---|
| `plugin-sdk/runtime-store` | `createPluginRuntimeStore` |
| `plugin-sdk/config-runtime` | Config load/write helpers |
| `plugin-sdk/infra-runtime` | System event/heartbeat helpers |
| `plugin-sdk/agent-runtime` | Agent dir/identity/workspace helpers |
| `plugin-sdk/directory-runtime` | Config-backed directory query/dedup |
| `plugin-sdk/keyed-async-queue` | `KeyedAsyncQueue` |

---

## Capability Subpaths

| Subpath | Key exports |
|---|---|
| `plugin-sdk/image-generation` | Image generation provider types |
| `plugin-sdk/media-understanding` | Media understanding provider types |
| `plugin-sdk/speech` | Speech provider types |

---

## Testing Subpath

| Subpath | Key exports |
|---|---|
| `plugin-sdk/testing` | `installCommonResolveTargetErrorCases`, `shouldAckReaction`, `removeAckReactionAfterReply` |
| `plugin-sdk/testing` (types) | `ChannelAccountSnapshot`, `ChannelGatewayContext`, `OpenClawConfig`, `PluginRuntime`, `RuntimeEnv`, `MockFn` |

---

## api object fields (inside register callback)

| Field | Type | Description |
|---|---|---|
| `api.id` | `string` | Plugin id |
| `api.name` | `string` | Display name |
| `api.version` | `string?` | Plugin version |
| `api.description` | `string?` | Plugin description |
| `api.source` | `string` | Plugin source path |
| `api.rootDir` | `string?` | Plugin root directory |
| `api.config` | `OpenClawConfig` | Full current config snapshot |
| `api.pluginConfig` | `Record<string, unknown>` | Plugin-specific config from `plugins.entries.<id>.config` |
| `api.runtime` | `PluginRuntime` | Runtime helpers namespace |
| `api.logger` | `PluginLogger` | Scoped logger: `.debug()`, `.info()`, `.warn()`, `.error()` |
| `api.registrationMode` | `PluginRegistrationMode` | `"full"`, `"setup-only"`, or `"setup-runtime"` |
| `api.resolvePath(input)` | `(string) => string` | Resolve path relative to plugin root |
