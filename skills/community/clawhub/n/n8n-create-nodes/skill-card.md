## Description:

Build production-ready n8n community nodes as npm packages, covering declarative and programmatic node styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rwilson504](https://clawhub.ai/user/rwilson504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold and implement n8n community node packages, including declarative REST nodes, programmatic nodes, credential types, triggers, local testing, and npm publishing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scaffold cleanup commands can remove an existing Git history if run in the wrong working directory.

Mitigation: Run scaffold commands only in a fresh project directory and verify the working directory before removing `.git`.

Risk: Credential examples can lead to weak secret handling if copied without adapting them to the target API.

Mitigation: Mask secret fields, prefer header-based credential injection, and use query parameters only when the API requires them.

Risk: Generated delete, webhook, and poll examples can affect external data or registrations during testing.

Mitigation: Test destructive operations, webhook registration, and polling behavior with sandbox data before publishing or linking a node into n8n.

## Reference(s):

- [Credential Patterns](references/CREDENTIAL_PATTERNS.md)
- [Trigger Node Patterns](references/TRIGGER_PATTERNS.md)
- [Examples](references/EXAMPLES.md)
- [Common Mistakes](references/COMMON_MISTAKES.md)
- [ClawHub Skill Page](https://clawhub.ai/rwilson504/skills/n8n-create-nodes)
- [Source Homepage](https://github.com/rwilson504/agent-skills/tree/main/n8n-create-nodes)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces n8n node package scaffolding and implementation guidance; no runtime service is embedded in the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
