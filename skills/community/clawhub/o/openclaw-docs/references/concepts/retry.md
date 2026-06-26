# Retry Policy

Source: https://docs.openclaw.ai/concepts/retry

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationMessages and deliveryRetry PolicyGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpFundamentals
Gateway ArchitectureAgent RuntimeAgent LoopSystem PromptContextAgent WorkspaceOAuth
Bootstrapping
Bootstrapping
Sessions and memory
Session ManagementSessionsSession PruningSession ToolsMemoryCompaction
Multi-agent
Multi-Agent RoutingPresence
Messages and delivery
MessagesStreaming and ChunkingRetry PolicyCommand Queue
On this page
- [Retry policy](#retry-policy)
- [Goals](#goals)
- [Defaults](#defaults)
- [Behavior](#behavior)
- [Discord](#discord)
- [Telegram](#telegram)
- [Configuration](#configuration)
- [Notes](#notes)

​Retry policy
​Goals

- Retry per HTTP request, not per multi-step flow.

- Preserve ordering by retrying only the current step.

- Avoid duplicating non-idempotent operations.

​Defaults

- Attempts: 3

- Max delay cap: 30000 ms

- Jitter: 0.1 (10 percent)

Provider defaults:

- Telegram min delay: 400 ms

- Discord min delay: 500 ms

​Behavior
​Discord

- Retries only on rate-limit errors (HTTP 429).

- Uses Discord `retry_after` when available, otherwise exponential backoff.

​Telegram

- Retries on transient errors (429, timeout, connect/reset/closed, temporarily unavailable).

- Uses `retry_after` when available, otherwise exponential backoff.

- Markdown parse errors are not retried; they fall back to plain text.

​Configuration
Set retry policy per provider in `~/.openclaw/openclaw.json`:
Copy```
{
  channels: {
    telegram: {
      retry: {
        attempts: 3,
        minDelayMs: 400,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
    discord: {
      retry: {
        attempts: 3,
        minDelayMs: 500,
        maxDelayMs: 30000,
        jitter: 0.1,
      },
    },
  },
}

```

​Notes

- Retries apply per request (message send, media upload, reaction, poll, sticker).

- Composite flows do not retry completed steps.

Streaming and ChunkingCommand Queue⌘I