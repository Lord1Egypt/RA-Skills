## Description: <br>
配置OpenClaw连接远程Chrome/CDP浏览器，实现无头浏览器自动化操作与管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HappyFee](https://clawhub.ai/user/HappyFee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure OpenClaw to attach to remote Chrome/CDP browsers, including Docker-hosted headless browsers and Browserless.io, then verify and troubleshoot browser automation connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote browser control can expose privileged automation access if the CDP endpoint is reachable by untrusted users. <br>
Mitigation: Bind local CDP endpoints to localhost or protect them with SSH, VPN, or firewall controls before using the configuration. <br>
Risk: Cloud browser credentials and Browserless tokens can be exposed through shared configuration or logs. <br>
Mitigation: Treat browser service tokens as secrets and avoid sensitive logins in shared or cloud browser sessions. <br>
Risk: Using an unpinned Docker image tag can change browser behavior or security posture over time. <br>
Mitigation: Pin the browser container image to a reviewed version or digest for repeatable deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HappyFee/openclaw-browser-auto) <br>
- [HappyFee publisher profile](https://clawhub.ai/user/HappyFee) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw browser profile settings, verification commands, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
