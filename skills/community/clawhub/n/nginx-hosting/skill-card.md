## Description:

Zero-auth static game hosting via the server's local nginx instance for browser games, serving static files at permanent public HTTPS URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogerwu188](https://clawhub.ai/user/rogerwu188)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy, update, list, and verify static browser games hosted from an nginx-served games directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated game names or destinations could publish files outside the intended /data/games path or expose sensitive files.

Mitigation: Use strict game-name validation, quote shell variables, and verify the destination remains under /data/games before copying files.

Risk: Updates can replace live public content immediately.

Mitigation: Use a small reviewed deployment script with staging or backups before reloading nginx.

Risk: The raw deployment commands are under-scoped for direct operational use.

Mitigation: Treat the examples as templates and review them before installation or execution.

## Reference(s):

- [Nginx Hosting on ClawHub](https://clawhub.ai/rogerwu188/skills/nginx-hosting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and nginx configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume static files only and an existing nginx configuration serving /data/games/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
