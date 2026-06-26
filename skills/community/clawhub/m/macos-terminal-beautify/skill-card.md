## Description: <br>
Helps users beautify a macOS terminal with Ghostty, Starship, Oh My Zsh, and Nerd Font to create a colorful Catppuccin Mocha prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhaorui](https://clawhub.ai/user/wuhaorui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS users use this skill for step-by-step terminal customization, including installing terminal tools, configuring fonts and prompts, and checking the resulting setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terminal setup commands may install packages, run the Oh My Zsh installer, clone plugins, and change local shell configuration. <br>
Mitigation: Review commands before execution, inspect the Oh My Zsh installer, back up ~/.zshrc, and run setup steps manually. <br>
Risk: Terminal and font configuration changes may affect shell behavior or display rendering. <br>
Mitigation: Use the provided self-check script after setup and keep existing local configuration in ~/.zshrc.local or a backup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuhaorui/macos-terminal-beautify) <br>
- [Oh My Zsh installer](https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh) <br>
- [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) <br>
- [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) <br>
- [zsh-completions](https://github.com/zsh-users/zsh-completions) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a shell self-check script for local terminal setup validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
