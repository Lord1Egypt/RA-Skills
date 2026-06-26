## Description: <br>
Scans a local network for active devices and open ports and returns a formatted Markdown table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Doooxu](https://clawhub.ai/user/Doooxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network administrators and technical users use this skill to inventory devices and exposed common ports on networks they own or administer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can actively probe a fixed private subnet and extra targets, which may scan hosts outside the user's intended scope. <br>
Mitigation: Run it only on networks you own or administer, confirm the target range before execution, and set SCAN_EXTRA_IPS only for hosts you intend to scan. <br>
Risk: The documented Windows PowerShell command references a scan.ps1 file that is not supplied in the artifact. <br>
Mitigation: Use the bundled Python scanner on supported systems, or provide and review a PowerShell script before running the Windows command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Doooxu/network-device-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown table with device IP addresses, MAC addresses, open ports, and inferred device types.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local discovery and port checks before summarizing results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
