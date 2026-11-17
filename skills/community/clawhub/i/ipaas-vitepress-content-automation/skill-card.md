## Description:

Automatically drafts B2B system-integration solution Markdown and deploys the resulting VitePress documentation site over SSH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evan-ch](https://clawhub.ai/user/evan-ch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to create B2B iPaaS integration case-study pages, update a VitePress site's navigation, and publish the built documentation to a configured server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSH deployment can create persistent remote access or publish to an unintended remote path when deployment settings are misconfigured.

Mitigation: Use a dedicated low-privilege deployment account, verify SSH host-key fingerprints out of band, restrict the authorized key and remote write directory, validate SERVER_PORT and REMOTE_DIR, and require explicit manual confirmation before deployment.

Risk: The skill can modify local VitePress content and navigation files before publishing.

Mitigation: Review generated Markdown and configuration diffs before running the deployment step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evan-ch/skills/ipaas-vitepress-content-automation)
- [Taobao Open Platform API documentation](https://open.taobao.com/doc.htm)
- [Kingdee Cloud Xingchen API documentation](https://open.jdy.com/#/files/api/detail?index=3&categrayId=3cc8ee9a663e11eda5c84b5d383a2b93)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown documents, VitePress configuration edits, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local VitePress docs and config files and may run an SSH/rsync deployment when invoked.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact frontmatter states 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
