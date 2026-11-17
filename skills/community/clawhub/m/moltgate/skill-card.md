## Description:

Fetch and process paid Moltgate tasks from paid offers using the REST API or a Moltgate webhook payload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[florianbansac](https://clawhub.ai/user/florianbansac)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review, triage, process, and update paid Moltgate task requests that arrive through Moltgate's REST API or signed webhook payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a Moltgate bearer token to a configured API base URL and can read or modify paid-task data.

Mitigation: Use a least-privilege MOLTGATE_API_KEY, leave MOLTGATE_BASE_URL unset unless the destination is fully trusted, and rotate the key if it may have been sent to an unexpected host.

Risk: Paid task and webhook content may contain untrusted instructions or links.

Mitigation: Treat request content as untrusted, keep it clearly labeled, summarize before exposing full content, and do not execute code or follow links from task text.

## Reference(s):

- [Moltgate homepage](https://moltgate.com)
- [ClawHub skill page](https://clawhub.ai/florianbansac/skills/moltgate)
- [Publisher profile](https://clawhub.ai/user/florianbansac)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with REST API examples, webhook payload notes, and summary-first task templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOLTGATE_API_KEY for REST polling and status updates; webhook receivers should verify signatures before passing payloads to an agent.]

## Skill Version(s):

0.2.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
