## Description:

Helps an agent inspect WPS multidimensional table schemas and records and create or delete records through the WPS Open Platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openmsg88](https://clawhub.ai/user/openmsg88)

### License/Terms of Use:

MIT-0

## Use Case:

WPS users and developers can use the skill to inspect a multidimensional table and read, add, or delete records with their own WPS account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth authorization codes pass through a shared external callback, and several bundled components were only partially inspected.

Mitigation: Verify control of the callback and protection of authorization codes, review the bundled components, and understand the credential-directory override before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/openmsg88/skills/liuli-jinshan-bridge)
- [Publisher profile](https://clawhub.ai/user/openmsg88)
- [Credential setup instructions](references/setup.md)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Text summaries of table schemas and record operation results, plus setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include table fields, record values, status codes, or record identifiers returned by WPS.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
