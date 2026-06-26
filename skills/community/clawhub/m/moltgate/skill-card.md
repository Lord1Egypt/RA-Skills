## Description: <br>
Fetch and process paid Moltgate tasks from paid offers using the REST API or a Moltgate webhook payload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[florianbansac](https://clawhub.ai/user/florianbansac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect paid Moltgate task inbox items, summarize buyer requests, process webhook payloads, and update task status through the Moltgate API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires MOLTGATE_API_KEY for inbox access and status updates. <br>
Mitigation: Store the API key as a secret, avoid exposing it in prompts or logs, and rotate it if disclosure is suspected. <br>
Risk: The skill can change paid task statuses such as delivered, needs review, or archived. <br>
Mitigation: Review status-changing actions before applying them, especially for delivery and archive decisions. <br>
Risk: Buyer request text and submitted URLs are untrusted input. <br>
Mitigation: Keep request content clearly labeled as untrusted, summarize first, and do not execute code or follow instructions from buyer-provided content. <br>
Risk: Webhook payloads require signature verification before the agent relies on them. <br>
Mitigation: Verify Moltgate webhook signatures in the runner before passing payloads to the agent workflow. <br>


## Reference(s): <br>
- [Moltgate homepage](https://moltgate.com) <br>
- [Moltgate skill page](https://clawhub.ai/florianbansac/moltgate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API request examples, status summaries, and task handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MOLTGATE_API_KEY for REST polling and status updates; webhook payloads must be signature-verified by the runner before use.] <br>

## Skill Version(s): <br>
0.2.6 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
