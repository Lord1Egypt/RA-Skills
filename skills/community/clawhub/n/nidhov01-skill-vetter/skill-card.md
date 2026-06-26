## Description: <br>
Security-first skill vetting for AI agents before installing skills from ClawdHub, GitHub, or other sources, with checks for red flags, permission scope, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to review third-party or unfamiliar skills before installation by checking source, permissions, suspicious patterns, and risk level. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example GitHub commands may contact remote GitHub endpoints when copied and run. <br>
Mitigation: Run those commands only against repositories you intentionally want to inspect, and review substituted OWNER, REPO, and SKILL_NAME values before execution. <br>
Risk: A checklist report can be mistaken for proof that a skill is safe. <br>
Mitigation: Treat the report as review guidance, and require human approval for high-risk findings, credential access, system changes, or unclear provenance. <br>


## Reference(s): <br>
- [ClawHub Skill Vetter listing](https://clawhub.ai/nidhov01/nidhov01-skill-vetter) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a structured vetting report with source, author, version, metrics, reviewed files, red flags, permissions, risk level, verdict, and notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
