## Description:

Guides users through configuring OpenClaw, Nginx, and GitHub Actions to establish a secure, autonomous GitHub integration pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patello](https://clawhub.ai/user/patello)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and configure a GitHub-to-OpenClaw webhook flow with Nginx proxying, GitHub Actions payload construction, explicit agent authorization, HTTPS guidance, and optional session grouping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens can be exposed if webhook testing sends authorization headers over HTTP.

Mitigation: Require HTTPS before sending tokens where possible; rotate any token used over HTTP and disable the HTTP route after testing.

Risk: Webhook-triggered agent runs may trust prompt text or GitHub comments before taking repository actions.

Mitigation: Verify GitHub webhook signatures or trusted event metadata outside the agent, restrict GitHub permissions, and require human approval for write actions triggered by issue or PR comments.

Risk: Automated server configuration changes can override existing routing.

Mitigation: Warn before modifying Nginx, firewall, Certbot, or OpenClaw files and proceed only with explicit user authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patello/skills/github-webhook-architect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON, YAML, Nginx, AGENTS.md, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to OpenClaw and Nginx configuration only after explicit user authorization.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact frontmatter reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
