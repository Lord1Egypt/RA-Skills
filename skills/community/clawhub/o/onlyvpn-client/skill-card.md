## Description: <br>
Operates the OnlyVPN desktop client through vpn-cli.exe on Windows or vpn-cli on macOS for status, subscription management, node selection, connection control, help, and version commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlynet-dev](https://clawhub.ai/user/onlynet-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to automate or document OnlyVPN CLI workflows on Windows and macOS, including subscriptions, node selection, status checks, and connect or disconnect actions after the native client is running. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using this skill may require installing and running the OnlyVPN native desktop client. <br>
Mitigation: Install OnlyVPN only when intentionally using that vendor, verify the installer comes from the official site, and review operating-system prompts before allowing the client to run. <br>
Risk: VPN connect and disconnect commands can change the machine's network routing and traffic path. <br>
Mitigation: Confirm the intended VPN action before running connect or disconnect commands, and check status output after execution to verify the active connection state. <br>


## Reference(s): <br>
- [OnlyVPN CLI reference](artifact/reference.md) <br>
- [OnlyVPN homepage](https://onlyvpn.net) <br>
- [ClawHub skill page](https://clawhub.ai/onlynet-dev/onlyvpn-client) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require the OnlyVPN native client to be running first and return JSON stdout containing code, message, data, and error fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
