## Description:

OpenClaw News Publisher helps agents create Markdown news drafts, preview article content, and publish or prepare distribution across configured platforms such as RSS, WeChat, and Twitter/X.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Content teams, developers, and operators use this skill to maintain a Markdown-first publishing workflow: create article drafts, preview content, run dry-runs, publish RSS output, and prepare platform-specific publishing for connected services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned remote Node code and dependencies may change between review and installation.

Mitigation: Review or pin the referenced repository and dependencies before installation or use.

Risk: Publishing commands can expose article content and metadata through connected services.

Mitigation: Use preview and dry-run modes first, then publish only with test or low-privilege platform accounts until the workflow is approved.

Risk: Platform credentials stored in environment files can grant access to publishing accounts.

Mitigation: Protect the .env file, restrict credential scope, and rotate credentials if they are exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/news-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces publishing workflow guidance, draft article structures, preview commands, dry-run commands, and credential configuration notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
