## Description:

Local-first CRM for managing leads, deals, follow-ups, and pipelines via a SQLite-backed command-line workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frank-bot07](https://clawhub.ai/user/frank-bot07)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and sales operators use this skill to manage local CRM records, track pipeline activity, schedule follow-ups, search contacts and deals, generate reports, and publish Markdown interchange files for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive CRM records may be stored locally and exported into Markdown files that other agents can read.

Mitigation: Treat the CRM database and interchange directory as sensitive, restrict access, and avoid using real customer data without redaction and explicit opt-in controls.

Risk: Agent-readable CRM Markdown may contain embedded user content from deals, activities, notes, or contacts.

Mitigation: Do not feed generated interchange files to agents that may follow embedded instructions unless content has been reviewed, escaped, or filtered.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frank-bot07/skills/openclaw-crm)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text output and Markdown interchange files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores CRM data in a local SQLite database and can generate agent-readable Markdown summaries.]

## Skill Version(s):

1.0.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
