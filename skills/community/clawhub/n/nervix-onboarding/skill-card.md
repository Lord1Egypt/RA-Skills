## Description:

Use this skill when onboarding a new agent or operator into Nervix, verifying live federation prerequisites, enrolling through the Nervix flow, and preparing or publishing the related skill bundle to ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dansidanutz](https://clawhub.ai/user/dansidanutz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent maintainers use this skill to verify Nervix federation readiness, enroll or validate agent identities, and prepare or publish ClawHub skill bundles when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthorized enrollment, heartbeat, or publishing actions could affect live Nervix or ClawHub state.

Mitigation: Confirm authorization and scope before running enrollment, heartbeat, preview, publish, or auto-bump steps.

Risk: Credentials such as CLAWHUB_API_TOKEN or Nervix tokens could be exposed or used in the wrong environment.

Mitigation: Use only approved credentials for the intended environment and avoid printing or storing tokens outside approved secret handling.

Risk: Endpoint or schema assumptions may become stale against the live Nervix federation.

Mitigation: Verify the Nervix API root and expected input types before retrying failed onboarding or publishing operations.

## Reference(s):

- [Nervix Federation Reference](references/nervix-federation.md)
- [Nervix Site](https://nervix.ai)
- [Nervix tRPC API Root](https://nervix.ai/api/trpc)
- [ClawHub](https://clawhub.ai)
- [ClawHub Skill Listing](https://clawhub.ai/dansidanutz/skills/nervix-onboarding)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include readiness blockers when required tokens or credentials are unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
