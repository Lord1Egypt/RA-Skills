## Description:

An operations inspection skill that checks host resources, middleware, Kubernetes status, logs, and business indicators, then summarizes health scores and findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to run automated health checks across infrastructure, middleware, container, log, and business-signal layers. It can print a console report or export a JSON inspection report for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised layer selector may not limit what the script checks.

Mitigation: Review the checks before use and do not rely on --layers for containment until the scope-control behavior is fixed.

Risk: Inspection reports may contain sensitive operational details.

Mitigation: Store exported reports in a restricted location and review them before sharing.

Risk: Some checks may require elevated host visibility and can run broader host or service inspections than expected.

Mitigation: Run from an unprivileged account by default and avoid sudo or scheduled execution unless the exact checks and report location have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-patrol-2026)
- [README.md](artifact/README.md)
- [README_INSPECTION.md](artifact/README_INSPECTION.md)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, guidance]

**Output Format:** [Console text report with optional JSON report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include host, operating system, layer results, health scores, risk counts, and remediation suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
