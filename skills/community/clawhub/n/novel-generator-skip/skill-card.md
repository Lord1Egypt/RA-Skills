## Description: <br>
Helps an agent expand a user's fiction direction into a Chinese web-novel prompt, outline, chapters, continuity notes, and optional Mermaid-style story diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejianjun000](https://clawhub.ai/user/xiejianjun000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and creative-writing agents use this skill to generate Chinese genre fiction from short directions, then maintain chapter continuity through local memory files for characters, locations, plot points, world rules, and errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores novel drafts, prompts, and continuity notes in local output/ and .learnings/ files, which may contain sensitive or private story material. <br>
Mitigation: Use it only in an appropriate workspace and avoid placing sensitive personal information in prompts, drafts, or memory files. <br>
Risk: The initialization script's --clean option removes existing Markdown output and resets continuity memory files. <br>
Mitigation: Back up output/ and .learnings/ before running initialization with --clean. <br>
Risk: Optional image-generation workflows may send story content outside the local workspace. <br>
Mitigation: Confirm the selected image-generation tool and data-sharing behavior before using it with private story content. <br>


## Reference(s): <br>
- [Prompt Guide](references/prompt-guide.md) <br>
- [Plot Structures](references/plot-structures.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with optional Mermaid diagrams and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces prompts, outlines, chapter drafts, continuity notes, error logs, and optional diagram files in the local workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact frontmatter, artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
