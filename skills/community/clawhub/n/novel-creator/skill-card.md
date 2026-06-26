## Description: <br>
Novel Creator helps agents plan, initialize, continue, and revise Chinese long-form fiction projects with reusable style guidance, project memory, chapter drafting, and consistency checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[km1001](https://clawhub.ai/user/km1001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers and creative-writing agents use this skill to turn a novel idea, outline, draft, or ongoing serial into a tracked writing workspace with plan files, memory files, style guidance, and chapter output. It is especially oriented toward Chinese web novels and long-form fiction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initialize and update local novel-project files, and its clean option can replace existing workspace state. <br>
Mitigation: Run it from the intended project folder, review the target directory before initialization, and use the built-in backup behavior when cleaning an existing workspace. <br>
Risk: Novel project folders may contain drafts, private notes, or sensitive material if users place them there. <br>
Mitigation: Avoid storing secrets in the project directory and review project files before sharing or publishing generated outputs. <br>
Risk: The bundled reference catalog may not cover every genre or representation need. <br>
Mitigation: Override or supplement the bundled references when a project requires broader or more inclusive genre coverage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/km1001/novel-creator) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Chapter guide](artifact/references/chapter-guide.md) <br>
- [Character building](artifact/references/character-building.md) <br>
- [Consistency guide](artifact/references/consistency.md) <br>
- [Plot structures](artifact/references/plot-structures.md) <br>
- [Quality checklist](artifact/references/quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown prose, local project files, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update plan, memory, output, backup, and manifest files in the selected novel project directory.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata; artifact frontmatter lists 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
