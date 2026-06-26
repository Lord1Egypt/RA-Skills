## Description: <br>
Connect OpenClaw to the AntSeed P2P AI network as a buyer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kotevcode](https://clawhub.ai/user/kotevcode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure OpenClaw to route model requests through a local AntSeed buyer proxy connected to a P2P provider network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw model traffic may be routed through third-party AntSeed providers. <br>
Mitigation: Install only when this routing is intended, and avoid sending secrets, private code, or sensitive prompts unless the selected providers and their data handling are trusted. <br>
Risk: The setup flow can modify the user's OpenClaw configuration. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before running setup or applying the documented configuration changes. <br>
Risk: The optional service mode creates a boot-persistent buyer proxy. <br>
Mitigation: Use the service option only when a persistent local proxy is desired and review the systemd unit before enabling it. <br>
Risk: Untrusted setup arguments could affect generated shell, JSON, or service configuration. <br>
Mitigation: Use trusted values for model, port, bootstrap node, context window, and max token arguments. <br>


## Reference(s): <br>
- [OpenClaw AntSeed ClawHub release](https://clawhub.ai/kotevcode/openclaw-antseed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npm and openclaw; the setup script accepts model, port, bootstrap node, context window, max tokens, and service options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
