## Description: <br>
Performs MCP server and skill security audits that scan local project files for vulnerability, malware, and compliance patterns, then report findings with remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to inspect MCP server or skill directories for suspicious code patterns, hardcoded credentials, broad network bindings, and logging practices that may expose sensitive data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit reads files in the user-selected target directory and may inspect configuration or .env-style files that contain sensitive credentials. <br>
Mitigation: Run it only against specific project folders that need review, avoid broad personal directories, and treat generated findings as sensitive until reviewed. <br>
Risk: Pattern-based security findings can be incomplete or require human judgment before remediation. <br>
Mitigation: Review findings before acting on them and use this tool alongside established security review or CI checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-mcp-security-audit) <br>
- [Publisher profile](https://clawhub.ai/user/534422530) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [CLI text report or JSON audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes score, grade, severity summary, finding locations, and remediation recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
