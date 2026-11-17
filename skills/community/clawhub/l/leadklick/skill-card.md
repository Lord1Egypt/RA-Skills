## Description:

Automates lead capture in Supabase with Make.com email workflows, lead status management, conversation logging, and auto-reply tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[big-roman123](https://clawhub.ai/user/big-roman123)

### License/Terms of Use:

MIT

## Use Case:

Developers and sales automation teams use this skill to let agents create, retrieve, list, update, and delete CRM leads, log conversations, and monitor automated first-reply delivery through a Supabase-backed workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests a highly privileged Supabase service role key.

Mitigation: Review the credential model before installation and prefer a least-privilege server-side API or restricted database role.

Risk: Lead and conversation records can contain personal or sensitive business data.

Mitigation: Define privacy, consent, redaction, and retention rules before storing lead conversations.

Risk: Data access depends on organization scoping and may be under-scoped if the database or API role is configured incorrectly.

Mitigation: Add and verify organization scoping on every read and write path, and confirm Supabase RLS policies enforce the same boundary.

Risk: The skill exposes destructive lead deletion behavior.

Mitigation: Document deletion behavior and require explicit confirmation before deleting lead records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/big-roman123/skills/leadklick)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [Lead schema](schemas/lead.json)
- [Conversation schema](schemas/conversation.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and TypeScript examples with JSON configuration and response objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces lead IDs, status values, conversation IDs, counts, automation status, and Supabase-backed CRM records.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata, package.json, README.md, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
