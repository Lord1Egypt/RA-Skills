# OpenClaw setup branches

## Configuration contract

Inspect installed schema before applying. Illustrative **merge fragment**, not a file replacement:

~~~json
{
  "models": {
    "mode": "merge",
    "providers": {
      "hashference": {
        "baseUrl": "https://hashference.com/v1",
        "api": "openai-completions",
        "apiKey": {"source":"env","provider":"default","id":"HASHFERENCE_API_KEY"},
        "models": [
          {"id":"EXACT_LIVE_ID","name":"CATALOG_NAME","input":["text"],"contextWindow":128000,"maxTokens":4096}
        ]
      }
    }
  }
}
~~~

Replace example ID/name/limits with live generated metadata. Do not change an intentional existing replace-mode setup without discussing impact. The default SecretRef provider assumes env resolution is available; preserve configured alternatives. Never put literal keys in config exports, shell arguments or packages.

Read installed help before commands; available versions may support:

~~~bash
openclaw --version
openclaw models list --agent AGENT_ID
openclaw plugins list
openclaw config schema --json
openclaw config set --help
~~~

To bind a key already in the Gateway environment, supporting versions expose:

~~~bash
openclaw config set models.providers.hashference.apiKey --ref-provider default --ref-source env --ref-id HASHFERENCE_API_KEY
~~~

This mutates config, not the env variable. Use the setup tool instead where session policy requires it. Inspect plugins/runtimes: HTTP compatibility alone does not prove the necessary OpenClaw runtime is installed. Never install plugins or restart the hosting Gateway through an unsupported shell workaround.

## Transports

| Use | OpenClaw api | baseUrl | Required endpoint |
| --- | --- | --- | --- |
| Default | openai-completions | https://hashference.com/v1 | /v1/chat/completions |
| Responses | openai-responses | https://hashference.com/v1 | /v1/responses |
| Native Messages | anthropic-messages | https://hashference.com | /v1/messages |

Clients append paths; avoid /v1/v1/messages. Check installed client normalization. Catalog protocol responses can still offer Chat; endpoints decides. Chat-only models cannot be forced onto Responses. Use separate local provider IDs for different transports instead of changing working sessions underneath users.

Native Messages aliases can use suffix -messages; same_model_as marks protocol variants, not additional checkpoints. Native direct Claude caching differs from Chat/Responses. Respect tool_choice_modes; do not force required on auto/none-only routes.

## Device login

1. POST https://hashference.com/v1/device/code with JSON {"client_name":"OpenClaw"}.
2. Privately show verification_uri_complete and user_code to the requester, honoring expiry. Never post login codes in a group.
3. Poll POST /v1/device/token with JSON device_code at returned interval or slower. Honor pending/slowdown/Retry-After, stop on denial, expiry or cancellation. No unowned background poller.
4. api_key from success goes **directly to an approved secret store**. Never fetch the final token response through a model-visible generic HTTP tool.
5. Report only storage/auth success. Login approval does not authorize spend.

If no safe token sink is exposed, use masked entry. An already-installed official Hashference CLI may offer login; verify current docs and its store integration first. Do not install a stale tarball or assume CLI login automatically configures OpenClaw.

## Route branches

- Primary: a provider/model pair for the correct agent; use live-tested default selection. Auth alone does not change primary.
- Fallback: preserve existing chain/order and append requested pair. Do not promise every error triggers fallback.
- Delegation: select pair for the child only; main model stays. Children share account credit.
- Session: inspect /status; use supported /model provider/model or /model default only as requested. Global changes do not prove existing sessions switched.

Do not create agents.defaults.models just to register runtime IDs. Check version-specific picker/allowlist behavior and explicit model policy before merging any required entries.
