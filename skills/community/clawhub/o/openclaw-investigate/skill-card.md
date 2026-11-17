## Description:

Openclaw Investigate guides agents through a systematic root-cause debugging workflow for bugs, abnormal behavior, and service errors, emphasizing investigation, hypothesis validation, minimal fixes, regression tests, and verifiable reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agents through disciplined debugging: collecting symptoms, tracing code paths, checking recent changes, forming testable root-cause hypotheses, validating fixes, and reporting evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using the skill may read relevant project code and run tests while debugging.

Mitigation: Use it in workspaces where code inspection and test execution are expected, and review proposed commands and reports before accepting changes.

Risk: The skill intentionally changes debugging behavior by discouraging unverified symptom fixes.

Mitigation: Require the agent to provide the stated root-cause hypothesis, validation evidence, test output, and final debug report before applying or accepting a fix.

## Reference(s):

- [Openclaw Investigate on ClawHub](https://clawhub.ai/x-rayluan/skills/openclaw-investigate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured debug reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
