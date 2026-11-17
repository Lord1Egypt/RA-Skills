## Description:

Run content past a reviewer before it goes out: who is on the team, what they said on a draft, how a share link gets a client's approval, and what "approved" does and does not mean in Postey.

This skill is ready for commercial/non-commercial use.

## Publisher:

[posteyai](https://clawhub.ai/user/posteyai)

### License/Terms of Use:

MIT-0

## Use Case:

Social media teams, agencies, and clients use this skill to identify reviewers, read internal feedback, resolve share links, and revise drafts based on review. It helps report approval accurately and keep publishing or scheduling under the user's explicit instruction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anyone holding a share link can read the associated draft.

Mitigation: Keep sensitive information out of drafts shared by link, and account for the possibility that a recipient forwards the link.

Risk: A reviewer's approval could be mistaken for authorization to publish or schedule.

Mitigation: Publish or schedule only after the user explicitly instructs it.

Risk: The separate Postey integration is outside the security review of the supplied skill files.

Mitigation: Use a trusted Postey integration.

## Reference(s):

- [Postey Teams on ClawHub](https://clawhub.ai/posteyai/skills/postey-teams)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Natural-language review summaries, draft content, and Markdown diffs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports review feedback and approval context; publishing or scheduling requires explicit user instruction.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
