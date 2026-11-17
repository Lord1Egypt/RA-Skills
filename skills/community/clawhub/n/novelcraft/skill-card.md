## Description:

Novelcraft helps OpenClaw agents create complete novels from an idea through concept, optional images, chapters, review, and PDF/EPUB publication using a configurable modular workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kesuek](https://clawhub.ai/user/kesuek)

### License/Terms of Use:

MIT-0

## Use Case:

External authors, editors, and developers use Novelcraft to plan and generate long-form fiction projects with configurable target audiences, chapter review, optional images, and publication outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Templates include fixed local paths and a fixed private-network image endpoint.

Mitigation: Review and replace path and endpoint values before installation; keep image generation disabled until the destination is explicitly trusted.

Risk: Optional image generation may send manuscript content to external services.

Mitigation: Use manual or local image providers for sensitive manuscripts, and avoid sensitive personal information in prompts or project files.

Risk: Autonomous mode can run broad subagent-control workflows with limited intermediate review.

Mitigation: Start in step-by-step mode inside an isolated workspace and review generated configs, drafts, and publication outputs before switching to autonomous use.

## Reference(s):

- [Novelcraft ClawHub Page](https://clawhub.ai/kesuek/skills/novelcraft)
- [Getting Started Guide](GETTING-STARTED.md)
- [Configuration Reference](references/CONFIG.md)
- [Security Considerations](SECURITY.md)
- [Workflow Fixes](WORKFLOW-FIXES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, configuration snippets, generated manuscript files, and publication instructions; final book artifacts may include PDF and EPUB files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw subagent support and uses pandoc plus optional xelatex for publication; image generation is optional and depends on the configured provider.]

## Skill Version(s):

3.2.3 (source: server release metadata; artifact manifests state 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
