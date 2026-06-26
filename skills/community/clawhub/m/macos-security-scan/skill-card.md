## Description: <br>
Scans a macOS computer for signs of tampering, malware, keyloggers, and suspicious activity, especially after repair or third-party handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentyao](https://clawhub.ai/user/vincentyao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support technicians use this skill to run a read-only macOS security scan after repair, third-party handling, or suspected compromise. It helps review suspicious processes, startup items, privacy permissions, network connections, browser extensions, and macOS security settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local report can include system inventory, privacy permission, process, and network details. <br>
Mitigation: Save and share the report deliberately, and treat it as potentially sensitive system information. <br>
Risk: Running with sudo can reveal more private system permission and network details than a standard-user scan. <br>
Mitigation: Run without sudo first, and use sudo only after the user explicitly agrees and understands the added visibility. <br>
Risk: A clean first-pass scan does not guarantee the Mac is free of all malware or tampering. <br>
Mitigation: Use the report as an initial check and escalate suspicious findings to Apple Support, a security professional, or dedicated antivirus tooling. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report saved as a local file plus a plain-language chat summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script writes a local security_report.md file and can optionally run selected checks with sudo when the user agrees.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
