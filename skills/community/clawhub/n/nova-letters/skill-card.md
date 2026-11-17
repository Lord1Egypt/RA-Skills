## Description:

Write reflective letters to your future self. Capture what matters across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocana](https://clawhub.ai/user/cryptocana)

### License/Terms of Use:

MIT

## Use Case:

Agents and developers use Nova Letters to record reflective, timestamped letters across sessions so future sessions can recover meaningful context, lessons, and decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Letters can expose sensitive or private information if users write secrets, credentials, regulated data, or private user information into them.

Mitigation: Do not store secrets, credentials, regulated data, or private user information in letters; review letter contents before sharing or syncing them.

Risk: The read command can be misused with crafted date arguments to print readable Markdown files outside the intended letters directory.

Mitigation: Avoid running Nova Letters with untrusted date arguments or instructions until the read path is hardened and date inputs are validated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cryptocana/skills/nova-letters)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown files and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores one Markdown file per day under ~/.openclaw/workspace/letters/.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
