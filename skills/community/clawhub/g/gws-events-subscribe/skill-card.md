## Description: <br>
Google Workspace Events: Subscribe to Workspace events and stream them as NDJSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace administrators use this skill to prepare Google Workspace event subscription commands, configure targets and event types, and stream Workspace events for monitoring or automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated command can create or reuse cloud Pub/Sub resources and subscribe to Google Workspace event streams. <br>
Mitigation: Confirm execution with the user, use a least-privileged Google or GCP account, and choose narrow targets and event types. <br>
Risk: Workspace event payloads may contain sensitive operational or user data, especially when written to an output directory. <br>
Mitigation: Use a protected output directory, limit retained files, and decide whether --once, --cleanup, and --no-ack match the task. <br>
Risk: The skill depends on the gws CLI and companion gws-shared instructions for authentication and global flags. <br>
Mitigation: Verify that gws and the generated gws-shared instructions are trusted before installing or running commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-events-subscribe) <br>
- [gws-shared](../gws-shared/SKILL.md) <br>
- [gws-events](../gws-events/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Files] <br>
**Output Format:** [Markdown guidance with bash commands; the generated command streams NDJSON and can write JSON event files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and trusted gws-shared authentication instructions.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
