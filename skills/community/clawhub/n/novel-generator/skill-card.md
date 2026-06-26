## Description: <br>
Novel Generator helps agents turn a short Chinese fiction premise into an expanded prompt, outline, serialized Markdown chapters, Mermaid diagrams, and continuity notes for Chinese爽文 stories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ITYHG](https://clawhub.ai/user/ITYHG) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creative writers and agent users use this skill to draft Chinese serialized fiction from a brief direction, then maintain continuity across characters, locations, plot points, and world rules. It is intended for agents that can read and write local workspace files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated fiction, prompts, and continuity notes are saved into the local workspace. <br>
Mitigation: Use the skill only in workspaces where those files are acceptable to store. <br>
Risk: Using `init-novel.sh --clean` resets prior generated chapters and story memory. <br>
Mitigation: Run the clean option only when intentionally starting over or after backing up work that should be preserved. <br>
Risk: Continuity memory can bleed between unrelated novels if the same workspace is reused. <br>
Mitigation: Keep different novels in separate workspaces or clear `.learnings/` before beginning a new project. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ITYHG/novel-generator) <br>
- [Prompt guide](references/prompt-guide.md) <br>
- [Plot structures](references/plot-structures.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>
- [self-improving-agent](https://github.com/peterskoett/self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with Mermaid diagrams, local continuity notes, and optional shell commands for workspace initialization] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes prompts, outlines, chapters, diagrams, and story memory into local workspace files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
