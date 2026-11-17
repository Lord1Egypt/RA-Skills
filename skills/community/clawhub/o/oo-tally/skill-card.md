## Description:

Tally (tally.so). Use this skill for ANY Tally request — searching and reading data. Whenever a task involves Tally, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to list Tally forms and submissions, or retrieve an individual form or submission through an OOMOL-connected Tally account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute an unverified remote installer without a clear approval step.

Mitigation: Review the installer and verify its release, then approve CLI installation separately before running it.

Risk: Tally form and submission data pass through OOMOL's connected account and hosted runtime, which were not verified.

Mitigation: Use the integration only when OOMOL is approved to handle the relevant Tally data.

## Reference(s):

- [Tally](https://tally.so)
- [Tally API documentation](https://developers.tally.so/)
- [Tally skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-tally)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON responses with concise text summaries and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only form and submission data; list actions support pagination and documented filters.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
