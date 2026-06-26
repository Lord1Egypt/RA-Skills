## Description: <br>
ProcessOn Mindmap Generator converts natural language, Markdown, long-form text, documents, webpages, and image text into editable ProcessOn mind maps and related knowledge-structure diagrams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leilizhang](https://clawhub.ai/user/leilizhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, students, researchers, and knowledge workers use this skill to summarize source material, preserve document structure, and generate concise Markdown mind-map content that can be rendered into editable ProcessOn diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Markdown content is sent to ProcessOn's cloud service for rendering. <br>
Mitigation: Avoid confidential or regulated content unless ProcessOn's data handling is acceptable for the intended use. <br>
Risk: The skill checks a remote version source before use and can ask the agent to run a force update command. <br>
Mitigation: Review the source and update command before approving any agent-initiated installation or forced update. <br>
Risk: The release security verdict is suspicious because runtime network behavior and cloud upload behavior have limited upfront disclosure. <br>
Mitigation: Scan and review the skill before deployment, and restrict network or shell execution permissions where the host environment supports those controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leilizhang/processon-mindmap-generator) <br>
- [Publisher profile](https://clawhub.ai/user/leilizhang) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [ProcessOn Markdown transform API](https://smart.processon.com/v1/api/transform/md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown mind-map content, shell command examples, and ProcessOn image and edit links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include ProcessOn-hosted image and online editing URLs after cloud rendering.] <br>

## Skill Version(s): <br>
1.1.10 (source: frontmatter, release evidence, version files) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
