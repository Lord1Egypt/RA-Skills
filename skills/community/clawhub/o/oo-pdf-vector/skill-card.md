## Description:

PDF Vector (pdfvector.com). Use this skill for ANY PDF Vector request — searching and reading data. Whenever a task involves PDF Vector, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use the skill to ask questions about PDFs at public URLs, parse documents into Markdown, or extract structured data as JSON through a connected PDF Vector account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup runs unchecked remote code through a CLI that also documents persistent changes to agent skills.

Mitigation: Review and approve CLI installation separately; check which persistent agent skills the chosen CLI release installs or synchronizes, and disable synchronization if unwanted.

Risk: Document requests pass through OOMOL and may consume service credit.

Mitigation: Account for possible OOMOL service-credit use when submitting document requests.

## Reference(s):

- [PDF Vector homepage](https://www.pdfvector.com)
- [PDF Vector API reference](https://global.pdfvector.com/api/reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-pdf-vector)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Provider-returned answer text, Markdown, or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and the public PDF URL supplied.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
