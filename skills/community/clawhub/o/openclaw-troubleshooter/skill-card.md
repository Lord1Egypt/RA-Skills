## Description: <br>
OpenClaw Troubleshooter helps diagnose and propose repairs for common OpenClaw Gateway, configuration, port conflict, and risky-skill issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[345968504](https://clawhub.ai/user/345968504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to troubleshoot OpenClaw installations, review diagnostic findings, and receive guided repair commands for Gateway, configuration, and skill security issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repair guidance can force-stop processes, overwrite OpenClaw configuration, or uninstall named skills. <br>
Mitigation: Run check-only diagnostics first, review each proposed repair, back up openclaw.json, and allow forced process kills or --yes uninstalls only when explicitly intended. <br>
Risk: Security claims about other installed skills may be stale or environment-specific. <br>
Mitigation: Verify any dangerous-skill finding with a current scan before uninstalling or changing the skill. <br>


## Reference(s): <br>
- [Openclaw Troubleshooter on ClawHub](https://clawhub.ai/345968504/openclaw-troubleshooter) <br>
- [Publisher profile: 345968504](https://clawhub.ai/user/345968504) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with PowerShell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prioritized diagnostic findings and proposed repair steps for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact metadata, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
