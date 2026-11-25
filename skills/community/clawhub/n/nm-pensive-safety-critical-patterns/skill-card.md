## Description:

Applies NASA Power of 10 rules for safety-critical verifiable code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to review safety-critical code against defensive coding rules and produce grounded findings with concrete remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was incomplete because two referenced files were absent from the artifact, so its benign verdict does not cover those files.

Mitigation: Review the missing referenced files and their behavior before relying on the scan assessment.

## Reference(s):

- [Pensive plugin project page (Clawdis homepage metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review findings with rule verdicts, source locations, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: release evidence; artifact frontmatter lists 1.10.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
