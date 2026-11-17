## Description:

Use the OOMOL-connected TinyPNG service to compress images and transform TinyPNG output images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other TinyPNG users can compress images and transform TinyPNG output images through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unchecked remote code through downloaded installers.

Mitigation: Review setup before use and prefer a separately installed, verified CLI release; the downloaded installers were not inspected.

Risk: Automatic skill synchronization can add persistent agent skills beyond TinyPNG.

Mitigation: Disable automatic skill synchronization if it is not wanted.

Risk: Image submissions are mediated by OOMOL and the connected TinyPNG account.

Mitigation: Review the OOMOL connection and image submissions as part of setup and use.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [TinyPNG](https://tinypng.com)
- [TinyPNG API documentation](https://tinypng.com/developers/reference)

## Skill Output:

**Output Type(s):** [API calls, Guidance]

**Output Format:** [JSON connector responses and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image actions return resource or transit URLs; inputs depend on the action schema.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
