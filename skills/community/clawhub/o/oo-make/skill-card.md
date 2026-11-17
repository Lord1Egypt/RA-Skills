## Description:

Operate Make.com scenarios and account data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users with a connected Make account use this skill to inspect account and scenario details, run scenarios, and manage scenario activation through Make actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute downloaded CLI installers whose complete effects were unavailable for inspection.

Mitigation: Review and approve CLI installation separately, prefer a verified release, and review or disable automatic agent-skill synchronization.

Risk: Connected Make credentials and requested permissions can expose or change account data.

Mitigation: Connect only the permissions needed and retain confirmation for scenario changes and runs.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Make API documentation](https://developers.make.com/api-documentation/getting-started/api-structure)
- [Make](https://www.make.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live action schemas to shape JSON payloads; changes to Make state require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
