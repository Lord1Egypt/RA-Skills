## Description:

RoxyAPI (roxyapi.com). Use this skill for ANY RoxyAPI request — searching and reading data. Whenever a task involves RoxyAPI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected RoxyAPI account can ask an agent to retrieve tarot, astrology, BaZi, Human Design, numerology, almanac, forecast, and city data through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup uses remote CLI installers that have not been verified.

Mitigation: Review and install the CLI yourself before use instead of letting the missing-command fallback execute downloaded code automatically.

Risk: The CLI's broader skill synchronization behavior is not disclosed.

Mitigation: Check its skill synchronization behavior and the documented OO_SKILLS_SYNC_DISABLED control before setup.

Risk: Chart requests may share personal details with OOMOL and RoxyAPI, and usage charges may apply.

Mitigation: Share only chart details you intend both services to process, and consider usage charges.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [RoxyAPI](https://roxyapi.com/)
- [RoxyAPI authentication documentation](https://roxyapi.com/docs/authentication)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON API responses with task-specific text summaries and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs vary; inspect the live action schema before submitting a request.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
