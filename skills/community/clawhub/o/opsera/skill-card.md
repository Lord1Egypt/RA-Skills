## Description: <br>
Use the bundled Opsera executable as the Xshell replacement for VPN-launched sessions so an agent can run commands or upload and download files through a current VPN-created .xsh local SSH tunnel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tao-vin](https://clawhub.ai/user/tao-vin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage SSH command execution and file transfer through VPN-launched Xshell .xsh tunnels with the bundled Opsera executable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run remote SSH commands and transfer files on servers reachable through configured VPN and Xshell sessions. <br>
Mitigation: Review target server inventory and SSH configuration before use, prefer least-privilege deploy users, and verify commands and upload or download paths before execution. <br>
Risk: Wildcard, batch, root, or production commands may affect more systems or data than intended. <br>
Mitigation: Use explicit targets and paths, avoid broad production commands unless deliberately authorized, and confirm user intent before high-impact operations. <br>


## Reference(s): <br>
- [ClawHub Opsera Skill Page](https://clawhub.ai/tao-vin/opsera) <br>
- [Opsera GitHub Repository](https://github.com/tao-vin/opsera) <br>
- [Opsera Releases](https://github.com/tao-vin/opsera/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the bundled opsera.exe executable for GUI or CLI workflows over existing .xsh tunnel files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
