## Description:

Securely fetch credentials from LastPass vault via lpass CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitchrisqueen](https://clawhub.ai/user/gitchrisqueen)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to retrieve specific passwords, usernames, notes, or raw LastPass entry data from a local lpass session for deployment, API, or login workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose plaintext LastPass passwords, notes, usernames, or raw records available to the local lpass session.

Mitigation: Require explicit approval before fetching or using secrets, and limit the LastPass account or shared folder to only entries needed for the workflow.

Risk: Raw record retrieval may disclose more vault data than a workflow requires.

Mitigation: Prefer field-specific retrieval for password, username, or notes and avoid raw record access unless it is necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitchrisqueen/skills/lastpass-cli)
- [Publisher profile](https://clawhub.ai/user/gitchrisqueen)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text returned from lpass commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return sensitive plaintext secret material from the user's local LastPass vault.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
