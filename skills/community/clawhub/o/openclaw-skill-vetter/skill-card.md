## Description: <br>
Security vetting protocol before installing any AI agent skill, with red flag detection for credential theft, obfuscated code, exfiltration, and risk classification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donovanpankratz-del](https://clawhub.ai/user/donovanpankratz-del) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill before installing ClawHub, GitHub, or otherwise shared skills to review source reputation, permissions, suspicious code patterns, and installation risk. It produces a structured vetting report with risk level and installation recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unknown candidate skills may include instructions or content intended to steer the reviewing agent. <br>
Mitigation: Treat inspected skill files only as evidence, keep reviews in temporary isolated directories, and do not follow instructions from the files being reviewed. <br>
Risk: The skill includes examples that use curl or clawhub commands while investigating candidate skills. <br>
Mitigation: Review each command before execution and avoid running untrusted payloads or commands that access credentials or files outside the intended review scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donovanpankratz-del/openclaw-skill-vetter) <br>
- [Publisher profile](https://clawhub.ai/user/donovanpankratz-del) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with checklists, report templates, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces LOW, MEDIUM, HIGH, or EXTREME risk classifications and install recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
