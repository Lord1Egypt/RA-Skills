## Description: <br>
Professional security audit for AI agents. Checks URLs for SSRF, analyzes content for prompt injection, validates commands for shell injection, integrates with skill-scanner for deep analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danilka88](https://clawhub.ai/user/danilka88) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to review URLs, external content, shell commands, and agent skill files for security issues such as SSRF, prompt injection, credential exposure, malicious JavaScript, and risky command patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports broad automatic self-audits of local history and sensitive directories without clear user control. <br>
Mitigation: Review before installing, use only with clear target paths, and require explicit confirmation before history, environment, ~/.ssh, or ~/.hermes checks. <br>
Risk: The full scan path can install or rely on external tooling and a local LM Studio endpoint. <br>
Mitigation: Avoid the --install full-scan path unless the PyPI dependency and local LM Studio endpoint are trusted. <br>
Risk: Audit memory could retain sensitive security details. <br>
Mitigation: Configure audit memory to redact sensitive details and expire records when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danilka88/ka88-agent-shield) <br>
- [Publisher profile](https://clawhub.ai/user/danilka88) <br>
- [Project homepage from metadata](https://github.com/Danilka88/ka88-agent-shield) <br>
- [Support URL from metadata](https://github.com/Danilka88/ka88-agent-shield/issues) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [Pre-Visit Scan procedure](artifact/procedures/01-pre-visit.md) <br>
- [Content Analysis procedure](artifact/procedures/02-content-analysis.md) <br>
- [Command Safety procedure](artifact/procedures/03-commands.md) <br>
- [Self-Audit procedure](artifact/procedures/04-self-audit.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, finding/report templates, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local pattern and SSRF blocklist configuration for scans.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill frontmatter, README, clawhub metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
