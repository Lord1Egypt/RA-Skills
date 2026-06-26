## Description: <br>
Security scanner for OpenClaw skills that analyzes skill folders and .skill files for prompt injection, data exfiltration, malicious scripts, suspicious network connections, dangerous code patterns, and unauthorized access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[produktentdecker](https://clawhub.ai/user/produktentdecker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill before installing or auditing OpenClaw skills to scan folders or packaged .skill files and review findings about suspicious patterns, dependencies, URLs, and risk levels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted .skill archive may write outside the intended extraction folder during scanning. <br>
Mitigation: Review before installing or running on untrusted .skill files, and use a disposable workspace or sandbox until archive extraction validates every member path, rejects symlinks and special files, and enforces size and file-count limits. <br>
Risk: Static analysis can miss logic-level attacks, obfuscated behavior beyond known patterns, and behavior fetched or executed only at runtime. <br>
Mitigation: Combine scan results with manual review for high-stakes deployments and treat low-risk results as advisory rather than proof of safety. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/produktentdecker/openclaw-skill-audit) <br>
- [Skill-declared source code](https://github.com/ProduktEntdecker/skill-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON scan reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Risk findings include overall risk, finding counts, referenced URLs and APIs, required environment variables, required binaries, and file/script counts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
