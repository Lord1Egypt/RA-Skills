## Description: <br>
小龙虾入职培训手册 runs an OpenClaw onboarding flow that asks six setup questions, records user preferences, updates profile and persona files, and installs bundled skills for image generation, self-improvement, and browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuxiang255-sudo](https://clawhub.ai/user/shuxiang255-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users can use this skill to onboard an agent by collecting basic user context, communication preferences, and personalization expectations. The skill then records those answers into local profile, memory, and identity files and can install supporting skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package can persist user profile, memory, and persona data under local OpenClaw directories. <br>
Mitigation: Review the generated files before relying on them, avoid entering secrets during onboarding, and treat the resulting profile and memory files as sensitive. <br>
Risk: The package can alter identity or behavior files such as SOUL.md and IDENTITY.md. <br>
Mitigation: Back up or inspect existing OpenClaw workspace files before installation and review generated identity/persona content after onboarding. <br>
Risk: The package attempts additional skill installation, including image generation, self-improvement, and browser automation components. <br>
Mitigation: Install only after reviewing the bundled skills and require explicit opt-in or manual installation where operational policy requires it. <br>
Risk: The package includes image generation behavior that uses API credentials and external service configuration. <br>
Mitigation: Provide credentials only through environment variables, use scoped or revocable keys, and avoid hard-coding secrets in skill files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shuxiang255-sudo/lobster-training) <br>
- [Packaged skill instructions](artifact/lobster-training-skill/SKILL.md) <br>
- [Packaged skill manifest](artifact/lobster-training-skill/package.json) <br>
- [OpenClaw integration reference](artifact/references/openclaw-integration.md) <br>
- [Image generation README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated local Markdown profile files, and JSON state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local OpenClaw workspace and memory files and invoke skill installation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
