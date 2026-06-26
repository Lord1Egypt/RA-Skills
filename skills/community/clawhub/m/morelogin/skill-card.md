## Description: <br>
Manage MoreLogin anti-detect browser profiles and cloud phones through the official localhost Local API, including profile lifecycle, fingerprint refresh, cloud phone power and app operations, and proxy, group, and tag management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MoreLoginBrowser](https://clawhub.ai/user/MoreLoginBrowser) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use this skill to control local MoreLogin browser profiles and cloud phones through documented API endpoints while building profile lifecycle, CDP, ADB, proxy, group, and tag workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over real MoreLogin profiles and cloud phones. <br>
Mitigation: Install only when that control is intended, keep the API target on localhost, and confirm sensitive actions before execution. <br>
Risk: Destructive operations can clear caches, delete profiles, uninstall apps, change proxies, or alter device state. <br>
Mitigation: Require explicit confirmation of target IDs, endpoint names, and request bodies before running destructive or state-changing commands. <br>
Risk: Automation can expose account data, cookies, screenshots, proxy credentials, ADB keys, or scraping outputs. <br>
Mitigation: Avoid logging secrets or captured data, review cookie, screenshot, scraping, and anti-detection workflows, and approve only exact endpoints and payloads. <br>


## Reference(s): <br>
- [MoreLogin Local API Documentation](https://guide.morelogin.com/api-reference/local-api) <br>
- [MoreLogin ClawHub Skill Page](https://clawhub.ai/MoreLoginBrowser/morelogin) <br>
- [API-CONTRACT.md](artifact/API-CONTRACT.md) <br>
- [local-api.yaml](artifact/local-api.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce localhost API payloads and CLI commands for MoreLogin browser profile, cloud phone, proxy, group, and tag operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
