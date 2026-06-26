## Description: <br>
clawguard reviews OpenClaw skills and deployments for risky instructions, credential requests, privilege risks, and other security issues before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Duclawbot](https://clawhub.ai/user/Duclawbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use clawguard to review third-party OpenClaw skill directories before installation, producing severity-rated findings, evidence snippets, and remediation guidance that can be read by people or reused by agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved reports can include snippets and file paths from reviewed skills. <br>
Mitigation: Treat local reports as sensitive and clear the report store when retained snippets should not persist. <br>
Risk: Pattern-based review may miss issues outside its rules or produce findings that need interpretation. <br>
Mitigation: Use results as review guidance and manually inspect flagged skill behavior before installation. <br>


## Reference(s): <br>
- [clawguard philosophy](references/philosophy.md) <br>
- [ClawHub skill page](https://clawhub.ai/Duclawbot/opsec) <br>
- [clawdis homepage](https://clawhub.com/skills/opsec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Human-readable security report, summary text, or structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include severity, matched location, evidence snippet, impact explanation, remediation guidance, and optional reviewer notes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter and skill.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
