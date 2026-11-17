## Description:

GInstall OneClick helps an agent set up GitHub Node.js projects locally by planning the install, cloning the repository, installing dependencies, and starting a development-oriented script through the ginstall CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunzhouli-hub](https://clawhub.ai/user/yunzhouli-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they want an agent to install and run a GitHub Node.js project from an owner/repo string, a full GitHub URL, or a monorepo tree URL. It is intended for local setup workflows that need clear planning, guided execution, and optional private repository access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to run an unpinned external CLI that can clone repositories, install dependencies, and execute repository scripts.

Mitigation: Use only repositories and a ginstall binary you trust, begin with plan-only or guided review before execution, and avoid non-interactive approval for unfamiliar repositories.

Risk: Private repository access may require a GitHub token.

Mitigation: Provide a minimally scoped GITHUB_TOKEN only when private repository access is necessary, and keep tokens in the environment or host secret storage rather than chat or shared files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yunzhouli-hub/skills/ginstall-oneclick)
- [GInstall OneClick homepage](https://github.com/ginstall-oneclick/ginstall-oneclick)
- [Upstream CLI repository](https://github.com/YunzhouLi-hub/GInstall-OneClick)
- [OpenClaw skill format](https://docs.openclaw.ai/clawhub/skill-format)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer users to plan Markdown and report paths emitted by the ginstall CLI.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
