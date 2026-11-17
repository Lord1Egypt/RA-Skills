## Description:

A code review helper that evaluates code across security, performance, correctness, and style perspectives, assigns severity levels, suggests fixes, and returns PASS/BLOCK-style decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure pull request review, security audit, performance review, and code-quality findings before merge or release decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact is incomplete or malformed, and the paid full-implementation claims are not supported by the uploaded files.

Mitigation: Review the artifact manually and validate behavior on representative code before relying on it for PR gates, CI blocking, paid security review, or audit decisions.

Risk: The advertised code review coverage may be narrower than readers expect from the release claims.

Mitigation: Treat findings as advisory and pair the skill with human review and established security, performance, and correctness checks for high-impact decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-code-review)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown code review report with severity-labeled findings and PASS, PASS_WITH_COMMENTS, or BLOCK verdicts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file and line references, remediation suggestions, and severity labels.]

## Skill Version(s):

2.0.0 (source: server release metadata and hub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
