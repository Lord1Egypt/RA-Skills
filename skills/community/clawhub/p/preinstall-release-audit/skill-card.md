## Description:

Audit public software releases before installation using static artifacts, license checks, endpoint scans, and live distribution verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and security reviewers use this skill to evaluate unfamiliar public software before installation by comparing release surfaces, inspecting packaged artifacts as data, checking licenses, inventorying endpoints, and verifying advertised downloads or manifests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installers and release artifacts can be unsafe to inspect if they are executed or imported during review.

Mitigation: Use an isolated workspace, unpack distributables as data, and keep installation as a separate explicit decision.

Risk: Static endpoint and packaged-code inspection cannot prove that runtime network behavior or telemetry is absent.

Mitigation: State what was not executed and what static inspection cannot exclude before making an installation recommendation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextaltair/skills/preinstall-release-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with observed facts, confidence limits, and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should cite artifact version and exact file or URL for each material claim.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
