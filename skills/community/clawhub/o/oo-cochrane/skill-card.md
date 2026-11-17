## Description:

Search and read Cochrane data for Cochrane-related requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, clinicians, and other Cochrane users use the skill to retrieve review metadata, roles, translations, and version information through their connected Cochrane account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Cochrane reading request can trigger software installation without a clear approval step.

Mitigation: Review setup behavior before installing. Use an independently verified, pinned CLI and require approval before any fallback installer runs; consider the CLI's bundled-skill installation and OOMOL account access.

## Reference(s):

- [Cochrane Review Document API documentation](https://documentation.cochrane.org/spaces/API/pages/117377312/Review+Document+API)
- [Cochrane](https://www.cochrane.org)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Cochrane skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-cochrane)

## Skill Output:

**Output Type(s):** [JSON, Structured data]

**Output Format:** [JSON responses from Cochrane connector actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include Cochrane data and execution metadata.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
