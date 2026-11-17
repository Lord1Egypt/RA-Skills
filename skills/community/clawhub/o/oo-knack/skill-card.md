## Description:

Operate Knack through an OOMOL-connected account to read, create, update, and delete records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working with Knack use this skill to retrieve records and perform record creation, updates, and deletions through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute remote code without an installation approval step, and the remote installer payload was unavailable for verification.

Mitigation: Review setup first, install the CLI through a separately reviewed process, and decide whether to enable bundled-skill synchronization.

Risk: Creating, updating, or deleting records changes Knack data.

Mitigation: Connect only the needed Knack account and retain approval for every write or deletion.

## Reference(s):

- [Knack skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-knack)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Knack API documentation](https://docs.knack.com/v3/reference)
- [Knack](https://www.knack.com)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the action schema; write and destructive actions are identified for review.]

## Skill Version(s):

1.0.5 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
