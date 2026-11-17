## Description:

Uses Xquik from Hermes Agent for X research, monitoring, and approval-gated actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xquik](https://clawhub.ai/user/xquik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Hermes Agent users use this skill for X/Twitter research, monitoring, social listening, support triage, creator or brand research, and controlled publishing workflows through Xquik routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install guidance enables an unpinned external Hermes Tweet plugin that may later run with Xquik API and account-action privileges.

Mitigation: Review and pin the exact Hermes Tweet plugin version before enabling it.

Risk: Automated X/Twitter operations can affect real accounts or private workflow state.

Mitigation: Keep HERMES_TWEET_ENABLE_ACTIONS disabled unless needed, and approve only a specific endpoint, payload, account, and side effect before using tweet_action.

Risk: Credential exposure could occur if users paste API keys into chat or tool arguments.

Mitigation: Configure XQUIK_API_KEY only in the Hermes runtime environment, never request or echo key values, and stop if a secret is pasted.

Risk: Endpoint guessing or direct HTTP fallbacks could bypass the catalog and approval boundary.

Mitigation: Use tweet_explore first, call only catalog-listed Xquik routes, and reject direct HTTP fallbacks.

## Reference(s):

- [Endpoint and Approval Contract](references/endpoint-contract.md)
- [Hermes Tweet ClawHub Listing](https://clawhub.ai/xquik/skills/hermes-tweet)
- [Xquik Hermes Tweet Guide](https://docs.xquik.com/guides/hermes-tweet)
- [Hermes Agent Plugin Guide](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/plugins.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown for humans with JSON-like tool payloads and shell command snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint selections, API-result summaries, action previews, sanitized errors, and troubleshooting guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter version 0.1.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
