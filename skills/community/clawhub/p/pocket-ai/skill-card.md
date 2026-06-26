## Description: <br>
Turn voice recordings into actionable intelligence with semantic search, action item extraction, and meeting context awareness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asabovetech](https://clawhub.ai/user/asabovetech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Attorneys, entrepreneurs, executives, consultants, founders, and their agents use this skill to query Pocket AI recordings for meeting context, action items, contact history, decisions, and daily briefing material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad access to sensitive Pocket AI recordings and transcript-derived profile data. <br>
Mitigation: Install only for trusted agents, protect and rotate the API key, and require explicit approval before sharing recording-derived output to channels or other tools. <br>
Risk: Cloud data flow and sharing controls are under-disclosed for the sensitivity of the accessed recordings. <br>
Mitigation: Review Pocket AI service terms and organizational data-handling requirements before commercial use. <br>
Risk: Heartbeat automation could repeatedly retrieve or surface sensitive action items without user intent. <br>
Mitigation: Enable heartbeat checks only deliberately and limit automated output to the minimum needed for the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asabovetech/pocket-ai) <br>
- [Pocket AI API documentation](https://docs.heypocketai.com/docs/api) <br>
- [Pocket AI documentation](https://docs.heypocketai.com) <br>
- [Pocket AI device](https://heypocket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python code snippets, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include sensitive transcript excerpts, action items, profile insights, recording metadata, and API search results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
