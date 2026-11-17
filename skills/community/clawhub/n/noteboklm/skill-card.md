## Description:

Complete Google NotebookLM integration for adding sources, asking questions, generating Studio content, downloading artifacts, and managing notebooks programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikolayco](https://clawhub.ai/user/nikolayco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to automate NotebookLM research workflows: importing sources, querying notebooks, generating study or presentation artifacts, downloading outputs, and managing NotebookLM state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local, cloud, and web sources into NotebookLM, which may expose sensitive or regulated content.

Mitigation: Use a dedicated Google account or isolated profile and avoid uploading sensitive or regulated documents unless that transfer is explicitly intended.

Risk: The skill can change notebook context and manage exports or sharing, including public links and editor permissions.

Mitigation: Confirm exact files and notebook IDs before import, and manually approve export or sharing changes before execution.

Risk: The skill relies on an unofficial library and undocumented NotebookLM APIs that may change or break without notice.

Mitigation: Prefer a pinned and audited version of notebooklm-py, and recheck behavior before deployment or after upstream NotebookLM changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nikolayco/skills/noteboklm)
- [notebooklm-py upstream library](https://github.com/teng-lin/notebooklm-py)
- [notebooklm-py troubleshooting documentation](https://github.com/teng-lin/notebooklm-py/blob/main/docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and references to generated NotebookLM artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide commands that create, download, export, or share NotebookLM artifacts after user approval where required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
