## Description: <br>
Creates behavioral rules in markdown to block dangerous commands or restrict AI behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to write local Hookify markdown rules that warn on or block unsafe commands, file edits, prompts, or stop conditions in Claude Code sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Enabled block rules can affect later agent sessions until they are disabled or deleted. <br>
Mitigation: Review each generated .claude/hookify.*.local.md rule before relying on it, and disable or delete rules that are too broad. <br>
Risk: Regular expression patterns can overmatch safe activity or miss the intended command or file content. <br>
Mitigation: Test patterns before enabling rules, start with warn actions when practical, and keep rule messages clear about the intended guardrail. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-hookify-writing-rules) <br>
- [Hookify homepage](https://github.com/athola/claude-night-market/tree/master/plugins/hookify) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML frontmatter examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Hookify rule guidance and examples for .claude/hookify.*.local.md files.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
