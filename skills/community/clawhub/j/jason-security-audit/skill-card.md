## Description: <br>
Security audit for external resources (GitHub repos, downloaded skills, files). Detects malicious code, suspicious executables, and content mismatches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ITHACAJASON](https://clawhub.ai/user/ITHACAJASON) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security-minded users use this skill to inspect local copies of external repositories, downloaded skills, and scripts before trusting or executing them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit recursively reads the chosen folder and reports file paths, which can expose sensitive local structure if run on broad private directories. <br>
Mitigation: Run it only on the specific repository, skill, or folder being evaluated, and review reports before sharing them. <br>
Risk: The scan is heuristic and static, so a clean result does not guarantee that external code is safe to execute. <br>
Mitigation: Treat results as triage guidance, then manually review code and use isolated environments before running untrusted software. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ITHACAJASON/jason-security-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style terminal report with risk level, findings, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a text report file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
