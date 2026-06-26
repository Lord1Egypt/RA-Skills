## Description: <br>
Mindgraph helps agents create, query, and maintain an Obsidian-style wikilink knowledge graph and reusable MindSkills in OpenClaw workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hulkworks](https://clawhub.ai/user/hulkworks) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Mindgraph to connect workspace Markdown files with wikilinks, query relationships, and store repeatable analysis processes with structured results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks to become a workspace-wide Markdown knowledge-graph convention. <br>
Mitigation: Install it only when that convention is desired, review significant Markdown changes, and rebuild the index after intentional updates. <br>
Risk: MindSkill execution and learning can create persistent process and result files. <br>
Mitigation: Treat MindSkill execution and learning as opt-in, and review saved PROCESS.md files before reuse. <br>
Risk: Untrusted or path-like MindSkill names may lead to unsafe file creation behavior. <br>
Mitigation: Avoid untrusted or path-like names until the learn command validates names as safe slugs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hulkworks/mindgraph) <br>
- [MindGraph Philosophy](artifact/references/philosophy.md) <br>
- [Knockout Test Process](artifact/mindskills/knockout-test/PROCESS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated workspace Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local graph indexes, MindSkill process files, and MindSkill result files in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
