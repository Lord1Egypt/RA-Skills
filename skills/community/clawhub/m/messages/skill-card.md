## Description: <br>
Messages manages incoming email, chat, and other communications by triaging urgency, drafting replies for review, tracking threads awaiting responses, reducing notification noise, and summarizing the user's communication landscape. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EthAgent](https://clawhub.ai/user/EthAgent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users use Messages to triage incoming email and chat, draft responses for review, track conversations needing follow-up, and review communication patterns across connected channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill implies broad, ongoing access to private email, chat, and cross-channel communication data. <br>
Mitigation: Require explicit approval for each connected channel, scope access to only necessary folders or contacts, and exclude sensitive sources before use. <br>
Risk: Voice matching and relationship views may create behavioral profiles from sent messages and conversation history. <br>
Mitigation: Limit or disable sent-message profiling unless needed, and confirm that message history, relationship profiles, and behavior summaries can be reviewed and deleted. <br>
Risk: Draft replies, follow-ups, unsubscribe actions, and mute actions could affect external communications if executed without review. <br>
Mitigation: Require user confirmation for each sent message, mute, unsubscribe, or cleanup action, including review of the exact text before sending. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or structured text summaries and draft replies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include daily briefings, reply drafts, follow-up prompts, noise-reduction recommendations, and weekly communication reviews.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
