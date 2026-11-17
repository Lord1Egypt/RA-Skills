## Description:

Drafts replies to specific existing LinkedIn comments from their URLs, resolves the correct LinkedIn parent comment target, and can publish the approved reaction and reply through Publora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to continue an existing LinkedIn comment thread with concise reply drafts, reaction guidance, and the correct parentComment target before approving a live post.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approving a draft can modify the user's live LinkedIn presence by sending both a reaction and a reply.

Mitigation: Review the exact reply text, reaction type, target comment URL, and parentComment before approving publication.

Risk: An incorrect parentComment can place the reply in the wrong thread or cause the publish request to fail.

Mitigation: Use the resolved top-level comment URN for parentComment and verify the thread preview before posting.

Risk: Reply drafts may be inappropriate for business or public-facing accounts if context is incomplete.

Mitigation: Confirm the thread context and edit the draft before approval, especially when automated comment fetching is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sergebulaev/skills/linkedin-reply-handler)
- [Reply templates](artifact/references/reply-templates.md)
- [Threading rules](artifact/references/threading-rules.md)
- [Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with short reply drafts, reaction suggestion, thread context summary, approval card, and posting target details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reply drafts are intended to be 150-300 characters each and require user approval before posting.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
