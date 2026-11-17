## Description:

Disciplined diagnosis loop for hard bugs and performance regressions, guiding agents through reproduction, minimization, hypothesis generation, instrumentation, fixes, regression tests, and cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to diagnose difficult bugs and performance regressions with a structured feedback-loop-first workflow. It is intended for debugging, regression analysis, targeted instrumentation, fix verification, and post-mortem cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Debugging work may involve proposed tests, scripts, profiling, temporary logs, or code and environment changes.

Mitigation: Review proposed changes before execution and remove temporary instrumentation during cleanup.

Risk: The skill can guide agents to request captured artifacts or temporary production instrumentation when no reliable feedback loop exists.

Mitigation: Share only approved artifacts and require normal review and approval before production instrumentation.

## Reference(s):

- [Mp Diagnose ClawHub Page](https://clawhub.ai/paudyyin/skills/mp-diagnose)
- [paudyyin ClawHub Profile](https://clawhub.ai/user/paudyyin)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command, test, instrumentation, and code-change recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable skill code; output depends on the target debugging task and repository context.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
