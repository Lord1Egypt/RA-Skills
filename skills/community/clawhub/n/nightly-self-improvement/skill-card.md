## Description: <br>
Nightly Build helps an agent scan recent sessions for friction points, choose one small reversible improvement, implement it, and leave a morning briefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeytbuilds](https://clawhub.ai/user/joeytbuilds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to schedule an agent that reviews recent sessions and memory for workflow friction, performs one low-risk reversible improvement, and reports what changed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A recurring unattended agent can read session history and memory and make local changes without per-action approval. <br>
Mitigation: Limit allowed directories, exclude sensitive sessions or projects, require approval for memory edits and scripts, and document how to disable the cron job. <br>
Risk: Morning briefings and saved summaries can expose secrets or personal data from prior sessions. <br>
Mitigation: Redact secrets and personal data before writing briefings, and save briefings to a local file by default. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a recurring 3:00 AM cron setup and a tiered autonomy policy for what the agent may change.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
