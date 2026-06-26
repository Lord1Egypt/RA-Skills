## Description: <br>
Migrate a user's OpenClaw customization footprint into Hermes Agent, including compatible memories, SOUL.md, command allowlists, user skills, selected workspace assets, and a report of items that could not be migrated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AgungPrabowo123](https://clawhub.ai/user/AgungPrabowo123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Hermes Agent users use this skill to plan and run an OpenClaw-to-Hermes migration with dry-run previews, conflict choices, and post-run reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The migration helper can move API keys or tokens when secret-related options are enabled or when compatible configuration categories are included. <br>
Mitigation: Run a dry run first, use user-data mode unless secret migration is intentional, and inspect any imported .env or configuration changes before keeping them. <br>
Risk: The migration can change personal Hermes state, including SOUL.md, memories, command allowlists, imported skills, workspace instructions, and selected workspace assets. <br>
Mitigation: Back up ~/.hermes, resolve conflicts explicitly, and review report.json, summary.md, imported skills, command allowlists, memories, SOUL.md, workspace instructions, and .env changes after execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AgungPrabowo123/openclaw-migration-2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured migration-report summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local file migration, configuration updates, dry-run inspection, conflict handling, and review of generated reports.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
