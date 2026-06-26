## Description: <br>
Private Web App (PWA) helps agents install, run, configure, and extend a personal FastAPI and React PWA dashboard with plugin apps, system monitoring, file browsing, and push notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camopel](https://clawhub.ai/user/camopel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and home-server administrators use this skill to set up and operate a private PWA dashboard, manage its service lifecycle, build frontend assets, add plugin apps, and configure web push notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard can expose local file browsing and downloads from its configured root. <br>
Mitigation: Bind the service to localhost or protect it with strong authentication and firewall or Tailscale ACLs, and configure the file browser to a narrow directory instead of the whole home directory. <br>
Risk: Plugin discovery can load executable app code from configured paths. <br>
Mitigation: Review each plugin path and app before enabling it, and keep discovery paths limited to trusted directories. <br>
Risk: System monitor actions include host restart and shutdown controls. <br>
Mitigation: Disable or remove the reboot and shutdown endpoints unless the deployment explicitly requires remote power controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/camopel/privateapp) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Instructions](artifact/SKILL.md) <br>
- [Tailscale Download](https://tailscale.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell, Python, TypeScript, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file edits, service commands, frontend build commands, and configuration changes for a personal PWA server.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence, created 2026-02-23T01:17:39Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
