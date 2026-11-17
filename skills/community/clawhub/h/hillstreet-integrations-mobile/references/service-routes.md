# Service routes

Use these source-verified routes as discovery starting points; recheck authorization and health. Do not infer readiness from this document.

| Service | Route | Verification |
| --- | --- | --- |
| Open-Connect | https://open-connect.site/mcp | Discover status, connections, projects, schemas; inspect personal and project grants separately. |
| Open-TGate | https://open-tgate.site/mcp | OAuth DCR; list accounts, then select authorized accounts and bounded audit reads. Never request raw Telegram sessions. |
| Open-Box | https://open-box.space/mcp | OAuth; verify protected-resource metadata and approved OAuth client allowlist. Explicitly link existing users to the correct SSO subject; never infer links from email. |
| Open-Teleset | https://open-teleset.site | Discover the deployed transport from the owning release. Require authenticated HTTP MCP execution and dependency readiness before mobile registration. A source branch or process health alone is insufficient. Do not guess an /mcp URL. |
| Open-System | Existing remote Open-System connector | Discover schemas and perform a bounded read. Use its owning deployment process for changes; do not infer an MCP URL from its web domain. |
| Twilio | Existing Open-Connect Twilio connection | Discover native schemas, then read the redacted account. Composio's Twilio documentation MCP has no account authentication and does not establish Twilio account execution. |
| ChatGPT | Existing remote ChatGPT plugin/connector | Preserve verified App bindings. OpenAI API availability does not prove ChatGPT conversation access or mobile plugin installation support. |

Cloudflare 1010 from a command-line HTTP client does not prove a native connector is broken. Use an already authorized native path, or report the blocked check without evasion.

Register source-verified custom MCP endpoints in the authenticated Composio dashboard, then complete OAuth before discovering and syncing tools. Never embed bearer tokens in URLs or manifests.


Personal Telegram uses the native Open-TGate authorized user account path; Telegram bot connections are separate identities. Proton Pass requires inspection of its installed transport and supported executor. Neither account metadata nor this route reference establishes vault access or hosted readiness.
