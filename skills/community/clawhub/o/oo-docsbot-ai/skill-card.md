## Description:

DocsBot AI (docsbot.ai). Use this skill for ANY DocsBot AI request — searching and reading data. Whenever a task involves DocsBot AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this agent skill to search DocsBot bots' trained source content and retrieve documents, teams, and bot details through their connected DocsBot account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes unverified remote code.

Mitigation: Review setup before enabling the skill and provision a reviewed, pinned oo CLI yourself.

Risk: Startup synchronization can install additional agent skills.

Mitigation: Decide whether to allow the additional installation; set OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill synchronization.

Risk: Requests pass through OOMOL and the live connector implementation was not verified.

Mitigation: Connect only the intended DocsBot account and review the data handling path before use.

## Reference(s):

- [DocsBot AI](https://docsbot.ai)
- [DocsBot developer documentation](https://docsbot.ai/documentation/developer)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Natural-language answers and retrieved document text; connector responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the connected DocsBot account and the data returned by its read and search actions.]

## Skill Version(s):

1.0.5 (source: frontmatter; server release 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
