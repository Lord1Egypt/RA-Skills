## Description:

Meta Cloudbase guides agents through CloudBase full-stack development and deployment by routing requests to the right source capabilities, checking prerequisites, validating work, and recording local learning notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to plan, implement, configure, and verify CloudBase web, mini-program, mobile, Cloud Function, CloudRun, database, authentication, AI Agent, and UI work. It is intended to improve routing and prerequisite checks for CloudBase delivery tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad CloudBase development and deployment guidance can affect live users, cloud resources, databases, authentication providers, and cost.

Mitigation: Require explicit confirmation before production deployments, database writes, provider or authentication changes, or cost-incurring actions.

Risk: The learner stores notes and preferences locally in plaintext.

Mitigation: Do not record secrets, tokens, credentials, sensitive incident details, or private customer data in learner notes or preferences.

Risk: The skill depends on CloudBase MCP and source skill details that are not embedded in the artifact.

Mitigation: Confirm CloudBase MCP configuration and consult the relevant source skill before deployment, database, authentication, or SDK-specific work.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/qq435912743/skills/meta-cloudbase)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code, command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local learned_patterns.json when the learner script is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
