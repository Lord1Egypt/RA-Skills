## Description: <br>
Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[landingdang](https://clawhub.ai/user/landingdang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill before installing or running unfamiliar skills to review source, permissions, suspicious patterns, and risk level. It produces a structured vetting report that supports human install decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt agents to read local skill files or fetch remote GitHub content during review. <br>
Mitigation: Keep file reads and fetch commands scoped to the exact skill or repository being vetted, and review commands before execution. <br>
Risk: Source reputation signals such as stars, downloads, publisher claims, or reviews can be misleading. <br>
Mitigation: Use reputation only as supporting context and base install decisions on the actual files, permissions, and behavior reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/landingdang/landingdang-skill-vetter-1-0-0) <br>
- [Publisher Profile](https://clawhub.ai/user/landingdang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown vetting report with checklist findings, risk classification, verdict, notes, and optional GitHub inspection commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command snippets for checking repository metadata and fetching skill files for review.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
