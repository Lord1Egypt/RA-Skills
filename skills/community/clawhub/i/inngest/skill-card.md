## Description: <br>
Manage Inngest serverless background jobs and event-driven workflows via REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dwhite-oss](https://clawhub.ai/user/dwhite-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate Inngest event-driven workflows by sending events, listing apps and runs, inspecting run history, canceling runs, and replaying failed jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real Inngest background jobs when valid credentials are available. <br>
Mitigation: Use scoped and rotatable credentials, and require explicit confirmation of the target environment, payload, and RUN_ID before sending events, canceling runs, or replaying failed jobs. <br>
Risk: Inngest credentials may be exposed if pasted into chat, command history, or logs. <br>
Mitigation: Provide credentials through environment variables and avoid echoing keys or embedding them directly in shared transcripts. <br>


## Reference(s): <br>
- [ClawHub Inngest release page](https://clawhub.ai/dwhite-oss/inngest) <br>
- [Inngest Management API base](https://api.inngest.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires INNGEST_EVENT_KEY and INNGEST_SIGNING_KEY environment variables for authenticated Inngest operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
