## Description: <br>
Adaptive Suite helps agents provide adaptive coding, business analysis, project management, web and data development, free-resource discovery, and read-only NAS metadata scanning support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and project leads use this skill to get adaptive implementation guidance, planning support, tool recommendations, data workflows, and read-only NAS metadata scanning assistance. It is suited to broad assistant workflows where external API use and local file metadata handling are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use an external API key and broad assistant behaviors, which can expose sensitive prompts, project details, or tool metadata if used without review. <br>
Mitigation: Review before installing, configure only the intended SkillBoss API credential, and avoid sending private project or file metadata to external services unless explicitly intended. <br>
Risk: NAS metadata scanning can expose sensitive file names, directory structure, or metadata. <br>
Mitigation: Approve only specific folders, avoid sensitive shares, keep scanning read-only, and inspect generated desktop-app code before running it. <br>


## Reference(s): <br>
- [Adaptive Suite on ClawHub](https://clawhub.ai/marjoriebroad/mar-adaptive-suite) <br>
- [Moltbot Skills Documentation](https://docs.molt.bot/tools/skills) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recommendations that depend on project context, approved local paths, and configured SkillBoss API credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
