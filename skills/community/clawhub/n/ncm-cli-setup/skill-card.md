## Description:

Installs and configures ncm-cli, including API key setup, optional mpv installation, default player selection, login, and basic troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junfengl](https://clawhub.ai/user/junfengl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to install the NetEase Cloud Music CLI, configure credentials and playback, and resolve common setup issues across macOS, Linux, and Windows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run package-manager commands that change the host system, including sudo-backed Linux installs and repository-enabling steps.

Mitigation: Review exact install commands before execution and confirm any sudo, repository, or package-manager change manually.

Risk: The setup process stores privateKey and login-session credentials for ncm-cli.

Mitigation: Treat the API privateKey and login session as sensitive credentials and avoid exposing them in shared terminals, logs, or transcripts.

Risk: The npm package and mpv installer are not pinned or independently verified by the skill.

Mitigation: Prefer pinning or verifying the npm package and mpv installation source before use.

## Reference(s):

- [NetEase Cloud Music Developer Platform API Key Application](https://developer.music.163.com/st/developer/apply/account?type=INDIVIDUAL)
- [mpv Installation](https://mpv.io/installation/)
- [ClawHub Skill Page](https://clawhub.ai/junfengl/skills/ncm-cli-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OS-specific package-manager commands and credential-handling guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
