## Description:

Search Prediction Bridge prediction-market events by text or X (Twitter) link via the backend API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallyunet](https://clawhub.ai/user/smallyunet)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find prediction-market events related to a topic, headline, article URL, or X/Twitter status link and present ranked market matches with brief snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, article URLs, and X/Twitter links are sent to Prediction Bridge's backend.

Mitigation: Use only content suitable for that external service; avoid secrets, private/internal links, personal data, and confidential business text unless the service is trusted for that data.

Risk: The skill depends on a reachable external API and may return empty or failed results when the backend is unavailable or rejects an input.

Mitigation: Confirm the API base URL when requests fail, retry transient failures, and ask for a more specific query or plain text when no strong matches are returned.

## Reference(s):

- [Prediction Bridge homepage](https://www.predictionbridge.xyz)
- [ClawHub skill page](https://clawhub.ai/smallyunet/skills/prediction-bridge-dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline links and optional shell commands; backend responses are parsed from JSON before presentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents ranked prediction-market events, optional related news, and concise market snapshots; raw JSON is not shown by default.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
