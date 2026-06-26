## Description: <br>
Adaptive Suite helps Clawdbot act as a coder, business analyst, project manager, web developer, data analyst, and read-only NAS metadata scraper while discovering free resources and adapting guidance to user context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and project teams use this skill for coding guidance, business and project analysis, web and data development support, resource discovery, and read-only NAS metadata collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SkillBoss API key and may use an external API for resource discovery. <br>
Mitigation: Install only when the API key can be scoped and stored securely, and review what project or business context may be sent to the external service. <br>
Risk: NAS metadata scanning could expose sensitive filenames, directory structures, or other metadata. <br>
Mitigation: Restrict scans to explicit non-sensitive paths and review collected metadata before sharing it outside the local environment. <br>
Risk: The security summary notes broad work access and vague learning behavior without clear privacy and control boundaries. <br>
Mitigation: Avoid providing credentials, sensitive project data, or confidential business context unless retention and data-use behavior are understood. <br>


## Reference(s): <br>
- [Moltbot Skills Documentation](https://docs.molt.bot/tools/skills) <br>
- [SkillBoss API Hub Endpoint](https://api.heybossai.com/v1/pilot) <br>
- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/modesty-adaptive-suite) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown text with code, shell command, and configuration snippets when useful.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recommendations, analysis workflows, library suggestions, and read-only NAS metadata collection plans.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
