## Description: <br>
Use when studying or normalizing Chinese lesson transcript/subtitle inputs with bundled public lesson data, learner docs, local export bundles, and pilot-first prepublish leak gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, tutors, and content operators use this skill to study sanitized Chinese lesson data, normalize transcript or subtitle inputs, create learner-facing Markdown and JSON lesson assets, and apply pilot-first publication gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some referenced course-data and system-prompt assets may be absent from the published package. <br>
Mitigation: Confirm the referenced assets are present in the source repository before relying on course data, prompt packs, or publication checks. <br>
Risk: Repository or Drive-sync commands could affect local files or exports if run without checking the command and target folder. <br>
Mitigation: Approve only exact commands shown in the conversation, and require a user-supplied local Drive mount for optional sync. <br>
Risk: Unsupported or incomplete lesson source material can lead to guessed Chinese text, weak answer keys, or synthetic filler. <br>
Mitigation: Keep uncertainty visible, require transcript or subtitle input for new material, and reject unsupported lesson content during review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/openclaw-agent-chinese-laoshi) <br>
- [Metadata Homepage](https://github.com/zack-dev-cm/openclaw-agent-chinese-laoshi) <br>
- [Pipeline Reference](references/pipeline.md) <br>
- [Release Gates](references/release-gates.md) <br>
- [ChatGPT Connector Guidance](references/chatgpt-connector-guidance.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with optional JSON lesson assets and explicit command proposals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Repository commands require explicit user confirmation; optional Drive sync requires a user-supplied local mount and documented repo command.] <br>

## Skill Version(s): <br>
1.0.15 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
