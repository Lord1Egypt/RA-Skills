## Description: <br>
Creates behavioral rules in markdown to block dangerous commands or restrict AI behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to write persistent local Hookify rules that warn on or block matching commands, file edits, prompts, or session-stop events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local Hookify rules can affect future sessions by warning on or blocking matching commands and edits. <br>
Mitigation: Review generated .claude/hookify.*.local.md rules before keeping them, and prefer warning rules before blocking rules when testing a new pattern. <br>
Risk: Overbroad or invalid regex patterns can match unintended actions or fail to match the intended text. <br>
Mitigation: Test regex patterns with a small Python check and scope rules to the relevant event fields before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-hookify-writing-rules) <br>
- [Hookify homepage](https://github.com/athola/claude-night-market/tree/master/plugins/hookify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with YAML rule examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local .claude/hookify.*.local.md rule files.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
