## Description: <br>
Lobster Says is a server-backed OpenClaw companion skill that schedules supportive IM messages and can optionally read local conversation transcripts in user-selected memory modes to generate summaries for nixiashuo.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredwei01](https://clawhub.ai/user/jaredwei01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to create and operate a personal emotional companion that sends scheduled messages to IM channels, manages configurable memory modes, and returns short-lived studio or screenshot links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run recurring background jobs through OpenClaw cron. <br>
Mitigation: Review and pause OpenClaw cron jobs after setup if the scheduled companion messages or digest jobs are not desired. <br>
Risk: The skill may read and upload private chat transcript data in smart or deep memory modes. <br>
Mitigation: Use lightweight mode for maximum privacy, and avoid deep mode unless raw transcript upload to nixiashuo.com is acceptable. <br>
Risk: The skill stores bearer tokens locally in .lobster-config. <br>
Mitigation: Keep .lobster-config private and avoid sharing logs or command output that could expose access tokens. <br>
Risk: IM delivery behavior, especially WeCom delivery, can target the wrong destination if channel metadata is not verified. <br>
Mitigation: Verify the IM target before enabling pushes and re-check pending activation states before registering recurring delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaredwei01/lobster-says) <br>
- [nixiashuo.com service dependency](https://nixiashuo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands and script-produced JSON status when initialization or delivery tasks run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .lobster-config, OpenClaw cron jobs, IM delivery targets, and short-lived studio links through bundled scripts.] <br>

## Skill Version(s): <br>
2.5.8 (source: server release metadata and artifact/openclaw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
