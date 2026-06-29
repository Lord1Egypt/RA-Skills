## Description: <br>
Audits project CLAUDE.md files as runtime configuration, returning a scorecard, prioritized fixes, and optional user-approved edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huiyonghkw](https://clawhub.ai/user/huiyonghkw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to audit CLAUDE.md guidance for bloat, vague rules, missing safeguards, broken documentation pointers, and hardcoded secrets, then prioritize edits that keep agent context leaner and safer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved fixes can change project guidance files and influence future agent sessions. <br>
Mitigation: Review each proposed change before applying it, especially Hook and MEMORY.md additions. <br>
Risk: Project CLAUDE.md files may contain sensitive instructions or hardcoded credentials that should not be kept in agent context. <br>
Mitigation: Keep secrets out of CLAUDE.md and rotate any discovered credential as part of remediation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huiyonghkw/hekouwang-claude-md-doctor-skill) <br>
- [README.en.md](artifact/README.en.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with optional JSON checker output, shell commands, and proposed file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [File edits require user approval; the command-line checker can emit JSON for CI.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
