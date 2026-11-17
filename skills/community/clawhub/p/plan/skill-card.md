## Description:

Plans tasks before execution by deciding when to plan versus act directly, sizing plan depth to risk, and structuring steps, estimates, validation, and rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to decide when planning is warranted, choose an appropriate plan depth, and produce concise execution plans with risks, estimates, validation points, and rollback handling for multi-step or irreversible work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local planning records may contain sensitive project details.

Mitigation: Install only if local records under ~/Clawic/data/plan/ are acceptable; review or delete that directory when plans may contain sensitive information.

Risk: Auto-execution defaults can reduce human review for high-impact work if configured too broadly.

Mitigation: Keep destructive, production, financial, external-send, and other irreversible work in always_validate.

## Reference(s):

- [ClawHub Plan Skill Page](https://clawhub.ai/ivangdavila/skills/plan)
- [Plan Homepage](https://clawic.com/skills/plan)
- [Setup Guide](setup.md)
- [Risk Guidance](risk.md)
- [Approval Guidance](approval.md)
- [Decomposition Guidance](decomposition.md)
- [Estimation Guidance](estimation.md)
- [Replanning Guidance](replanning.md)
- [Long-Horizon Planning Guidance](long-horizon.md)
- [Outcome Tracking Guidance](outcomes.md)
- [Planning Strategies](strategies.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, files]

**Output Format:** [Markdown or plain text planning guidance with optional local planning records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist planning preferences, active plans, and outcome logs under ~/Clawic/data/plan/ when the workflow calls for it.]

## Skill Version(s):

1.0.3 (source: artifact/SKILL.md frontmatter and evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
