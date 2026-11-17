## Description:

Datagma (datagma.com). Use this skill for ANY Datagma request — searching and reading data. Whenever a task involves Datagma, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Datagma through an OOMOL-connected account for person or company enrichment, work email and phone discovery, job-change checks, and account credit information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs downloaded code that was unavailable for inspection and may install additional agent instructions.

Mitigation: Review and verify the CLI installation separately; consider disabling cross-agent skill synchronization as described by the publisher.

Risk: Lookup details are shared with OOMOL and Datagma, and requests may use account credits.

Mitigation: Submit only details intended to be shared and consider account credit usage.

## Reference(s):

- [Datagma homepage](https://datagma.com/)
- [Datagma API documentation](https://datagmaapi.readme.io/reference/getting-started-with-your-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-datagma)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON inputs and connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas and response fields vary by the selected Datagma action.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
