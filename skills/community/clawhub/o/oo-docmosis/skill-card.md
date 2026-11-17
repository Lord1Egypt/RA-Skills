## Description:

Docmosis (docmosis.com). Use this skill for ANY Docmosis request — searching and reading data. Whenever a task involves Docmosis, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill with an OOMOL-connected Docmosis account to inspect environment and template information and render documents from JSON data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an online installer and connector implementation that were not verified.

Mitigation: Install a reviewed, version-pinned oo release and check its automatic agent-skill synchronization settings before enabling the skill.

Risk: Document rendering can send submitted data through OOMOL to Docmosis and may affect delivery settings or quota.

Mitigation: Require approval for each render after reviewing the template, submitted data, delivery settings, and quota impact.

## Reference(s):

- [Docmosis](https://www.docmosis.com)
- [Docmosis Cloud API documentation](https://apidocs.docmosis.com/cloud/dws4/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Configuration instructions]

**Output Format:** [Markdown instructions with inline shell commands; JSON connector responses and optional rendered document files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Render results include delivery metadata and may include an explicit base64 result file.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
