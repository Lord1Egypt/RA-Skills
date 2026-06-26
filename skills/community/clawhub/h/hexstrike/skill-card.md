## Description: <br>
Hexstrike helps agents run and interpret cybersecurity workflows for CTF challenges, authorized penetration testing, reconnaissance, vulnerability assessment, forensics, reverse engineering, cloud security, and OSINT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaylane](https://clawhub.ai/user/jaylane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security practitioners, developers, and CTF participants use this skill to select tools, run shell-based checks, and organize findings for authorized security testing and challenge solving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad command-line scanning and credential-attack workflows that can affect systems outside an approved scope. <br>
Mitigation: Use it only for CTFs, owned lab systems, scoped bug bounty work, or professional engagements with written authorization; confirm target scope before running commands. <br>
Risk: Direct shell commands, unknown binaries, privileged installs, and long-running scans can disrupt systems or expose the operator environment. <br>
Mitigation: Review every command before execution, prefer isolated environments, avoid unattended privileged installs, and set reasonable timeouts and rate limits. <br>


## Reference(s): <br>
- [CTF Playbook](references/ctf-playbook.md) <br>
- [Recon & Pentest Methodology](references/recon-methodology.md) <br>
- [Tool Quick Reference](references/tool-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest long-running or privileged security-tool commands that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
