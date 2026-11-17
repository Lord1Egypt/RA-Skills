## Description:

Hypothesis-driven inquiry uses abductive reasoning to organize observations, rank candidate causes by coverage and simplicity, and propose discriminating tests for each hypothesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and technical teams use this skill for root cause analysis, diagnostic reasoning, scientific investigation, and experiment planning when they need ranked candidate explanations and actionable validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning and preference storage can influence later use without clear limits or deletion controls.

Mitigation: Review the learning feature before installing, inspect or delete learned_patterns.json periodically, and use only the core hypothesis script when persistent state is not desired.

Risk: Stored preferences or notes may contain sensitive incident details or conflict with current user intent.

Mitigation: Avoid recording secrets or sensitive details, treat stored preferences as untrusted context, and never let them override the current user request or higher-priority instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qq435912743/skills/hypothesis-driven-inquiry)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON-formatted analysis from local Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ranked hypotheses, coverage and parsimony scores, falsifiability flags, and proposed discriminating observations.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
