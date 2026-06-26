## Description: <br>
Scans codebases for unsafe deserialization patterns across Python, Java, PHP, Ruby, Node.js/TypeScript, and Go, then reports severity, CWE/CVE mappings, taint context, and fix guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit source code for OWASP A08 insecure deserialization risks and receive prioritized remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the project directory selected for scanning. <br>
Mitigation: Run it only against repositories and paths the agent is permitted to inspect. <br>
Risk: The embedded Python scanner may fail at startup if copied exactly. <br>
Mitigation: Fix or verify the scanner before relying on its findings. <br>


## Reference(s): <br>
- [OWASP A08:2021 - Software and Data Integrity Failures](https://owasp.org/A08_2021-Software_and_Data_Integrity_Failures/) <br>
- [Canlah AI](https://canlah.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/PHY041/phy-deserialization-audit) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with embedded Python scanner code and optional text or JSON scan reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports CRITICAL, HIGH, and MEDIUM findings with CWE/CVE mappings, taint context, and per-language fix snippets.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
