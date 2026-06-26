## Description: <br>
Audit and safely repair OpenClaw configuration with deterministic validation, backups, rollback, and change reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soal2](https://clawhub.ai/user/soal2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw JSON configuration, identify startup-blocking problems, apply documented repairs only after backup, and report validation results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect and propose repairs for local OpenClaw configuration. <br>
Mitigation: Install only when that local configuration access is intended, and review proposed edits before applying them. <br>
Risk: Incorrect configuration edits can prevent OpenClaw from starting. <br>
Mitigation: Create a backup before any write, apply only documented startup-blocking repairs, and require successful post-change validation before trusting the repair. <br>
Risk: A failed repair could leave the configuration in an invalid state. <br>
Mitigation: Roll back immediately from the generated backup if post-change validation fails, and report the backup path and validation result. <br>


## Reference(s): <br>
- [Official source list](references/official-sources.md) <br>
- [OpenClaw gateway configuration](https://docs.openclaw.ai/gateway/configuration) <br>
- [OpenClaw configuration reference](https://docs.openclaw.ai/gateway/configuration-reference) <br>
- [OpenClaw CLI config](https://docs.openclaw.ai/cli/config) <br>
- [OpenClaw CLI doctor](https://docs.openclaw.ai/cli/doctor) <br>
- [ClawHub skill page](https://clawhub.ai/soal2/openclaw-config-guard) <br>
- [Publisher GitHub profile](https://github.com/soal2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with command guidance and JSON validation details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include official sources consulted, active config path, backup path, modified config paths, validation results, rollback status, and restart guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
