## Description:

GInstall OneClick helps an agent install GitHub Node.js projects by planning setup, cloning repositories, installing dependencies, and starting development scripts through the ginstall CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunzhouli-hub](https://clawhub.ai/user/yunzhouli-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when they want an agent to set up a GitHub Node.js project locally, including monorepo tree URLs and private repositories that require a GitHub token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unknown GitHub projects can run untrusted setup, dependency, or development scripts through an external CLI.

Mitigation: Use plan-only mode first, inspect package scripts and dependency sources, avoid --yes for unfamiliar repositories, and run installs in a disposable sandbox or container.

Risk: GitHub tokens used for private repositories may be exposed to dependency installs or development scripts.

Mitigation: Keep GITHUB_TOKEN out of dependency-install and runtime environments when possible, use minimum contents:read scope, and avoid pasting tokens into chat or plan files.

## Reference(s):

- [GInstall OneClick CLI repository](https://github.com/ginstall-oneclick/ginstall-oneclick)
- [ClawHub skill page](https://clawhub.ai/yunzhouli-hub/skills/one-click-installation-of-github-projects)
- [OpenClaw skill format](https://docs.openclaw.ai/clawhub/skill-format)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct users to plan Markdown and report paths produced by the ginstall CLI.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
