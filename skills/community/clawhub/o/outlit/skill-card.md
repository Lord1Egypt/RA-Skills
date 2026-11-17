## Description:

Use when accessing Outlit customer intelligence through the `outlit` CLI, Outlit MCP tools, Pi tools, or @outlit/tools, including customer lookups, users, workspace users, timelines, facts, source evidence, semantic search, revenue, churn, SQL analytics, identity splits, merge suggestions, setup, integrations, or troubleshooting agent access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-paz](https://clawhub.ai/user/leo-paz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and customer-facing teams use this skill to retrieve and analyze Outlit customer intelligence for onboarding, adoption, retention, renewal, and expansion work. It can also guide explicitly requested workspace configuration and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation instructions include a remote shell script that the security review reports as unverified.

Mitigation: Review and verify the installer before running it; use a package installation route only after checking its source and contents.

Risk: The reported workflow can execute customer merges, which may permanently combine customer records.

Mitigation: Treat merge execution as a consequential workspace change: require explicit user authorization, confirm both records are the same customer, and review the merge preview before execution.

## Reference(s):

- [Outlit documentation index](https://docs.outlit.ai/llms.txt)
- [Outlit documentation](https://docs.outlit.ai/)
- [Outlit product homepage](https://outlit.ai)
- [Outlit ClawHub release](https://clawhub.ai/leo-paz/skills/outlit)
- [Identity and merge workflow](artifact/references/identity.md)
- [SQL reference](artifact/references/sql-reference.md)

## Skill Output:

**Output Type(s):** [Analysis, API calls, SQL queries, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown and text, with SQL queries, shell commands, and configuration examples when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include customer evidence and source citations; scope depends on available workspace tools and access.]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
