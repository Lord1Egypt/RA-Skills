## Description: <br>
Manages a mihomo (Clash Meta) proxy service on Linux servers by helping configure, update, restart, switch proxy nodes, update subscriptions, and troubleshoot connectivity for existing mihomo installations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lflyice](https://clawhub.ai/user/lflyice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and server operators use this skill to manage an existing mihomo proxy deployment, including validating configuration, restarting the systemd service, inspecting proxy groups, switching nodes, and generating configuration from subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The update helper can turn a subscription URL into shell execution. <br>
Mitigation: Only use trusted subscription URLs and replace the shell-based downloader with argument-array execution or a native HTTP client with strict URL and content validation before installation. <br>
Risk: The configuration generator writes directly to the live mihomo config path without built-in backup safeguards. <br>
Mitigation: Back up the existing mihomo configuration before updates, validate generated configuration with mihomo's test mode, and restart the service only after validation succeeds. <br>


## Reference(s): <br>
- [Mihomo Proxy Manager on ClawHub](https://clawhub.ai/lflyice/mihomo-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce command sequences for systemd, curl-based local API calls, and mihomo configuration generation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
