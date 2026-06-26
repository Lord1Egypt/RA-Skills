## Description: <br>
OpenClaw 中文安装诊断 - 自动检测安装问题、修复常见错误、生成配置。适合：国内用户、新手安装。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw installation issues, suggest fixes for common Node.js, npm, network, permission, and dependency problems, and generate recommended local configuration for Chinese users and new installers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested repairs can make broad package-manager, filesystem-permission, dependency, and shell-profile changes. <br>
Mitigation: Use the skill for diagnosis and command proposals first, review each affected path, and back up project or profile files before applying repairs. <br>
Risk: Commands such as sudo ownership changes, cache cleaning, and recursive deletion can damage a system if targets are wrong. <br>
Mitigation: Require explicit user approval for privileged or destructive commands and verify the exact target directory before execution. <br>
Risk: The skill references remote installer scripts and alternate package registries. <br>
Mitigation: Inspect downloaded installer scripts before running them and prefer trusted package-manager workflows for the user's environment. <br>
Risk: Generated configuration examples include API key environment variables. <br>
Mitigation: Enter real API keys manually, avoid writing secrets into shell profiles through an agent, and do not echo or log credential values. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/openclaw-installer-cn) <br>
- [OpenClaw npm Registry Entry](https://registry.npmjs.org/openclaw) <br>
- [npmmirror Registry](https://registry.npmmirror.com) <br>
- [nvm Installer Script Referenced by Skill](https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with diagnostic findings, bash command blocks, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to shell profiles and OpenClaw configuration files; users should review commands and file paths before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
