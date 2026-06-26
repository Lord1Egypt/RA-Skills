## Description: <br>
Provides human-help support to AI agents via HeySummon by monitoring requests, sending notifications, and handling provider replies through the HeySummon platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomasansems](https://clawhub.ai/user/thomasansems) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External providers and operators use this skill to receive help requests from AI agents through HeySummon, get notifications in a messaging target, and send human responses back through the platform API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts a persistent watcher that uses the local OpenClaw gateway token to send notifications. <br>
Mitigation: Install only from a trusted publisher, use a dedicated notification target, and stop the watcher with the teardown script when it is not needed. <br>
Risk: Provider replies are forwarded externally without an additional confirmation step. <br>
Mitigation: Avoid sending secrets, regulated data, or unreviewed sensitive content in replies. <br>
Risk: Runtime event logs may contain sensitive request or message data. <br>
Mitigation: Monitor or delete ~/.heysummon-provider event logs according to local retention and data-handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thomasansems/heysummon-provider) <br>
- [HeySummon platform](https://heysummon.ai) <br>
- [Publisher profile](https://clawhub.ai/user/thomasansems) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command examples and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start or stop a persistent local watcher and send provider replies through configured platform credentials.] <br>

## Skill Version(s): <br>
0.1.0-beta (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
