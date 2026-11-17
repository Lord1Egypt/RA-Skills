## Description:

Inspect CraftMyPDF account and template data and generate PDFs from CraftMyPDF templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect CraftMyPDF account and template details and generate PDFs from templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute unverified downloaded code and may install additional persistent agent skills.

Mitigation: Review and verify a fixed oo CLI release before setup; consider disabling automatic skill synchronization.

Risk: PDF generation is a write action, and generated PDFs are returned through hosted output links.

Mitigation: Confirm the exact payload and effect before generation, and review how the hosted PDF output will be handled.

## Reference(s):

- [CraftMyPDF API documentation](https://craftmypdf.com/docs/index.html)
- [CraftMyPDF homepage](https://craftmypdf.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-craftmypdf)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON responses and natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account and template data, or a hosted PDF URL with transaction metadata.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
