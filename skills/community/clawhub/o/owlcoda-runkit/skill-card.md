## Description:

OwlCoda RunKit helps Codex coordinate receipt-backed, project-owned work, including assignments, checkpoints, handoffs, verification evidence, ready-for-commit receipts, and read-only foreign-project shadowing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeemio](https://clawhub.ai/user/yeemio)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and engineering agents use this skill to manage durable project execution through local RunKit artifacts, explicit work ownership, verification receipts, and handoff or recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage durable execution receipts and local .owlcoda/runkit state in a project.

Mitigation: Use it only in projects where that local coordination state is intended, and review generated RunKit artifacts before relying on them.

Risk: The skill invokes the external owlrunkit CLI package.

Mitigation: Review the external package and keep it pinned to the exact expected version before using it for skill installation, deployment, or fleet operations.

Risk: RunKit workflows may reach higher-risk actions such as skill installation, deployment, or fleet operations.

Mitigation: Require separate explicit authority for higher-risk actions and treat RunKit receipts as evidence, not permission to commit, publish, deploy, or perform destructive work.

## Reference(s):

- [OwlCoda product site](https://owlcoda.com/#start)
- [OwlCoda RunKit Contract v0.2](references/contract-v0.2.md)
- [OwlCoda RunKit Contract v0.1](references/contract-v0.1.md)
- [OwlCoda RunKit 0.22.1 npm rollback baseline](https://registry.npmjs.org/owlrunkit/-/owlrunkit-0.22.1.tgz)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npx; writes local .owlcoda/runkit control artifacts when authorized by the user workflow.]

## Skill Version(s):

0.23.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
