## Description: <br>
High-speed, memory-efficient file transfer between OpenClaw nodes using Node.js native streams and token-secured HTTP streaming without Base64 encoding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EisonMe](https://clawhub.ai/user/EisonMe) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to transfer large files between OpenClaw nodes without loading whole files into memory or encoding payloads as Base64. It provides deployment, installation-check, sender, and receiver workflows for stream-based node-to-node transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transfers can expose local files over plaintext HTTP between nodes. <br>
Mitigation: Use the skill only on trusted or VPN-protected networks, avoid sensitive files unless transport protection is in place, and confirm the exact source and destination paths before transfer. <br>
Risk: The deployment workflow generates PowerShell and uses persistent helper scripts on nodes. <br>
Mitigation: Review generated PowerShell before execution, avoid untrusted custom install directories, and remove helper scripts when they are no longer needed. <br>
Risk: Incorrect node or path selection could send or write the wrong file. <br>
Mitigation: Verify source node, destination node, input path, output path, and install directory before each transfer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EisonMe/node-transfer) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Node Transfer Latency Investigation Report](artifact/INVESTIGATION_REPORT.md) <br>
- [Contributing Proposal](artifact/CONTRIBUTING_PROPOSAL.md) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command snippets; runtime helper scripts emit JSON status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses source and destination node identifiers, file paths, install directory, generated transfer URL, one-time token, timeout, and progress/status fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
