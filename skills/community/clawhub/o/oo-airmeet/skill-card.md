## Description:

Airmeet (airmeet.com). Use this skill for ANY Airmeet request — searching and reading data. Whenever a task involves Airmeet, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with an OOMOL-connected Airmeet account use this skill to list events and inspect their booths, custom registration fields, sessions, and tracks. It guides the agent in checking action schemas and making read requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded software whose contents and exact system changes could not be verified; the security assessment rates this suspicious.

Mitigation: Prefer an independently reviewed oo installation and require approval before running either downloaded installer.

Risk: Airmeet access uses the user's OOMOL-connected account, and the security guidance calls out the CLI's automatic skill installation behavior.

Mitigation: Review the permissions granted to the Airmeet connection and review the CLI's automatic skill installation behavior.

## Reference(s):

- [Airmeet Public API documentation](https://help.airmeet.com/support/solutions/articles/82000467794-airmeet-public-api-introduction)
- [Airmeet](https://www.airmeet.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Markdown instructions with JSON action payloads and connector response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Airmeet event and configuration data]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
