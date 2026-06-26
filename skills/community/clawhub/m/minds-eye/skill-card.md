## Description: <br>
Remember and retrieve visual content from conversations, including images, charts, diagrams, screenshots, websites, and similar past visual memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Horisky](https://clawhub.ai/user/Horisky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to give an agent durable visual memory: analyzing images or website screenshots, storing descriptions and tags locally, and searching or listing remembered visual content later. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores visual memories locally and sends images or screenshots to the configured vision provider for analysis. <br>
Mitigation: Avoid confidential images, private websites, admin pages, credentials, or regulated data unless local retention and provider transmission are acceptable. <br>
Risk: Durable visual memory may retain content longer than the user expects. <br>
Mitigation: Periodically review or delete ~/.multimodal-memory/ when retained memories are no longer needed. <br>


## Reference(s): <br>
- [minds-eye on ClawHub](https://clawhub.ai/Horisky/minds-eye) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus script output for analysis results, search results, local image files, SQLite records, and memory.md summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores visual memories under ~/.multimodal-memory/ and uses a configured vision provider for image analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
