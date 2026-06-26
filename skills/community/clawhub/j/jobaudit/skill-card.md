## Description: <br>
Audit your OpenClaw cron job history and estimate how much you've spent on AI agents this week. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avale-slai](https://clawhub.ai/user/avale-slai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Jobaudit to review recent cron job costs, identify expensive jobs, and compare current spend against cheaper model configurations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is incomplete because package.json references a jobaudit executable that is not included in the artifact. <br>
Mitigation: Ask the publisher to include the missing executable source before installing or relying on the skill. <br>
Risk: The installer makes persistent local changes and sends an install analytics request without clear user control. <br>
Mitigation: Review install.sh before use and require telemetry plus shell-profile edits to be explicit, optional, and reversible. <br>
Risk: The artifact does not document exactly what OpenClaw job-history data is read or sent to Signalloom. <br>
Mitigation: Require data-handling documentation before providing a Signalloom API key or running audits on sensitive job history. <br>


## Reference(s): <br>
- [Jobaudit ClawHub listing](https://clawhub.ai/avale-slai/jobaudit) <br>
- [Signalloom signup](https://signalloomai.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown cost audit and optimization report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports total jobs and cost, cheapest model configuration, potential savings, and the most expensive jobs for the selected period.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence; artifact package.json lists 1.0.1 and install.sh lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
