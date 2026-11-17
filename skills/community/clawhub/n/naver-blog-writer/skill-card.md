## Description:

Publish prepared content to Naver Blog from an authenticated local browser on the buyer machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y80163442-boop](https://clawhub.ai/user/y80163442-boop)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to publish already prepared posts to Naver Blog through a local macOS runner after setup and one-time login. It is not intended for drafting posts, SEO planning, or topic research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned third-party npm runner that can handle login, live publishing, and persistent local services.

Mitigation: Use pinned package versions and integrity verification, and run setup or daemon commands only after reviewing and trusting the package source and current release.

Risk: The live publishing path can post to the user's Naver Blog account.

Mitigation: Require explicit confirmation before publish_live, use dry_run for preview, and document how to stop or uninstall any local service.

## Reference(s):

- [Naver Blog Publisher on ClawHub](https://clawhub.ai/y80163442-boop/skills/naver-blog-writer)
- [Publisher profile](https://clawhub.ai/user/y80163442-boop)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live publish returns naver_publish_result; preview and readiness flows return dry_run or doctor/capabilities JSON, with structured recovery fields on failure.]

## Skill Version(s):

0.6.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
