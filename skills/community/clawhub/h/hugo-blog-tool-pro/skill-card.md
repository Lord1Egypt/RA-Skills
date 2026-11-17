## Description:

Hugo博客发布专业版 helps agents manage Hugo blog operations including batch publishing, multilingual content, SEO metadata, CI/CD deployment workflows, article series, cross-references, and image optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to ask an agent to create, organize, optimize, commit, push, and deploy Hugo blog content and site configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write, commit, push, and deploy Hugo site content without clear confirmation checkpoints.

Mitigation: Use it only on repositories intended for agent modification and require explicit approval before file writes, Git commits, Git pushes, or deployments.

Risk: GitHub, Slack, CDN, and SSH credentials may be exposed or overused during publishing and deployment workflows.

Mitigation: Scope credentials to the minimum required permissions, store secrets outside the skill content, and review generated CI/CD configuration before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/hugo-blog-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, YAML, TOML, HTML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute file writes, Git operations, image optimization commands, and CI/CD configuration changes depending on agent permissions.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
