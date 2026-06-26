## Description: <br>
Open Skills is an interactive CLI skill that helps developers browse, select, install, and sync AI agent skills across multiple editors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lumacoder](https://clawhub.ai/user/lumacoder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to discover, multi-select, install, synchronize, update, export, and import AI agent skills for editors such as Claude Code, Cursor, Windsurf, Cline, Roo-Cline, Antigravity, Hermes, and GitHub Copilot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can modify global or project-level agent and editor configuration. <br>
Mitigation: Prefer local scope first, review selected skills and target directories before applying changes, and back up existing rule or skill directories. <br>
Risk: Update, sync, and import workflows can affect directories that contain manually maintained files. <br>
Mitigation: Avoid running update, sync, or import on manually maintained directories unless the changes have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lumacoder/open-skills) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lumacoder) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [package.json](artifact/package.json) <br>
- [IDE Engine design notes](artifact/docs/ide-engine.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Interactive CLI prompts, terminal output, Markdown skill files, registry JSON, and editor configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can install, sync, update, export, import, and create skill bundles across global or project-level editor targets.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata; artifact frontmatter and package.json state 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
