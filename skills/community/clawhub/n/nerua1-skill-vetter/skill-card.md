## Description: <br>
Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerua1](https://clawhub.ai/user/nerua1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill before installing or running third-party skills to review source trust, permission scope, suspicious patterns, and install risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a checklist aid, so relying on it as the only security decision could miss issues. <br>
Mitigation: Verify the publisher and source, review the skill files, and use scanner results or human approval before installing skills. <br>
Risk: The quick vet examples use curl to inspect GitHub repositories when intentionally run. <br>
Mitigation: Run the commands only for repositories the user explicitly wants inspected, and review the destination URLs before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nerua1/nerua1-skill-vetter) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown report with checklist items, risk classification, verdict, notes, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review guidance only; it does not execute checks by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
