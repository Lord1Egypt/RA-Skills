## Description:

Build SaaS projects end-to-end with OpenClaw as orchestrator and Gemini CLI as a local planning and generation copilot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiromps](https://clawhub.ai/user/hiromps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product builders use this skill to turn SaaS, web app, MVP, internal tool, dashboard, landing page, or productized automation requests into requirements, architecture, implementation plans, source scaffolds, repository setup, and optional deployment steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product briefs or planning prompts may include confidential or regulated information.

Mitigation: Remove sensitive data before using Gemini CLI and keep regulated data out of prompts unless the environment is approved for that use.

Risk: Repository creation, pushes, or Vercel deployment can change external systems when authenticated CLIs are available.

Mitigation: Confirm explicit user intent, repository visibility, authentication status, environment variables, and deploy target before running publishing or deployment steps.

Risk: Generated requirements, architecture, code, or shell commands may be incomplete or unsuitable for the target product.

Mitigation: Review generated files, scan for secrets, run tests, and validate deployment settings before release.

## Reference(s):

- [Repo and Deploy Checklist](references/repo-and-deploy-checklist.md)
- [SaaS Build Modes](references/saas-build-modes.md)
- [SaaS Doc Templates](references/saas-doc-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local files, repository setup steps, and deployment guidance that require user review before external side effects.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
