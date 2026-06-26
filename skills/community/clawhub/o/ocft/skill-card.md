## Description: <br>
P2P file transfer between AI agents via message channels, with chunked transfer, IPFS fallback for large files, and trusted peer management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stormixus](https://clawhub.ai/user/stormixus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to transfer files between trusted AI agents over text-based channels such as chat systems. It supports chunked transfer, integrity checks, resumable transfers, peer trust management, and optional IPFS fallback for large files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Peer secrets and exported connection details can authorize trusted transfers if exposed. <br>
Mitigation: Keep node and peer secrets private, verify peers before trusting them, and prefer short trust TTLs. <br>
Risk: Auto-accept mode can receive files without manual review from configured trusted peers. <br>
Mitigation: Use auto-accept only for peers you intend to trust, review trust entries regularly, and expire or remove peers that no longer need access. <br>
Risk: IPFS fallback and public chat channels can expose files beyond the intended recipient. <br>
Mitigation: Avoid IPFS and public channels for sensitive files unless that exposure model is intentional. <br>
Risk: Downloads and large transfers can write unwanted files or exceed expected storage limits. <br>
Mitigation: Choose a contained download directory and configure an appropriate maximum file size before use. <br>


## Reference(s): <br>
- [OCFT ClawHub page](https://clawhub.ai/stormixus/ocft) <br>
- [OCFT GitHub project](https://github.com/stormixus/ocft) <br>
- [OCFT npm package](https://www.npmjs.com/package/ocft) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with bash, TypeScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI setup, peer-management commands, transfer configuration, and programmatic usage examples.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
