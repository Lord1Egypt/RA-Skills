# Client and installation notes

Import the `mochi-crypto-intelligence` directory through your AI client's supported Skill import flow. It must contain SKILL.md at its root. Do not assume every chatbot accepts Skill folders. In Codex, the default local location is `$CODEX_HOME/skills/mochi-crypto-intelligence` (or `~/.codex/skills/mochi-crypto-intelligence` when CODEX_HOME is unset). A new session may be needed for discovery. Other clients have their own documented paths/import UI; use those instead of changing unrelated configuration.

The host supplies the AI model and search/web-reading/browser tools. No extra AI API key, AIXBT account, market-data subscription or MochiPay account is requested by this Skill. The host's model/search billing and network permissions remain its own. The Skill cannot grant browsing or scheduler capabilities to a client that lacks them.

Python3.10+ is optional for scripts and local incremental state. They use only the standard library. Browser-based research works without Python; accurately report unavailable script/history operations. A normal public browser is useful when sites depend on JavaScript. Static script collection may encounter network policy restrictions, robots rules or source changes; report the gap and use other accessible sources. No proxy rotation, access-control bypass or TLS-disabling instructions are provided.

No always-running service, automatic schedule, website component or Monitor integration is installed. If the user separately requests recurring briefs, use a host-supported scheduler and explicit destination. Do not promise reminders or notifications when the host cannot deliver them.
