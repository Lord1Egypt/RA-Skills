## Description:

Know whether the things you scheduled actually went out, find the ones that failed, and fix them. Publishing is asynchronous — created is not published, and scheduled is not published either.

This skill is ready for commercial/non-commercial use.

## Publisher:

[posteyai](https://clawhub.ai/user/posteyai)

### License/Terms of Use:

MIT-0

## Use Case:

Social account operators use this skill to verify whether scheduled posts were published on each platform, diagnose delivery and queue problems, and choose safe recovery steps for failed or deleted posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A retry after partial publishing success could create duplicate posts.

Mitigation: Check publishing status for each platform and ask the user before retrying.

Risk: Restoring a deleted post returns it to DRAFT, and later scheduling could publish it.

Mitigation: Check the trash, let the user choose which posts to restore, and get explicit approval before scheduling or publishing.

Risk: Connecting social accounts involves permissions managed by a separate Postey integration.

Mitigation: Review that integration's account permissions before connecting.

## Reference(s):

- [Postey Ops on ClawHub](https://clawhub.ai/posteyai/skills/postey-ops)
- [Postey AI publisher profile](https://clawhub.ai/user/posteyai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown status summaries and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-platform publishing status, likely failure causes, queue health, and user-controlled recovery recommendations.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
