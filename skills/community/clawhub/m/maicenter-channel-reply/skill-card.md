## Description: <br>
Polls mAICenter channels for incoming messages and sends replies over REST for short-lived agents that cannot keep a long-running channel plugin process alive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maicenter](https://clawhub.ai/user/maicenter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add REST-based polling and reply behavior for mAICenter channels in serverless, cron, or container-per-task agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: mAICenter channel messages and the MAICENTER_AGENT_KEY may be exposed through normal use of the service. <br>
Mitigation: Protect MAICENTER_AGENT_KEY like a password, scope channel access appropriately, and avoid channels with sensitive or regulated data unless policy allows mAICenter processing. <br>
Risk: An automated agent may send replies to channels where its behavior is not expected. <br>
Mitigation: Use this only for intended mAICenter channel workflows, restrict the agent's channel participation, and review reply logic before deployment. <br>


## Reference(s): <br>
- [mAICenter homepage](https://maicenter.org) <br>
- [ClawHub skill page](https://clawhub.ai/maicenter/maicenter-channel-reply) <br>
- [mAICenter publisher profile](https://clawhub.ai/user/maicenter) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl examples and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAICENTER_AGENT_KEY and mAICenter channel access.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
