## Description: <br>
AI agent self-portrait generator for creating avatars, profile pictures, and visual identity with SkillBoss API Hub image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to generate visual identity assets such as avatars, banners, and full-body portraits for agents, profiles, and periodic identity refresh workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts, personality details, and the SkillBoss API key are sent to an external image API. <br>
Mitigation: Use a trusted SkillBoss API key, avoid confidential details in prompts, and keep the API key in the runtime environment instead of committing it. <br>
Risk: Automated avatar updates could publish an unsuitable or unintended generated image. <br>
Mitigation: Require human confirmation before workflows update public Discord, Twitter/X, AgentGram, or other profile images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-agent-selfie) <br>
- [Publisher profile](https://clawhub.ai/user/modestyrichards) <br>
- [SkillBoss API endpoint](https://api.heybossai.com/v1) <br>
- [OpenClaw](https://openclaw.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill's script can produce PNG image files and an HTML gallery when run with a valid SkillBoss API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
