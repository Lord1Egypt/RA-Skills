## Description:

宽数题库项目入口，涵盖四套量化题库来源、仓库结构、常用命令与当前公网部署信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aznikline](https://clawhub.ai/user/aznikline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to understand, run, extend, validate, and deploy the kuanshu-tiku multi-source quantitative puzzle bank project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents a one-command production Vercel deployment using an unpinned CLI and --yes, which can bypass an explicit human safety check.

Mitigation: Review the repository and build output, install with npm ci and a lockfile, pin the Vercel CLI version, confirm the target Vercel account and project, run a preview deployment first, and avoid --yes for production without human approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aznikline/skills/kuanshu-tiku)
- [Publisher profile](https://clawhub.ai/user/aznikline)
- [GitHub repository](https://github.com/aznikline/kuanshu-tiku)
- [Current public site](https://quantics-bank.vercel.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and project paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
