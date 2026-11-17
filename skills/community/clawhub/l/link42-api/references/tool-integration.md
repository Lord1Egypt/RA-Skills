# Tool integration

Use a current authorized text model that supports the tool's required functions and context. Protocol compatibility does not turn a DeepSeek/GLM model into Claude/GPT or add hosted tools.

## OpenAI SDK / compatible clients

Base URL `https://www.link42.ai/v1`, API key from `LINK42_API_KEY`, exact model ID from discovery. Chat Completions and Responses have distinct bodies/events; choose the client's matching wire format. JSON images, embeddings and tasks are separate resources. Azure deployment URLs, AWS SigV4 and native cloud-resource auth are not this gateway's standard client interface.

## Claude Code / Anthropic SDK

`ANTHROPIC_BASE_URL=https://www.link42.ai` (SDK appends `/v1`), `ANTHROPIC_AUTH_TOKEN` sourced privately from the LINK42 key, `ANTHROPIC_MODEL` set to the selected model. Do not retain a conflicting `ANTHROPIC_API_KEY`. The gateway serves Messages/count_tokens, model discovery, request IDs, retry headers, streamed events and sanitized error recovery. Vendor beta headers can be forwarded, but model-incompatible fields still require legitimate fallback. Claude-specific Remote Control/hosted services are not promised on arbitrary upstream models.

## Codex

Use a user-level custom provider (not the reserved `openai` ID), `base_url=https://www.link42.ai/v1`, `env_key=LINK42_API_KEY`, `wire_api=responses`, and select an authorized tool-capable model. Keep `requires_openai_auth=false`/WebSocket support disabled unless that feature is actually implemented. Do not rewrite the user's current provider or security/approval settings just to install the skill. Provide a separate configuration snippet/profile and let the user select it.

## OpenClaw and other skill hosts

Install this folder using the host's documented skill directory/import mechanism. OpenClaw discovers SKILL.md and the `metadata.openclaw.primaryEnv` key requirement; configure LINK42_API_KEY privately. Skills teach model/resource actions; they do not automatically replace the host's reasoning model/provider. Installing into a folder is not proof the running session loaded it: check the host's skill list/check and start a new session if required.

International/domestic distribution changes download routing only, never the selected model/account, API credentials, currency or scope. A ClawHub/SkillHub command is advertised only after the exact published slug/version is verified. The official checksum-pinned download works without either registry. Never invent a store listing or silently install unrelated marketplaces/plugins.

If a host lacks shell/Python, import SKILL.md/references and expose authorized HTTP or the optional stdio MCP bridge. Only use the requested scopes. Do not weaken sandbox, certificate, authentication or approval policy to make an integration work.
