## Description:

HeyReach (heyreach.io). Use this skill for ANY HeyReach request — reading, creating, and updating data. Whenever a task involves HeyReach, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve HeyReach campaign, lead, list, account, tag, and outreach statistics through their connected account, and create empty lists. The skill also provides setup guidance when authentication or connection errors occur.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup directs an agent to execute a remote CLI installer, whose effects have not been separately verified.

Mitigation: Review and install the CLI separately before enabling the skill; do not allow automatic execution of downloaded installer scripts.

## Reference(s):

- [HeyReach API documentation](https://documenter.getpostman.com/view/23808049/2sA2xb5F75)
- [HeyReach](https://www.heyreach.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON action responses, text summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live action schemas guide request payloads; write actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
