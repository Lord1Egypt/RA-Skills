## Description: <br>
Hourly Knowledge sends users a short, useful fact every hour and uses recent-topic history to reduce repeated themes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrmiracle1](https://clawhub.ai/user/mrmiracle1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who opt in to recurring updates use this skill to receive brief hourly knowledge facts. It is intended for automated, plain-text fact delivery with basic recent-topic de-duplication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends recurring automatic messages from the configured bot account. <br>
Mitigation: Install only for users or channels that have opted in to hourly fact messages, and confirm the configured accountId is appropriate. <br>
Risk: The helper script includes a config command that can print the configured accountId. <br>
Mitigation: Do not expose or run the config helper command in contexts where the account identifier should remain private. <br>
Risk: The skill keeps a local history of recently sent topics. <br>
Mitigation: Treat the topic history as local operational data and avoid adding sensitive topics to the history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrmiracle1/hourly-knowledge) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mrmiracle1) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text fact message, usually concise and may include emoji] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a rolling history of the 10 most recent topics to reduce repeated themes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
