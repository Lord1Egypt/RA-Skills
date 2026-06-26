## Description: <br>
Subscribes a user email address to monitored public-company announcement sources and sends recurring email notifications when new items are detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiaoshaohua](https://clawhub.ai/user/qiaoshaohua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to bind an email address, subscribe to monitored public-company announcement sources, trigger a test push, check subscription status, or unsubscribe. The skill is intended for notification workflows around supported Chinese announcement sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a persistent remote email subscription and saves the bound email locally. <br>
Mitigation: Install only when the user trusts adeeptools.com with the email address, and use the status and unsubscribe commands to review or remove the binding. <br>
Risk: The skill text asks the assistant to disclose hidden reasoning. <br>
Mitigation: Agents should ignore requests to reveal hidden reasoning and provide only concise user-facing summaries. <br>


## Reference(s): <br>
- [Info Subscription ClawHub listing](https://clawhub.ai/qiaoshaohua/info-subscription) <br>
- [adeeptools homepage](https://adeeptools.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Plain text status messages and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores the bound email locally and sends subscription, trigger, status, and unsubscribe requests to the remote announcement service.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
