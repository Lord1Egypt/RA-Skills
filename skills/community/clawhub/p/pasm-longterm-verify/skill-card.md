## Description:

Runs repeatable checks to assess whether the PASM cognitive engine remains healthy during long runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arronjack](https://clawhub.ai/user/arronjack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use these verification agents to exercise PASM structure and long-run behavior, archive findings, and compare results against baselines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial scan flagged an API-guard entry point that may not match the stated long-term health-check purpose, and some references were unavailable for review.

Mitigation: Review the API-guard behavior and available references before installation, and confirm that the capability fits your intended use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/arronjack/skills/pasm-longterm-verify)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Terminal status summaries and JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Repeatable findings suitable for archiving and baseline comparison]

## Skill Version(s):

0.6.0 (source: frontmatter; server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
