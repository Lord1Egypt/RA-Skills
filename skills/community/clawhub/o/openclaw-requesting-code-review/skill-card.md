## Description: <br>
Use when completing tasks, implementing major features, or before merging - dispatches code review subagent to catch issues before they cascade, adapted for OpenClaw sessions_spawn model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to request focused code review before merges, after substantial implementation work, or when they need an independent review of diffs and requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan classified the release as suspicious because it may resemble a full application repository rather than a scoped installable skill. <br>
Mitigation: Confirm the publisher, expected file list, and package scope before installation or agent use. <br>
Risk: The skill asks agents to collect diffs and prepare code review context, which may include sensitive source details. <br>
Mitigation: Review the diff and prompt context before sharing it with any external reviewer or subagent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/openclaw-requesting-code-review) <br>
- [Skill artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and a subagent review prompt template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewer context and follow-up handling guidance; it does not execute review actions by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
