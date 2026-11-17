## Description:

Connects an agent to SendFox to read, create, update, and delete contacts and contact lists through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage contacts and contact lists in a SendFox account connected through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute an unverified CLI release and add persistent agent skills during startup synchronization.

Mitigation: Review and install a verified CLI release before use; set OO_SKILLS_SYNC_DISABLED=1 when only SendFox functionality is needed.

Risk: The OOMOL service handles the SendFox connection and contact data.

Mitigation: Understand OOMOL's role in connection and contact-data handling before use.

## Reference(s):

- [SendFox](https://sendfox.com)
- [SendFox API documentation](https://sendfox.com/developer/docs/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector responses with text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read, create, update, or remove contact data; writes and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
