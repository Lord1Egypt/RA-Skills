## Description:

Mirrors a target website into a local folder for offline browsing, including network checks, recursive download, filename cleanup, link rewriting, validation, and a localhost preview server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wenbing3049](https://clawhub.ai/user/wenbing3049)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to mirror static or server-rendered websites into a local directory for backup, inspection, or offline browsing. It is not suitable for login-only sites or JavaScript-rendered single-page applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can modify local folders and create or rewrite mirrored files.

Mitigation: Use a new empty dedicated directory and review the proposed paths before running commands.

Risk: The download commands disable TLS certificate checks and ignore site crawling rules.

Mitigation: Remove insecure TLS bypass unless explicitly required, respect site crawling rules, and review the commands before execution.

Risk: The workflow can leave a preview server running after mirroring completes.

Mitigation: Start preview only when needed, bind it to localhost, record the process ID, and stop it after use.

Risk: Mirroring sensitive or login-only sites can capture private content locally.

Mitigation: Avoid using the skill on sensitive, authenticated, or login-only websites.

## Reference(s):

- [Skill README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/wenbing3049/skills/mirror-website)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash commands and generated shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local mirror files, helper shell scripts, and a localhost preview server when followed by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
