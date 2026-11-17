## Description:

Laizy orchestrates repo-native, supervised software delivery with the Laizy CLI for multi-step coding runs across planning, implementation, recovery, verification, and closeout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaolonggao521](https://clawhub.ai/user/xiaolonggao521)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use Laizy to coordinate supervised, milestone-based software delivery in a repository. The skill helps bootstrap or continue a run by following Laizy-generated plans, contracts, recovery steps, verification commands, and closeout artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned external Laizy CLI package.

Mitigation: Pin and audit the Laizy CLI before installation, and install it only in an isolated repository or disposable environment.

Risk: The skill directs agents to run Laizy-generated verification commands.

Mitigation: Inspect every generated command before execution and avoid exposing unrelated secrets or credentials to the run environment.

Risk: The workflow can include commit and push steps after milestone completion.

Mitigation: Do not allow automatic commits or pushes unless that workflow is explicitly intended and reviewed.

Risk: Generated run artifacts may be needed to understand or audit the coding run.

Mitigation: Archive run artifacts instead of deleting them during review and incident investigation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaolonggao521/skills/laizy)
- [Project homepage from metadata](https://github.com/XiaolongGao521/Laizy)
- [Laizy Decision Map](references/decision-map.md)
- [Planner-Needed Bootstrap Template](references/planner-bootstrap.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration]

**Output Format:** [Markdown guidance with bash command blocks and artifact path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to inspect Laizy-emitted local run artifacts and execute one bounded next action at a time.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
