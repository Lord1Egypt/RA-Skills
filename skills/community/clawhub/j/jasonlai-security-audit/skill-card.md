## Description: <br>
Security Audit by Jason helps agents pre-screen external repositories, downloaded skills, and files for risky file types, suspicious content patterns, and README/content mismatches before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ITHACAJASON](https://clawhub.ai/user/ITHACAJASON) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill before trusting or executing external code, downloaded skills, or local repositories. It reports risky file types, suspicious patterns, and README/content mismatches so a human can decide whether to proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Heuristic audit results can miss malicious behavior or create false confidence. <br>
Mitigation: Treat the output as a local pre-screen, not proof of safety, and manually inspect unfamiliar code even when the audit passes. <br>
Risk: Scanning broad private directories or sharing saved reports can expose local file paths or project details. <br>
Mitigation: Run the audit from the exact repo, skill, or folder being checked, avoid broad private directories, and review any saved report before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ITHACAJASON/jasonlai-security-audit) <br>
- [Publisher profile](https://clawhub.ai/user/ITHACAJASON) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text report with optional plain-text report file and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports Safe, Warning, or Critical recommendations; optional --output writes a local report file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
