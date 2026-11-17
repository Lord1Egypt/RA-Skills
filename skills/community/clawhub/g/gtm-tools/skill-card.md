## Description:

GTM Tools helps agents set up authentication and call the gtm-tools API for LinkedIn, Reddit, email-finding, buying-signal, billing, and geocoding workflows using curl, MCP, or the CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arnaudjnn](https://clawhub.ai/user/arnaudjnn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and GTM operators use this skill to connect agent workflows to the gtm-tools API, manage authentication, inspect billing state, and run LinkedIn, Reddit, email, signal, and geocoding tools with cost-aware sequencing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may create or retain long-lived GTM API credentials.

Mitigation: Use revocable keys, store them only in approved secret storage, avoid hard-coding them into scripts or CI, and revoke unused keys after the workflow ends.

Risk: The browser-session helper can connect real LinkedIn or Reddit accounts to agent-driven workflows.

Mitigation: Install it only after verifying the installer and account scope, and document how to disconnect sessions or revoke access before enabling session-backed tools.

Risk: The tool catalog includes billing, token purchase, public posting, messaging, voting, and other account-changing actions.

Mitigation: Require explicit user approval before spending tokens, buying tokens, enabling auto-reload, posting publicly, sending messages, or changing account state.

Risk: Metered tools can charge tokens for not-found results, upstream failures, and repeated try-again-later responses.

Mitigation: Check balance and live tool costs first, filter targets before expensive calls, limit fan-out, and honor retry-after guidance instead of tight retries.

## Reference(s):

- [GTM Tools Skill Page](https://clawhub.ai/arnaudjnn/skills/gtm-tools)
- [GTM Tools Tool Catalog](references/tools.md)
- [GTM Tools Agent Docs Index](https://gtm-tools.sh/llms.txt)
- [GTM Tools API Reference](https://gtm-tools.sh/api-reference)
- [GTM Tools Agent Identity Protocol](https://api.gtm-tools.sh/auth.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include API calls that create or revoke credentials, inspect billing state, connect browser sessions, or perform account-changing actions after user authorization.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
