## Description:

ShortPixel (shortpixel.com). Use this skill for ANY ShortPixel request — reading, creating, updating, and deleting data. Whenever a task involves ShortPixel, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

ShortPixel account users can use the skill to associate domains, check CDN usage, purge cached or stored optimized images, and revoke domain associations through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run an unverified remote installer without separate consent, and the downloaded installer's full behavior is unverified; setup may also change other agent skills.

Mitigation: Review setup first, prefer installing a verified version-pinned CLI yourself, and check controls for automatic skill synchronization.

Risk: Domain association changes, cache or storage purges, and revocation can alter ShortPixel account state or remove data.

Mitigation: Inspect the live action schema and confirm the exact target and effect before write or destructive actions, following the skill's approval requirements.

## Reference(s):

- [ShortPixel API documentation](https://shortpixel.com/api-docs)
- [ShortPixel](https://shortpixel.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs follow the live connector schema; state-changing and destructive actions require user approval.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
