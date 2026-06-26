## Description: <br>
Security scanner for ClawdHub skills - detects suspicious patterns, manages whitelists, and monitors Moltbook for security threats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[digitaladaption](https://clawhub.ai/user/digitaladaption) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security reviewers use this skill to scan ClawdHub skill files for suspicious patterns, manage whitelists, monitor security discussions, and produce scan reports before installation or deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional shell hooks can intercept future skill install commands and change the normal install flow. <br>
Mitigation: Review the hook scripts and paths, keep a backup of your shell profile, and enable the hook only when you want this skill to mediate future installs. <br>
Risk: Scheduled scans and scanner decisions can be incomplete, noisy, or overly broad. <br>
Mitigation: Treat scan results as advisory and manually review anything the skill blocks or whitelists before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/digitaladaption/openclaw-skills-security-checker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference markdown and JSON scan reports when the underlying scanner is run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
