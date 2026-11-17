## Description:

Operate Photoroom to edit product images through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to apply composed ecommerce edits to Photoroom product images and return a result for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can execute unverified remote code without clear user approval.

Mitigation: Review setup first, install a verified CLI release yourself, and avoid automatic fallback installers; review its bundled-skill installation behavior.

Risk: Images pass through OOMOL and temporary connector storage.

Mitigation: Approve the image-editing payload and account for this image handling before use.

## Reference(s):

- [Photoroom skill release](https://clawhub.ai/oomol/skills/oo-photoroom)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Photoroom homepage](https://www.photoroom.com)
- [Photoroom API documentation](https://docs.photoroom.com/api-reference-openapi)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON]

**Output Format:** [JSON action payloads and result URLs, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image-editing results that use relighting, text removal, or beautification should be reviewed before publishing.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
