## Description:

2-agent collaborative software development workflow for OpenClaw

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to coordinate a project-manager agent and developer agent that plan, implement, test, and package small software projects from a written request. It is best suited for landing pages, React or Next.js applications, prototypes, component libraries, developer tools, and documentation sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents broad ability to modify files, run shell commands, install dependencies, use Git, and prepare deployments.

Mitigation: Install and run it only in a dedicated project workspace, review planned commands and diffs, and confirm Git remotes or deployment targets before publication.

Risk: Generated projects can include incorrect code, vulnerable dependencies, or incomplete tests.

Mitigation: Run builds, tests, dependency audits, and human code review before using generated output in production.

Risk: Credentials or production secrets could be exposed if the agents work inside a sensitive repository.

Mitigation: Keep production secrets out of the workspace and use isolated credentials or environment files that are reviewed before command execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chloepark85/skills/multi-agent-dev-team)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw](https://openclaw.ai)
- [Skill README](artifact/README.md)
- [Project Specification Template](artifact/templates/project-spec-template.md)
- [Landing Page Example](artifact/examples/landing-page-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses, generated project files, shell commands, configuration snippets, and code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initialize Git repositories, install dependencies, run tests, and prepare deployment-oriented deliverables when the agent environment permits.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
