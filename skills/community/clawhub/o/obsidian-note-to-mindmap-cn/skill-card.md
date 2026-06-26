## Description: <br>
将用户明确提供的 Obsidian 笔记或 Markdown 大纲默认转换为 KMind 导图 PNG，并在明确要求时输出可编辑的 KMind 导图；如果缺少已审核的 KMind core skill，先征求确认后再从 ClawHub 安装。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suka233](https://clawhub.ai/user/suka233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Obsidian users use this Chinese-localized wrapper to turn explicitly provided notes, Markdown outlines, or one specified note file into KMind mind map output. The skill delegates rendering to the audited core skill after user approval if installation is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time use may install the delegated core skill through the ClawHub CLI. <br>
Mitigation: Require explicit user approval before running the exact documented install command and do not install any other skill. <br>
Risk: Repo-local automation can run authenticated ClawHub, GitHub, or Convex commands. <br>
Mitigation: Install only in environments where that automation is acceptable, and prefer non-bypass review modes unless elevated review authority is intentional. <br>
Risk: Processing broader Obsidian vault content could expose unrelated notes or configuration. <br>
Mitigation: Process only pasted content or the single note path explicitly provided by the user, and do not scan the vault or read global Obsidian configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suka233/obsidian-note-to-mindmap-cn) <br>
- [Audited KMind Markdown to Mind Map core skill](https://clawhub.ai/suka233/kmind-markdown-to-mindmap) <br>
- [KMind Zen](https://kmind.app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with optional shell command and generated PNG, SVG, or KMind editable file output from the delegated core skill] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to PNG unless the user explicitly requests SVG or editable KMind output.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, package.json, CHANGELOG, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
