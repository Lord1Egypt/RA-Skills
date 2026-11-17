## Description:

GitHub App helps agents and automations authenticate through GitHub Apps so git and gh actions use installation tokens and bot attribution across one or more profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eliasempresas](https://clawhub.ai/user/eliasempresas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation maintainers use this skill to configure ghapp, manage GitHub App profiles, and run git and gh commands with GitHub App installation-token authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses a third-party credential tool that can persist changes to Git and GitHub CLI authentication.

Mitigation: Review the ghapp upstream project and Homebrew tap before installing, test configuration in an isolated environment, and use ghapp auth status or reset commands to inspect or undo local auth changes.

Risk: GitHub App credentials, private keys, installation tokens, and local token caches can expose repository access if mishandled.

Mitigation: Use a least-privilege GitHub App installed only on required repositories, protect the private key, avoid printing tokens in shared logs, and rotate credentials if exposure is suspected.

Risk: Shell hooks, path shims, config files, and token caches may continue affecting commands after initial setup.

Mitigation: Document the selected auth mode, understand which files and shell integrations persist on the machine, and prefer scoped profiles for separate clients or organizations.

## Reference(s):

- [GitHub App Skill on ClawHub](https://clawhub.ai/eliasempresas/skills/github-app)
- [ghapp-cli Repository](https://github.com/eliasempresas/ghapp-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest commands that change Git and GitHub CLI authentication state and local token caches.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
