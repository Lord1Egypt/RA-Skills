## Description: <br>
Installs and connects the WeChat channel plugin for OpenClaw so users can authorize WeChat by scanning a terminal QR code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kylinr](https://clawhub.ai/user/Kylinr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install the WeChat channel plugin, start the QR-code login flow, verify the channel status, and recover common connection issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup runs an unpinned external installer. <br>
Mitigation: Run the installer only in a trusted terminal and consider pinning or verifying the npm package version before installation. <br>
Risk: The setup links a WeChat account as an ongoing messaging channel. <br>
Mitigation: Use only the intended WeChat account, enable per-channel context isolation when using multiple accounts, and confirm how to disconnect the channel and clear stored session data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, verification, restart, multi-account, context-isolation, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
