## Description: <br>
OpenClaw 초보자를 위한 풀패키지 온보딩 스킬로, 첫 세팅부터 보안 강화까지 대화형으로 안내한다. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyeuun97](https://clawhub.ai/user/gyeuun97) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to complete a guided first-time OpenClaw setup, including profile files, memory structure, heartbeat automation, recommended skills, cron basics, and security hardening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent profile, memory, heartbeat, and setup files that may affect future agent behavior. <br>
Mitigation: Review generated SOUL.md, USER.md, MEMORY.md, and HEARTBEAT.md before relying on them. <br>
Risk: Profile and memory files could accidentally contain API keys or sensitive personal data. <br>
Mitigation: Keep secrets out of memory and profile files; use environment variables or OpenClaw configuration for API keys. <br>
Risk: Cron or heartbeat automation may run recurring actions that the user did not intend. <br>
Mitigation: Confirm any cron or heartbeat automation before enabling it and periodically review active jobs. <br>
Risk: Recommended third-party skills may introduce separate permissions, dependencies, or behavior. <br>
Mitigation: Review each recommended third-party skill independently before installing it. <br>


## Reference(s): <br>
- [OpenClaw Starter Kit release page](https://clawhub.ai/gyeuun97/openclaw-starter-kit) <br>
- [OpenClaw security guide](guides/security-guide.md) <br>
- [OpenClaw skill recommendations](guides/skill-recommendations.md) <br>
- [OpenClaw cron basics](guides/cron-basics.md) <br>
- [Brave Search API](https://brave.com/search/api/) <br>
- [OpenClaw Discord community](https://discord.com/invite/clawd) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated setup file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions and proposed SOUL.md, USER.md, MEMORY.md, HEARTBEAT.md, and related workspace files for user review.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; package.json declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
