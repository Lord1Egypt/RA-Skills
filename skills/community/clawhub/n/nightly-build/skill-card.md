## Description:

Automates nightly maintenance tasks like skill audits, updates, cleanup, and health checks, then summarizes a morning report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xraini](https://clawhub.ai/user/0xraini)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Nightly Build to schedule unattended workspace maintenance and receive a concise morning report covering system health, disk usage, skill inventory, git status, cleanup, and memory statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended nightly maintenance can run update and cleanup tasks while the operator is away.

Mitigation: Before enabling cron, restrict exactly which repositories and paths may be updated or cleaned, and review any auto-update behavior.

Risk: Security audit reporting may be misleading if npm audit failures are handled as successful checks.

Mitigation: Fix or review audit failure handling before relying on the generated security summary.

Risk: The schedule and report timestamps use an Asia/Shanghai timezone in the provided setup and script.

Mitigation: Adjust the cron timezone and script timezone to match the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xraini/skills/nightly-build)
- [The Nightly Build inspiration](https://www.moltbook.com/post/562faad7-f9cc-49a3-8520-2bdf362606bb)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown report with system, disk, skill inventory, git, cleanup, and memory sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local nightly report file when run by the script.]

## Skill Version(s):

1.1.0 (source: server release metadata; changelog v1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
