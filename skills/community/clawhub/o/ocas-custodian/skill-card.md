## Description: <br>
Custodian monitors OpenClaw gateway logs, cron jobs, skill journals, and OCAS data directories, applies safe non-destructive fixes during quiet hours, initializes skills, registers missing background tasks, and escalates unresolved issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use Custodian to check system health, investigate log and cron failures, initialize skills, register missing background tasks, and run overnight maintenance. It is intended for operational maintenance workflows where unresolved issues should be surfaced with diagnostics or repair plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent system changes, including creating files, registering scheduled jobs, and updating itself from GitHub. <br>
Mitigation: Review the source before installation, disable automatic updates or cron registration until trusted, and confirm rollback steps for any enabled maintenance action. <br>
Risk: Autonomous repair actions can change operational state even when they are intended to be non-destructive. <br>
Mitigation: Use the documented safety envelope, review issue and fix records after scans, and require manual approval for Tier 2 through Tier 4 repairs. <br>
Risk: Server-resolved import provenance is unavailable for this release. <br>
Mitigation: Verify the publisher handle, package hashes, and install source before deploying the skill in a sensitive environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/indigokarasu/ocas-custodian) <br>
- [Publisher profile](https://clawhub.ai/user/indigokarasu) <br>
- [Known issue registry](references/known_issues.json) <br>
- [Custodian repair plan](references/plans/custodian-repair.plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command names, configuration details, issue summaries, status output, and repair-plan descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce maintenance actions and follow-up verification guidance for OpenClaw health, cron, journal, and data-directory issues.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
