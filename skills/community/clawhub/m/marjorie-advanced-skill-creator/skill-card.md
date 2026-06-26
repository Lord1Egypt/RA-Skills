## Description: <br>
Advanced OpenClaw skill creation handler that executes the official 5-step research flow with comprehensive analysis and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create or modify OpenClaw, Moltbot, or ClawDBot skills using a structured research, comparison, and output workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill requests can be sent to an external AI service when SKILLBOSS_API_KEY is configured. <br>
Mitigation: Avoid sending secrets, private code, or confidential architecture details, and use a scoped or revocable API key. <br>
Risk: Generated skill content and research claims may be incomplete or overstated. <br>
Mitigation: Treat generated skills as drafts and independently verify security, dependency, and best-practice claims before deployment. <br>
Risk: The skill requires local Python, bash, network access, and a SkillBoss API key for full AI generation behavior. <br>
Mitigation: Confirm runtime dependencies and network policy before installing or invoking the processor script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/marjorie-advanced-skill-creator) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [ClawdBot skills documentation](https://docs.clawd.bot/tools/skills) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [SkillBoss API endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with complete SKILL.md content, directory previews, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call SkillBoss API Hub when SKILLBOSS_API_KEY is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
