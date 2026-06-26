## Description: <br>
Kairoa CLI is a developer toolbox skill that guides agents to use the kairoa command-line utility for encoding and decoding, hashing and HMAC, UUID and ULID generation, data conversion, JSON and SQL handling, network checks, password tools, mock data, OTP, QR codes, regex testing, image and PDF utilities, coordinate conversion, and AI chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luduoxin](https://clawhub.ai/user/luduoxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to select and run Kairoa CLI commands for common development utilities, including data formatting, hashing, network diagnostics, credential-safe AI chat setup, and generated shell command workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if real secrets are passed directly with command-line flags. <br>
Mitigation: Prefer environment variables, a secret store, or a secure prompt for API keys, and avoid copying examples that place real keys after -k or --api-key. <br>
Risk: Network commands such as HTTP, DNS, IP lookup, port scanning, TLS checks, WebSocket, and traceroute can contact external systems. <br>
Mitigation: Confirm the target is authorized before running network operations. <br>
Risk: Remote installation scripts can execute unreviewed code on the host. <br>
Mitigation: Review installation scripts before execution and prefer package-manager installs, release binaries, or source builds when higher assurance is required. <br>


## Reference(s): <br>
- [Kairoa CLI ClawHub page](https://clawhub.ai/luduoxin/kairoa-cli) <br>
- [Kairoa CLI project repository](https://github.com/covoyage/kairoa-cli) <br>
- [Kairoa CLI releases](https://github.com/covoyage/kairoa-cli/releases/latest) <br>
- [Covoyage Scoop bucket](https://github.com/covoyage/scoop-bucket) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Code, Files, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or guide creation of local files such as QR images, mock data JSON, resized images, PDF metadata output, and encrypted vault data depending on the selected Kairoa command.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
