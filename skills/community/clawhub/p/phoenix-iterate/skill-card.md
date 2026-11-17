## Description:

AI-driven quantitative strategy iteration workflow - a complete loop of briefing, hypothesis, code generation, constitutional scan, backtest submission, forensic diagnosis, and lesson recording for QuantConnect strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tltby12341](https://clawhub.ai/user/tltby12341)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and quantitative strategy builders use this skill to run a disciplined iteration loop for QuantConnect strategies, including briefing, hypothesis selection, code scanning, progressive backtest validation, diagnosis, and lesson recording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled run metadata can become persistent LLM guidance through constitutional memory.

Mitigation: Use the skill only with trusted inputs, review or sanitize memory/lessons.json before briefings, and avoid recording untrusted free-form metadata.

Risk: Unpinned dependency and loose path/input handling can reduce reproducibility or allow unintended files to influence an iteration workflow.

Mitigation: Run the skill in a dedicated strategy workspace, pin pandas for production use, and add path and input validation before relying on autonomous iteration.

## Reference(s):

- [Phoenix Iterate on ClawHub](https://clawhub.ai/tltby12341/skills/phoenix-iterate)
- [Publisher profile](https://clawhub.ai/user/tltby12341)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands, JSON records, and code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses python3 and requires separately installed backtest-poller and qc-deep-feature-forensics skills for the full workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
