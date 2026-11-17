## Description:

Creates a migration package that captures project status, decisions, files, risks, and next steps so another AI session or model can continue the work without reading the prior conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shary-ho](https://clawhub.ai/user/shary-ho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI users, and project teams use this skill when handing off active work to another model, another chat, or a future collaborator. It produces a structured project migration package and preserves relevant generated or uploaded files so the next agent can resume from verified context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect and package broad workspace or conversation data, including sensitive files that should not be shared.

Mitigation: Confirm the project root, request a file manifest, exclude secrets such as .env files, keys, tokens, credential stores, private databases, hidden files, and unrelated uploads, then review the final package before sharing it.

Risk: The handoff may contain unsupported assumptions if project directories, files, or conversation history cannot be inspected.

Mitigation: Require unknown or unavailable information to be marked explicitly instead of inferred, and review the migration package for unsupported claims before reuse.

## Reference(s):

- [Migration Package template](references/template.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown migration package plus collected project files, optionally packaged as a ZIP archive]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a 16-section handoff template covering status, decisions, failed attempts, attachments, risks, and a next-agent prompt.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
