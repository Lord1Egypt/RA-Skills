## Description: <br>
Write Obsidian-compatible .md notes and .canvas files for notes, knowledge bases, daily logs, project docs, and canvas diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hekate2639](https://clawhub.ai/user/hekate2639) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and knowledge workers use this skill to create Obsidian vault notes, project documentation, daily logs, and JSON Canvas diagrams with Obsidian-specific syntax. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to write, commit, and push Obsidian vault changes without a review step. <br>
Mitigation: Require the agent to show changed files and wait for explicit approval before any commit or push. <br>
Risk: Private or sensitive notes may be exposed if the vault syncs to the wrong Git remote or a public repository. <br>
Mitigation: Confirm the vault path and Git remote before use, and keep the repository private when notes contain sensitive information. <br>


## Reference(s): <br>
- [JSON Canvas Spec 1.0](references/canvas-spec.md) <br>
- [Obsidian Supported File Formats](references/file-formats.md) <br>
- [JSON Canvas 1.0 Specification](https://jsoncanvas.org/spec/1.0/) <br>
- [Obsidian File Formats](https://help.obsidian.md/file-formats) <br>
- [JSON Canvas GitHub Repository](https://github.com/obsidianmd/jsoncanvas) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Obsidian Markdown files and JSON Canvas .canvas files, with optional Git shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to a configured Obsidian vault path; canvas output should validate as JSON Canvas 1.0.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
