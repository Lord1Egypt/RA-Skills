## Description:

Helps an agent identify the current session's login entry from an authoritative configuration file and label replies accordingly, asking the user when the entry cannot be confirmed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

All rights reserved (documentation); MIT for .py code only

## Use Case:

Agent users and operators use this Chinese-oriented helper to confirm which login entry a session belongs to and avoid mislabeling replies across accounts. If the authoritative configuration does not establish the entry, the agent asks the user rather than guessing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad identity-related triggers could activate the skill unintentionally.

Mitigation: Review trigger phrases and invoke it only when session-entry identification is needed.

Risk: Declared Write and WebSearch tools grant more authority than the described identity check requires.

Mitigation: Review the tool list and limit execution to the minimum required read-only access.

## Reference(s):

- [ClawHub identity-verify release](https://clawhub.ai/zhaoxinghua09-cell/skills/identity-verify)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the user's language; labels the confirmed entry or requests confirmation when uncertain.]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release; bundled manifest and frontmatter say 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
