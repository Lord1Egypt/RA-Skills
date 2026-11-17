## Description:

Read and write flomo memos on macOS through the local flomo desktop login state, incoming webhook, or URL scheme.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dotheworknow](https://clawhub.ai/user/dotheworknow)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent fetch, search, filter by tag, summarize, and create flomo memos on a logged-in macOS desktop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses a logged-in flomo account and private memos.

Mitigation: Install only if this account access is acceptable, review commands before execution, and do not share local flomo configuration or tokens.

Risk: Webhook write and verification flows can create real memos in the user's account.

Mitigation: Review write and verify commands before running them, and run webhook verification only when creating a test memo is acceptable.

Risk: Changing FLOMO_API_BASE can redirect authenticated API calls.

Mitigation: Use the default flomo API base unless an alternate endpoint has been explicitly reviewed and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dotheworknow/skills/openclaw-flomo-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON tool output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads may return memo content, tags, timestamps, and HTML-derived text; write and verify flows can create real flomo memos.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
