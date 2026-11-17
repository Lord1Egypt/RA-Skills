## Description:

Manage Google NotebookLM notebooks, sources, chats, artifacts, and exports through the notebooklm-py CLI with safe workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suidge](https://clawhub.ai/user/suidge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Google NotebookLM notebooks, sources, chats, generated artifacts, and exports through the notebooklm-py CLI. The skill is intended for safe account-backed NotebookLM workflows that require auth checks, explicit notebook selection, JSON output, and review before destructive or long-running actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and use a third-party CLI with their NotebookLM account.

Mitigation: Pin notebooklm-py to a trusted reviewed version, install it with pipx rather than global pip, and verify authentication with notebooklm auth check --test --json before account-backed workflows.

Risk: Notebook, source, artifact, sharing, generation, and download actions may expose files or NotebookLM content or perform destructive changes.

Mitigation: Use only notebooks and files intended for NotebookLM, prefer explicit notebook IDs and JSON output, and require user review before delete, clean, share, generate, download, saved-note, or wait actions.

## Reference(s):

- [notebooklm-py CLI Reference](references/notebooklm-py-cli.md)
- [ClawHub Skill Page](https://clawhub.ai/suidge/skills/notebooklm-py-skill)
- [Skill Homepage](https://github.com/Suidge/notebooklm-py-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers explicit notebook IDs and --json output; asks before destructive, long-running, sharing, generation, download, and file-writing actions.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
