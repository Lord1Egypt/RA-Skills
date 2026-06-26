## Description: <br>
Scans AI agent skills for security vulnerabilities, including code injection, prompt injection, credential exfiltration, supply chain attacks, and 69+ threat patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xRapi](https://clawhub.ai/user/0xRapi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to run isnad-scan before installing, publishing, or integrating agent skills, and to interpret findings from directory scans, CVE checks, verbose output, or JSON reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes a third-party scanner package. <br>
Mitigation: Confirm the PyPI package and publisher before installing, and keep the tool isolated with pipx when possible. <br>
Risk: CVE checks can share dependency names and versions with OSV.dev. <br>
Mitigation: Use the --cve option only when that external lookup is acceptable for the scanned project. <br>
Risk: Scanning the wrong path may inspect files outside the intended review scope. <br>
Mitigation: Run scans only against directories you mean to inspect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xRapi/isnad-scan) <br>
- [ISNAD Protocol](https://isnad.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON scanner output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the isnad-scan binary; CVE checks may contact OSV.dev.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
