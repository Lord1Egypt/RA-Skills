## Description:

Automates Instagram comment-to-DM funnels through the Upload-Post API, including keyword-triggered private replies, persistent monitoring, one-shot semantic matching, and follow-up reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mutonby](https://clawhub.ai/user/mutonby)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agent operators use this skill to turn Instagram post or Reel comments into private DM workflows for lead magnets, campaign replies, and follow-up reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent or bulk DM automation can message more people than intended if the post, keywords, audience, duration, or stop controls are not confirmed.

Mitigation: Confirm the exact post, message, trigger keywords, audience, monitoring duration, and pause, stop, or delete controls before starting a monitor or bulk DM action.

Risk: Instagram automation can violate Meta rules or applicable consent and anti-spam requirements if used for cold outreach, excessive retries, or irrelevant messages.

Mitigation: Use only user-initiated comment-to-DM flows, stop on rate limits, keep messages relevant, and verify campaign compliance before execution.

Risk: The skill requires an Upload-Post API key for Instagram automation workflows.

Mitigation: Install only if you trust Upload-Post with the Instagram workflow and API key, and handle the key as a credential.

## Reference(s):

- [Upload-Post homepage](https://upload-post.com)
- [Upload-Post API docs](https://docs.upload-post.com)
- [Upload-Post LLM reference](https://docs.upload-post.com/llm.txt)
- [Meta Compliance Reference](references/compliance.md)
- [Meta Private Replies API](https://developers.facebook.com/docs/instagram-platform/private-replies/)
- [ClawHub skill page](https://clawhub.ai/mutonby/skills/instagram-auto-reply-comments)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash commands and operational status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Upload-Post API requests, monitor IDs, comment and DM counts, and error summaries for Instagram comment-to-DM workflows.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
