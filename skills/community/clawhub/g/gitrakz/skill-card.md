## Description:

Drive a self-hosted gitrakz instance to sync GitHub activity into local SQLite, query timelines and work sessions, manage templates, and export results through REST or MCP interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install or operate a trusted gitrakz instance, trigger GitHub activity syncs, inspect timelines and work-session summaries, and run or export deterministic report templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and runtime may rely on external installer or container code while handling a live GitHub token.

Mitigation: Review the installer before running it, prefer per-user installation, pin container images by immutable digest where possible, avoid rolling `:latest` with real credentials, and use a dedicated fine-grained read-only GitHub token.

Risk: Optional LLM features may send commit titles or diffs to the configured LLM endpoint.

Mitigation: Leave LLM settings empty unless the endpoint is trusted and the user accepts sharing that repository activity context.

Risk: A system-wide install can broaden who can operate the shared stack.

Mitigation: Use the per-user path by default and choose `--system` only after auditing the installer and confirming the host access model.

## Reference(s):

- [gitrakz ClawHub Skill Page](https://clawhub.ai/psyb0t/skills/gitrakz)
- [gitrakz Homepage](https://github.com/psyb0t/gitrakz)
- [gitrakz setup](references/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with inline bash, JSON, and endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce REST or MCP requests and CSV, PDF, or JSON export instructions for a user-controlled gitrakz instance.]

## Skill Version(s):

0.7.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
