## Description: <br>
Adds an OCEAN-based personality, emotional response, and persistent preference layer for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neshama-ai](https://clawhub.ai/user/neshama-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to give an agent a persistent personality, emotional tone, and remembered coding preferences across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist user preferences and technical decisions in local markdown files. <br>
Mitigation: Require user confirmation before writing to USER.md or SOUL.md, and periodically review or delete stored preferences. <br>
Risk: API-backed features can send message context to an external provider. <br>
Mitigation: Disable API-backed features for sensitive work and avoid sending secrets, proprietary code, or regulated data to the provider. <br>
Risk: The release includes a public beta API key and API usage limits. <br>
Mitigation: Use a personal key for production workflows, review credential handling, and rely on local fallback configuration when the API is unavailable or rate-limited. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neshama-ai/neshama-soul) <br>
- [Neshama website](https://neshama.pw) <br>
- [SoulCraft](https://neshama.pw/soulcraft) <br>
- [Neshama API documentation](https://api.neshama.pw/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown guidance with JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist user preferences in local markdown files and may call the Neshama Soul API when API-backed features are enabled.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
