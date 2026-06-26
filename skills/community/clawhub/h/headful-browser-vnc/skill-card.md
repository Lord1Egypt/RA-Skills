## Description: <br>
Headful Chromium with VNC/noVNC operator UI and Chrome CDP exports for cookies, screenshots, and rendered outerHTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waylonsong](https://clawhub.ai/user/waylonsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a server-side headful Chromium session for browser automation workflows that need human interaction, then export browser artifacts for downstream analysis or processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live VNC, noVNC, or Chrome debugging endpoints can expose an active browser session. <br>
Mitigation: Install only in an isolated VM or container and bind access to localhost behind SSH tunneling or firewall rules. <br>
Risk: Exported cookies and page data can contain sensitive authentication or personal information. <br>
Mitigation: Use dedicated browser profiles and task-specific accounts, treat exported cookies like passwords, and delete profiles and output artifacts promptly. <br>
Risk: Setup and runtime helpers may propose package installation or service changes. <br>
Mitigation: Review any auto-install command before allowing it and keep privileged service deployment behind explicit operator approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/waylonsong/headful-browser-vnc) <br>
- [README](artifact/README.md) <br>
- [Docker Usage](artifact/README.docker.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and generated browser artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce cookies, screenshots, rendered HTML, logs, and local runtime configuration files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
