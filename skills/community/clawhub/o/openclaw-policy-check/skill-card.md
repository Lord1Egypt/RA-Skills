## Description: <br>
Scan repositories for risky security patterns before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spbavarva](https://clawhub.ai/user/spbavarva) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run a local preflight scan on repositories or files before execution, then review risky commands, secret-like patterns, and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan findings can include snippets from lines that look like secrets. <br>
Mitigation: Treat scanner output as sensitive and avoid sharing raw findings outside the trusted review context. <br>
Risk: Broad scans can expose more local repository content than needed for the requested review. <br>
Mitigation: Run the scanner against specific repositories or files instead of broad home-directory paths. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown summary with optional JSON scanner output and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports total findings, severity breakdown, top findings with file and line, and brief remediation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
