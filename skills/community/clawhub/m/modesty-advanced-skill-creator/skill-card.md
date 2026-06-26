## Description: <br>
Advanced OpenClaw skill creation handler that executes the official 5-step research flow with comprehensive analysis and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to draft or modify OpenClaw, Moltbot, and ClawDBot skills with structured research, comparison, and standardized SKILL.md output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends skill-generation prompts and generated context to a third-party SkillBoss API using SKILLBOSS_API_KEY. <br>
Mitigation: Use it only when the data-sharing terms are acceptable, keep the API key in environment configuration, and avoid prompts containing proprietary code, credentials, or private context. <br>
Risk: Security review says the skill overstates its research behavior and its output should be treated as AI-assisted draft material. <br>
Mitigation: Manually verify generated skills against current official documentation and review the output before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-advanced-skill-creator) <br>
- [Claw skills documentation](https://docs.clawd.bot/tools/skills) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [SkillBoss API endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML frontmatter, directory previews, code blocks, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates AI-assisted draft skill content using SkillBoss API when SKILLBOSS_API_KEY is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
