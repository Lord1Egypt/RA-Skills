## Description:

Operate Databar.ai to read, create, and update data through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Databar.ai users can use the skill to inspect tables and enrichments, retrieve account and task information, and create tables, insert rows, or submit enrichment tasks through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback may install software or affect other agent skills, and the external installer and hosted credential handling have not been verified.

Mitigation: Review and approve CLI installation separately, check whether it adds or updates other skills, and disable that behavior if unwanted. Connect only the intended Databar account.

Risk: Write actions can change Databar.ai data.

Mitigation: Retain confirmation for every write and review the exact action and payload before running it.

## Reference(s):

- [Databar.ai API documentation](https://docs.databar.ai/)
- [Databar.ai](https://databar.ai/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell command examples and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs must match the live connector schema; write actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
