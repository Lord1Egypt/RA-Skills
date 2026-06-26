## Description: <br>
Zero-auth static game hosting via the server's local nginx instance for browser games served at a permanent public HTTPS URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogerwu188](https://clawhub.ai/user/rogerwu188) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to deploy, update, list, and verify static browser games on the configured nginx host. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or overwrite live public static files and reload nginx. <br>
Mitigation: Require explicit approval for each deployment, verify the game name and source build directory, and keep backups or versioned deployments before overwriting existing games. <br>
Risk: Public deployments may expose secrets, private assets, or unintended build artifacts. <br>
Mitigation: Inspect files before copying them to the games directory and confirm that the release contains only intended static assets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rogerwu188/nginx-hosting) <br>
- [Hosted games base URL](https://roger-us02.clawln.net/games/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets static files only; no server-side logic or databases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
