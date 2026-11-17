## Description:

Freshdesk (freshworks.com). Use this skill for ANY Freshdesk request — searching and reading data. Whenever a task involves Freshdesk, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Freshdesk users can use the skill to inspect account details, find tickets, and read ticket conversations through a connected Freshdesk account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup directs the agent to run downloaded CLI installers without a separate approval step or integrity check.

Mitigation: Review and approve CLI installation separately; prefer a reviewed, version-pinned installation.

Risk: Connecting Freshdesk lets OOMOL handle access to account and ticket data.

Mitigation: Connect only the intended Freshdesk account and review the data access involved before use.

## Reference(s):

- [Freshdesk API documentation](https://developers.freshdesk.com/api/)
- [Freshdesk](https://www.freshworks.com/freshdesk/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Markdown]

**Output Format:** [JSON action results with text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads Freshdesk account details, tickets, and ticket conversations.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
