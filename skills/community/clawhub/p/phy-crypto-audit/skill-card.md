## Description: <br>
Detects weak cryptography patterns in Python, JavaScript/TypeScript, Go, Java, and PHP source code and provides local audit output with CI fail-gate commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to create and run a local weak-cryptography audit helper against source code before merging or releasing changes. It is suited for finding common OWASP A02 cryptographic failures and surfacing remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports may expose sensitive source paths or code lines from the scanned project. <br>
Mitigation: Scan only intended local source paths and avoid sharing generated reports publicly. <br>
Risk: Running a helper script that differs from the code shown in the skill could produce unexpected behavior. <br>
Mitigation: Confirm the local crypto_audit.py script was created from the skill-provided code before execution. <br>
Risk: Static pattern matching can miss issues or produce false positives in context-heavy cryptographic code. <br>
Mitigation: Review findings manually and use them as triage input alongside normal security review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-crypto-audit) <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [PHY041 ClawHub profile](https://clawhub.ai/user/PHY041) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command snippets; generated audit reports are plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local static-analysis helper; CI mode can exit nonzero when critical or high findings are present.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
