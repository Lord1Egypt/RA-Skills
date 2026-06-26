## Description: <br>
Detect friction signals during agent sessions and turn recurring patterns into reviewable learning and rule proposals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill during session retrospectives to identify repeated corrections, failed commands, retry loops, and other friction signals, then propose durable guidance for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A separate Claude Code or Night Market plugin may add commands, hooks, or runtime permissions not present in this markdown-only skill. <br>
Mitigation: Review that external plugin separately before installing or enabling it. <br>
Risk: Graduation proposals could turn noisy or misleading session patterns into persistent guidance. <br>
Mitigation: Review the evidence behind each proposal and require explicit user approval before modifying durable guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-abstract-friction-detector) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable friction reports, session-log schemas, scoring guidance, and rule-graduation proposals.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
