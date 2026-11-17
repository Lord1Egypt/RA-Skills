## Description:

Provides agent-facing LongPort OpenAPI CLI workflows for stock quotes, account balances and positions, order management, and market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankxiong](https://clawhub.ai/user/frankxiong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to let an agent query Longbridge account and market data, produce CLI calls, and format results as text or JSON. Users may also route order-management requests through the CLI when trading is deliberately enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An AI-accessible CLI can read Longbridge brokerage account data when credentials are available.

Mitigation: Install only for intended account access, keep credentials least-privileged, and prefer paper or read-only profiles for agent workflows.

Risk: Live buy, sell, or cancel commands can execute when trading is enabled, and --yes/-y bypasses confirmation prompts.

Mitigation: Keep the default read-only mode unless deliberately trading, avoid --yes/-y for live orders, and require human review before order submission.

Risk: Profile and .env files may hold brokerage secrets used by the CLI.

Mitigation: Protect profile files, separate paper and live credentials, and review environment-file handling before using real brokerage accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frankxiong/skills/longbridge-kit)
- [LongPort OpenAPI](https://open.longportapp.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with bash examples; CLI commands can return table text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, uv, and Longbridge credential environment variables; trade actions remain read-only unless explicitly enabled.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
