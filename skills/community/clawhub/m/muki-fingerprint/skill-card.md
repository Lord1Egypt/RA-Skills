## Description: <br>
MUKI is an asset fingerprinting skill for authorized red-team reconnaissance, asset discovery, service fingerprinting, vulnerability scanning, attack surface mapping, sensitive path detection, and sensitive information extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Admin4Giter](https://clawhub.ai/user/Admin4Giter) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Security teams and authorized external assessors use this skill to run MUKI-based asset discovery, service fingerprinting, sensitive path checks, and findings review during scoped penetration tests or asset assessments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide active scans against arbitrary targets. <br>
Mitigation: Use it only for authorized penetration testing or asset assessment with written scope, target lists, time windows, and rate limits. <br>
Risk: Active probing and directory checks may create unwanted traffic or access sensitive endpoints. <br>
Mitigation: Disable active or directory modules unless they are explicitly approved for the engagement. <br>
Risk: Reports may contain credentials, PII, financial data, internal IPs, or other sensitive findings. <br>
Mitigation: Secure generated reports, restrict access to authorized personnel, define retention rules, and delete data when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Admin4Giter/muki-fingerprint) <br>
- [SKILL.md](SKILL.md) <br>
- [Quick reference](references/quick-reference.md) <br>
- [Sensitive extraction rules](references/Rules.yml) <br>
- [Active fingerprint rules](references/active_finger.json) <br>
- [Passive fingerprint database](references/finger.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and references to JSON or Excel scan outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated commands and guidance may lead to reports containing service fingerprints, sensitive paths, and extracted sensitive information.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
