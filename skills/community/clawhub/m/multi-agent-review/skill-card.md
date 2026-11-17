## Description:

Runs six specialized review agents in parallel to examine code architecture, security, tests, performance, maintainability, and documentation, then consolidates high-confidence findings into one report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review repositories or code changes with multiple specialized agents and receive prioritized findings, conflicts, and recommended actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some review agents can run command execution while reviewing private or untrusted repositories.

Mitigation: Require explicit approval for command execution, run approved commands in an isolated sandbox, or remove exec access from the test and performance agents by default.

Risk: The workflow forwards code context to spawned agents without documented sharing boundaries.

Mitigation: Document what code is shared with each spawned agent, limit review scope to necessary files, and avoid including secrets or sensitive repositories unless policy allows.

## Reference(s):

- [Review workflow](artifact/references/review-workflow.md)
- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/multi-agent-review)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown report with structured finding data from JSON-style agent results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include severity, location, description, suggestion, confidence, per-dimension scores, conflict notes, and recommended actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
