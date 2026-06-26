## Description: <br>
Loads SoulPod persona packages so an agent can converse in character, with passive recreation and proactive companion modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evangeliona](https://clawhub.ai/user/evangeliona) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to load SoulPod persona packages for fictional roleplay conversations, including local memory, story baselines, optional diary traces, and optional image or voice generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps local conversation and diary-style memory for roleplay personas. <br>
Mitigation: Use it only when comfortable with local memory retention, review persona memory files periodically, and avoid entering sensitive personal details. <br>
Risk: Image and voice features can send prompts or text to external services and require a MiniMax API key. <br>
Mitigation: Use a dedicated MiniMax API key and avoid including sensitive details in image or voice prompts. <br>
Risk: Cleanup helpers can remove local chat history created by the skill. <br>
Mitigation: Back up chat history before running cleanup or uninstall commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/evangeliona/memory-inhabit) <br>
- [Memory Inhabit product homepage](https://memory-series.github.io/#/product/inhabit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with optional shell command snippets and generated media file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local persona history and diary files, and may call external image or voice services when configured.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
