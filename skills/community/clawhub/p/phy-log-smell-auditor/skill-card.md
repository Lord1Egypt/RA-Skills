## Description: <br>
Scans source files for logging anti-patterns such as debug output in production paths, log-level mismatches, PII exposure, missing request or trace context, and noisy debug loops across JavaScript/TypeScript, Python, Go, Java, and Ruby. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to audit application code for unsafe, noisy, or low-quality logging before release or CI enforcement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated fix commands can make real code changes, including removing logs that may be needed for production debugging, auditing, or compliance. <br>
Mitigation: Run preview commands first, work in version control, inspect the diff, and avoid bulk log removal in production or audit-sensitive code without manual review. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill listing](https://clawhub.ai/PHY041/phy-log-smell-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown audit report with file and line citations, remediation guidance, and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local static analysis; no external API is required.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
