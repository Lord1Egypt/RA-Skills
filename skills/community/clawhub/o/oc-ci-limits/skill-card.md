## Description:

Manage OpenClaw GitHub Actions and Blacksmith CI capacity, runner-registration budgets, fanout caps, main-push single-flight, shard sizing, hosted-runner offload, queue health, and safe ramp-down/ramp-up changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining OpenClaw CI use this skill to diagnose capacity bottlenecks and plan measured changes to runner budgets, fanout, shard sizing, and hosted-runner placement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports partial coverage and notes broader pull request review and preparation tasks than the stated CI capacity purpose.

Mitigation: Inspect referenced files and review proposed changes before acting on broader review or preparation guidance.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hillstreet-ph/skills/oc-ci-limits)
- [Windows pnpm store measurements (GitHub Actions run)](https://github.com/openclaw/openclaw/actions/runs/35547255790)
- [Hosted Mac dependency measurements (GitHub Actions run)](https://github.com/openclaw/openclaw/actions/runs/33458856298)
- [Actions artifact checkout measurements (GitHub pull request)](https://github.com/openclaw/openclaw/pull/124818)
- [Actions artifact download measurements (GitHub Actions run)](https://github.com/openclaw/openclaw/actions/runs/31971531521)
- [OpenClaw CI run referenced by the skill](https://github.com/openclaw/openclaw/actions/runs/33538827388)
- [ClawSweeper service status](https://clawsweeper.openclaw.ai/api/status)
- [ClawSweeper exact review queue](https://clawsweeper.openclaw.ai/api/exact-review-queue)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and CI configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
