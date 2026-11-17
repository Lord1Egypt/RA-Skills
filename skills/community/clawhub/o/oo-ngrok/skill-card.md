## Description:

Use ngrok through an OOMOL-connected account to search and read ngrok data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect ngrok endpoints, reserved domains, tunnel sessions, and tunnels through their connected OOMOL account. It returns account data from the listed read actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes downloaded code and can introduce changes to other agent skills.

Mitigation: Review and approve CLI installation separately, use a pinned release with verified integrity, and set OO_SKILLS_SYNC_DISABLED=1 unless startup skill synchronization is wanted.

Risk: The installer and hosted backend were not verified, and OOMOL receives permissions for the connected ngrok account.

Mitigation: Confirm the ngrok permissions granted to OOMOL before connecting or using the skill.

## Reference(s):

- [ngrok API documentation](https://ngrok.com/docs/api/)
- [ngrok](https://ngrok.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API data, JSON, Guidance]

**Output Format:** [JSON responses with concise textual summaries; Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results for endpoints, reserved domains, tunnel sessions, and tunnels.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
