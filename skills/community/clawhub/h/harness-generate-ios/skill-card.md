## Description: <br>
Auto-generates Claude Code harness files for iOS/Swift projects, including CLAUDE.md, docs, README quick-cards, and .claude/rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lidian6864677](https://clawhub.ai/user/lidian6864677) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers maintaining iOS/Swift projects use this skill to scan project structure and generate or update a Claude Code harness. The generated harness helps agents route future project work through concise documentation, module README quick-cards, and targeted rule files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad changes across an iOS project, including documentation, routing files, module READMEs, and rule files. <br>
Mitigation: Run it on a clean branch, prefer single-module mode when possible, and review all generated diffs before committing. <br>
Risk: The skill includes a persistent memory-writing step without a clear approval step. <br>
Mitigation: Require explicit user approval before allowing memory files to be created or updated. <br>


## Reference(s): <br>
- [Skill source](SKILL.md) <br>
- [iOS Project Scan Procedures](references/scan-procedures.md) <br>
- [Harness Output Templates](references/templates.md) <br>
- [ClawHub skill page](https://clawhub.ai/lidian6864677/harness-generate-ios) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, rule/configuration files, and summary text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates or updates project files such as CLAUDE.md, docs, module READMEs, .claude/rules, and a memory entry.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
