## Description: <br>
Oh My Zsh management for adding plugins to .zshrc and authoring $ZSH_CUSTOM/*.zsh configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers who use Oh My Zsh can use this skill to manage plugin entries in .zshrc and create custom zsh startup scripts for aliases, functions, environment variables, and key bindings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide persistent shell startup changes in .zshrc and auto-loaded $ZSH_CUSTOM/*.zsh files. <br>
Mitigation: Review exact file diffs before applying changes and keep backups of existing shell configuration. <br>
Risk: External plugin setup may clone third-party zsh plugin repositories. <br>
Mitigation: Confirm each plugin repository and trust boundary before cloning or adding it to the plugins array. <br>
Risk: The source includes an automatic skill-upgrade instruction unrelated to normal Oh My Zsh management. <br>
Mitigation: Do not allow /skill-manager upgrade omz unless a separate skill update was explicitly requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/omz) <br>
- [Oh My Zsh Plugin Management](artifact/plugin.md) <br>
- [Oh My Zsh Custom Script Authoring](artifact/custom.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to shell startup configuration and Oh My Zsh custom files.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and CHANGELOG, released 2026-06-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
