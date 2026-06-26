## Description: <br>
Authorization gatekeeper for OpenClaw agents with scoped grants, time-bound permissions, skill scanning, prompt injection detection, and a full audit trail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juanfiguera](https://clawhub.ai/user/juanfiguera) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to gate agent actions with scoped, expiring grants, scan skills before installation, detect prompt-injection patterns, and keep an audit trail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audit and grant records may reveal sensitive agent activity. <br>
Mitigation: Keep the Jean-Claw data directory out of shared repositories and backups when needed, and rotate or delete audit files periodically. <br>
Risk: The skill influences authorization decisions for guarded or restricted agent actions. <br>
Mitigation: Review the policy and requested grants before relying on enforcement, and require explicit real-time approval for restricted actions. <br>
Risk: Bundled helper scripts read local skill and audit data and can write scan or export files. <br>
Mitigation: Review the shell scripts before running them and execute them only against intended skill or audit directories. <br>


## Reference(s): <br>
- [APOA Framework](https://agenticpoa.com) <br>
- [APOA SDK](https://github.com/agenticpoa/apoa) <br>
- [ClawHavoc Incident Background](https://snyk.io/blog/clawhub-malicious-google-skill-openclaw-malware/) <br>
- [ClawHub Skill Page](https://clawhub.ai/juanfiguera/jean-claw-van-damme) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown command responses, JSON audit/grant records, and shell script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local data records for grants, audit logs, policy state, threat logs, and scan results when activated by an agent.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
