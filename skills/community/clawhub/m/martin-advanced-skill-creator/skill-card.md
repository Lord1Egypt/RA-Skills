## Description: <br>
Advanced Skill Creator helps create and modify OpenClaw, Moltbot, and ClawDBot skills by following a structured five-step research and synthesis workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to research, design, and generate OpenClaw-compatible skill packages with frontmatter, examples, implementation guidance, and security considerations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User prompts and generated skill context can be sent to an external SkillBoss API. <br>
Mitigation: Use a limited SkillBoss API key and avoid including secrets, credentials, or proprietary project details in skill-generation prompts. <br>
Risk: Activation and install metadata are under-scoped, which can cause the skill to trigger more broadly than intended. <br>
Mitigation: Review and narrow trigger phrases, frontmatter, and install metadata before broad deployment. <br>
Risk: Generated skill content can include incorrect guidance or unsafe implementation details. <br>
Mitigation: Review, test, and scan generated skill packages before installing or publishing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/godferylindsay/martin-advanced-skill-creator) <br>
- [ClawdBot skills documentation](https://docs.clawd.bot/tools/skills) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with file trees, complete SKILL.md content, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the SkillBoss API when SKILLBOSS_API_KEY is configured; generated skill content should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
