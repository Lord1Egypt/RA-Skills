## Description:

Principles Agent helps OpenClaw users decompose complex goals into first-principles facts, atomic tasks, dependency-aware execution batches, and final markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingxinsuixing](https://clawhub.ai/user/lingxinsuixing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to turn complex objectives into clarified goals, basic assumptions, ordered subtasks, validation checkpoints, and an integrated final answer. It is suited to planning multi-step analysis or implementation work inside OpenClaw, where the main agent performs LLM calls and external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validation flow may be unreliable and should not be treated as a safety gate.

Mitigation: Review generated plans, task outputs, and final reports before relying on them for decisions or deployment.

Risk: The skill may make multiple LLM calls through the OpenClaw main agent.

Mitigation: Run it only in sessions where the prompt content, cost, and data handling expectations are acceptable.

Risk: The optional --output path writes a report file.

Mitigation: Use --output only with paths where you intend to create or overwrite a report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lingxinsuixing/skills/principles-agent)
- [Original principles project](https://github.com/miltonian/principles)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report and structured result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write the generated report to a user-specified path when the --output option is used.]

## Skill Version(s):

0.2.0 (source: evidence.json release.version and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
