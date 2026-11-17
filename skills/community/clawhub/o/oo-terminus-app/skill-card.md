## Description:

Use Terminus App through an OOMOL-connected account to inspect projects, tracking conventions, and links, and to create tagged links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a Terminus App workspace can review projects, conventions, and tracked links, and create tagged links through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run changing remote code and alter managed skills without clearly explaining the changes.

Mitigation: Install a verified CLI release yourself and review its managed-skill synchronization settings before enabling the skill.

Risk: A connected account may grant more Terminus access than the task requires.

Mitigation: Authorize the OOMOL connection with only the Terminus access needed.

Risk: Creating a tagged link changes Terminus App data.

Mitigation: Confirm the exact payload and effect with the user before running a write action.

## Reference(s):

- [Terminus App](https://www.terminusapp.com/)
- [Terminus App API documentation](https://www.terminusapp.com/apidocs)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with oo CLI commands and JSON payloads or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Terminus data; create_link creates a tagged link after the user confirms the change.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
