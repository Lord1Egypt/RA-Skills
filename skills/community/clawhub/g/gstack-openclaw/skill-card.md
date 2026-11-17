## Description:

Gstack Openclaw is a documentation-only OpenClaw skill collection that gives agents structured engineering-team roles for product planning, architecture, design review, debugging, security review, QA, release, deployment, status tracking, and retrospectives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo-jiqimao](https://clawhub.ai/user/leo-jiqimao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to guide software work through specialized agent roles such as product planning, engineering design, code review, QA, security assessment, deployment preparation, and retrospectives. It produces structured guidance, reports, checklists, code examples, shell commands, and configuration snippets for human review and execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual installation guidance in the skill text includes a git clone plus ./install.sh command even though the release is intended to be documentation-only.

Mitigation: Install through ClawHub or copy reviewed markdown files only; do not run the manual ./install.sh command from the skill text.

Risk: Some subskills describe production deploy, rollback, PR merge, browser-login, and auto-fix workflows that could affect real systems or source files.

Mitigation: Require explicit human approval, reviewed plans, scoped credentials, and environment checks before applying any operational recommendation.

Risk: The skill may mention external services and API credentials while presenting examples and best practices.

Mitigation: Treat external service content as guidance unless the user has separately installed authorized integrations and provided scoped credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leo-jiqimao/skills/gstack-openclaw)
- [Security Policy](SECURITY.md)
- [Workflow Guide](docs/workflow.md)
- [Garry Tan gstack](https://github.com/garrytan/gstack)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with reports, checklists, code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only prompts; operational recommendations involving production deployment, rollback, PR merge, browser login, or auto-fix require explicit review, scoped credentials, and human approval before action.]

## Skill Version(s):

2.5.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
