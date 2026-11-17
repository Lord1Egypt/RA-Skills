## Description:

AI Agent judgment enhancement via Monte Carlo lookahead, risk-adjusted utility, and historical reflection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen-feng123](https://clawhub.ai/user/chen-feng123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to evaluate candidate actions under uncertainty with configurable lookahead depth, simulation breadth, risk tolerance, and outcome history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes documentation issues, including Chinese-only reference docs and inaccurate CognitiveEnhancer/setup.bat references.

Mitigation: Review the bundled reference docs and examples before relying on the skill in production workflows.

Risk: The skill provides local decision-support code whose recommendations depend on the caller's world model, objective function, and tuning parameters.

Mitigation: Validate world-model behavior, objective scoring, and risk-tolerance settings against expected outcomes before using recommendations for consequential decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chen-feng123/skills/judgment-enhancement-engine)
- [API specification](references/API_SPEC.md)
- [Use guide](references/USE_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns decision recommendations, per-action scores, risk metrics, confidence values, and human-readable reasoning when used as a Python library.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
