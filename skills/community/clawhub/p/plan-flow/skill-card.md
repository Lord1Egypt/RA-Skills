## Description:

Plan Flow provides structured AI-assisted development workflows for discovery, planning, execution, code reviews, and testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brunoscardoso](https://clawhub.ai/user/brunoscardoso)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use Plan Flow to structure AI-assisted software work across project setup, requirements discovery, implementation planning, plan execution, code and PR review, API contract drafting, and test generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can direct an agent to create or edit repository files automatically.

Mitigation: Review generated changes before committing or deploying them, especially after autopilot or plan execution workflows.

Risk: The ledger behavior can silently retain project-specific memory in flow/ledger.md.

Mitigation: Keep flow/ledger.md out of sensitive contexts, review its contents periodically, and prune entries that may expose private project details.

Risk: The configuration example places an API key in .plan-flow.yml.

Mitigation: Do not store real API keys in project configuration files; use environment variables or an approved secret-management mechanism.

Risk: The contract workflow can fetch or process API documentation URLs.

Mitigation: Avoid using /create-contract on internal or untrusted URLs unless the environment controls network access and the target is approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brunoscardoso/skills/plan-flow)
- [Project Homepage](https://github.com/brunoscardoso/plan-flow)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documents, code snippets, shell commands, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates workflow files under flow/; some workflows require git or the GitHub CLI.]

## Skill Version(s):

1.0.8 (source: SKILL.md frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
