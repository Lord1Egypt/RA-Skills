## Description: <br>
Generates AI agent self-portraits, profile pictures, banners, and visual identity assets through SkillBoss API Hub image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create profile-ready visual assets for an AI agent identity, including avatars, banners, and vertical portraits. It supports mood and seasonal presets, personality JSON, batch generation, and gallery output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Avatar prompts and personality descriptors are sent to SkillBoss API Hub. <br>
Mitigation: Avoid including secrets, private profile details, or sensitive identity traits in prompts or personality JSON. <br>
Risk: Heartbeat behavior can update Discord, Twitter/X, AgentGram, or other public profile avatars without clear approval controls. <br>
Mitigation: Require explicit user approval for the exact account and generated image before changing any public profile. <br>
Risk: Generated asset paths and style preferences may be saved in agent memory. <br>
Mitigation: Review or disable memory-saving behavior when persistent records of generated images or style preferences are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-agent-selfie) <br>
- [Publisher profile](https://clawhub.ai/user/kirkraman) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [AgentGram related skill](https://clawhub.org/skills/agentgram) <br>
- [gemini-image-gen related skill](https://clawhub.org/skills/gemini-image-gen) <br>
- [opencode-omo related skill](https://clawhub.org/skills/opencode-omo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands; when executed, the skill writes PNG images, prompts.json, and an HTML gallery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and accepts personality JSON, mood, theme, format, count, and output directory options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
