## Description:

Lemma is an AI operating system platform for business teams. Use this as the single entrypoint when designing, provisioning, testing, or improving Lemma pods, datastores, integrations, functions, workflows, desks, assistants, agents, widgets, or workspace execution, then route to the matching module guide.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepak-jha-kgp](https://clawhub.ai/user/deepak-jha-kgp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business platform builders use this skill to design, provision, test, and improve Lemma pods and related resources for AI-powered business workflows. It routes work to focused module guides for integrations, functions, datastores, workflows, desks, assistants, agents, widgets, and workspace execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes local authentication and desk setup flows that handle Lemma tokens and environment files.

Mitigation: Use short-lived least-privilege test tokens, keep tokens out of URLs and source files, review .env.local before sharing or committing, and clear browser localStorage after testing.

Risk: Desk scaffold and bundle scripts install and build npm dependencies, including mutable package versions.

Mitigation: Run setup only in trusted projects, review generated files and dependency changes, and pin or audit package versions before production use.

Risk: The skill can guide provisioning of Lemma resources that affect data, workflows, integrations, and user-facing desks.

Mitigation: Follow the documented design-first routing, verify upstream resources before wiring desks, and grant agents, assistants, tables, folders, and applications only the access they need.

## Reference(s):

- [Lemma Skill Page](https://clawhub.ai/deepak-jha-kgp/skills/lemma)
- [Known CLI Behavior](modules/lemma-main/references/known-cli-behavior.md)
- [Desk Testing Guide](modules/lemma-desks/testing.md)
- [VoltAgent Design Markdown References](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads, shell commands, configuration snippets, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes the agent to module-specific guides and may produce implementation plans, resource definitions, scripts, and verification steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
