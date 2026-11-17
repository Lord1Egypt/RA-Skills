## Description:

Helps agents guide users through beautifying a macOS terminal with Ghostty, Starship, Oh My Zsh, Nerd Fonts, and Catppuccin Mocha-style prompt configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaorui](https://clawhub.ai/user/wuhaorui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill when they want an agent to provide terminal appearance setup guidance, including install commands, shell configuration, font setup, Ghostty settings, Starship prompt customization, and environment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide asks users to execute a live remote Oh My Zsh installer with unattended behavior.

Mitigation: Review, pin, or manually inspect the installer before running it; avoid unattended execution where policy requires command review.

Risk: The guide makes persistent shell configuration and locale changes.

Mitigation: Apply those changes only if they match the desired behavior for future shell sessions, and preserve existing local PATH, credential, and API key configuration separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhaorui/skills/macos-terminal-beautify)
- [Oh My Zsh installer](https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)
- [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)
- [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)
- [zsh-completions](https://github.com/zsh-users/zsh-completions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, Zsh, INI, TOML, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a diagnostic shell script for checking fonts, terminal tools, configuration files, plugins, and environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
