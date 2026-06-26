## Description: <br>
Watches your desktop activity, maintains a real-time task stack, detects forgotten tasks after interruptions, and gently reminds you. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HuilingP](https://clawhub.ai/user/HuilingP) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Knowledge workers and productivity-focused agent users use Intent Guardian to monitor local desktop activity, maintain a task stack, and receive reminders when interruptions cause suspended work to be forgotten. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Continuous desktop activity monitoring can capture sensitive app names, window titles, URLs, document titles, and task context in local memory files. <br>
Mitigation: Enable the skill only with informed consent, store data in a restricted local directory, review captured fields, and run cleanup on a defined retention schedule. <br>
Risk: Optional screenshot capture can expose sensitive screen content and may involve a vision model if configured. <br>
Mitigation: Keep screenshot capture disabled unless explicitly needed, avoid cloud vision models on sensitive screens, and verify that raw screenshots are deleted immediately after analysis. <br>
Risk: Security evidence says privacy controls such as working hours and excluded apps are incomplete or not enforced. <br>
Mitigation: Verify or add enforcement for working-hours and excluded-app filtering before relying on those controls. <br>
Risk: ActivityWatch integration can import detailed local desktop activity from a local service. <br>
Mitigation: Use ActivityWatch only when richer activity tracking is needed, keep the service local, and review its captured buckets and retention settings. <br>


## Reference(s): <br>
- [Intent Guardian ClawHub Listing](https://clawhub.ai/HuilingP/intent-guardian) <br>
- [Project Homepage](https://github.com/HuilingP/intent-guardian) <br>
- [Forgetting Detection - Algorithm Reference](references/forgetting-detection.md) <br>
- [Intent Guardian - Heartbeat Integration Guide](references/heartbeat-integration.md) <br>
- [ActivityWatch](https://activitywatch.net/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or JSONL local data outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes local activity logs, task stacks, focus profiles, reminder feedback, and daily focus summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence, artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
