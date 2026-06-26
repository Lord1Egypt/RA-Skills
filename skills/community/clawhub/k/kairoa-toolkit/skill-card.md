## Description: <br>
Launches the Kairoa desktop app and provides deep-link, command, and helper-script guidance for developer tools including encoding, formatting, cryptography, QR codes, mock data, and network diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luduoxin](https://clawhub.ai/user/luduoxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to open Kairoa and route common utility tasks into its desktop tools through app launch commands, deep links, and short helper scripts. It is most useful for formatting data, encoding or decoding text, generating identifiers or QR codes, checking hashes, and running authorized network diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deep-link URLs can expose secrets through command history, logs, browser handlers, or screenshots if passwords, API keys, private keys, seed phrases, or tokens are embedded in kairoa:// parameters. <br>
Mitigation: Do not place sensitive values in kairoa:// URLs; enter secrets only through trusted secure app flows after verifying the installed Kairoa app. <br>
Risk: Network tools such as port scanning, traceroute, TLS checks, DNS lookup, WebSocket testing, and API requests may affect systems outside the user's authorization. <br>
Mitigation: Use network diagnostics only on systems the user owns or is explicitly authorized to test. <br>
Risk: The skill launches a local desktop application and assumes a trusted Kairoa installation is present. <br>
Mitigation: Install Kairoa only from a trusted source and confirm the app path before launching or following helper commands. <br>


## Reference(s): <br>
- [Kairoa Toolkit on ClawHub](https://clawhub.ai/luduoxin/kairoa-toolkit) <br>
- [Skill source description](artifact/SKILL.md) <br>
- [Artifact manifest](artifact/clawhub.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, markdown] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes macOS app launch commands, kairoa:// deep-link examples, and optional Python helper scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
