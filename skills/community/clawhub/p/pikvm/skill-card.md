## Description: <br>
Control and inspect PiKVM devices over the PiKVM HTTP API for power, HID, screen capture, virtual media, and switch-port operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[didyouexpectthat](https://clawhub.ai/user/didyouexpectthat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support engineers use this skill to inspect and operate a user-configured PiKVM-managed machine from an agent workflow. It is suited for authenticated device status checks, remote input, power control, screenshots, OCR, virtual media, and switch-port actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-impact PiKVM operations such as power off, reset, HID typing, virtual-media changes, and switch-port changes. <br>
Mitigation: Require clear user intent for state-changing actions, restate the exact operation before execution, and re-read the relevant PiKVM state afterward. <br>
Risk: PiKVM credentials and session material are sensitive and could expose remote machine control if mishandled. <br>
Mitigation: Use environment variables for credentials, avoid command-line passwords, do not expose passwords, TOTP values, or cookies in reports, and use the least-privileged PiKVM account available. <br>
Risk: Disabling TLS verification can weaken protection for PiKVM authentication and API traffic. <br>
Mitigation: Keep SSL verification enabled when possible and approve insecure connections only for trusted local deployments. <br>


## Reference(s): <br>
- [PiKVM API Documentation](https://docs.pikvm.org/api/) <br>
- [PiKVM API reference notes](references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown summaries with shell commands, JSON API responses, and optional saved snapshot files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and PiKVM_URL, PIKVM_USER, and PIKVM_PASS; PIKVM_VERIFY_SSL and PIKVM_USE_BASIC_AUTH adjust connection behavior.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
