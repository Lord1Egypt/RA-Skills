## Description: <br>
Build, maintain, query, archive, and audit a Markdown / Obsidian knowledge Wiki continuously maintained by an LLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengsusky](https://clawhub.ai/user/fengsusky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to initialize and maintain a local Markdown or Obsidian knowledge wiki, import source materials, connect concepts, answer questions from the wiki, and audit structure and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad wiki reorganization, including renames, moves, and updates across many Markdown files. <br>
Mitigation: Limit the agent to the intended vault and review bulk rename or reorganization plans before applying them. <br>
Risk: Generated or reorganized wiki content can introduce incorrect conclusions, duplicate concepts, broken links, or outdated synthesis pages. <br>
Mitigation: Run the included audit script after imports or refactors and review important knowledge changes before relying on them. <br>
Risk: The audit script prints local file paths and wiki diagnostics. <br>
Mitigation: Treat audit output as local diagnostics and avoid sharing it outside the intended review context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengsusky/llm-obsidian-wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with wiki file changes, Obsidian links, audit findings, and Python or shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local wiki pages and reports local audit diagnostics; no external reporting is described.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
