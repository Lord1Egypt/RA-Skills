## Description:

Connects to an explicitly configured Smartisan Notes service with username or email credentials so an agent can manage cloud notes, folders, starred and pinned states, trash recovery, WeChat-ready HTML, and Markdown-to-PNG long-image exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoolee](https://clawhub.ai/user/zhaoolee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to operate their own configured Notes service from an agent: list, query, create, update, classify, star, pin, delete, restore, and export notes. It is also useful for producing WeChat-compatible HTML or PNG long images from Markdown content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted env files used with export_note.sh can execute shell commands when sourced.

Mitigation: Use only trusted env files, inspect them before use, keep them outside version control, and prefer process environment variables or explicit CLI parameters when practical.

Risk: Markdown export can upload local files referenced by Markdown image paths.

Mitigation: Review Markdown image references before export, process only trusted Markdown files, and use inline Markdown only for remote image URLs when local uploads are not intended.

Risk: Reusable account credentials may be sent to a configured Notes service over plain HTTP.

Mitigation: Use HTTPS for non-local Notes servers, verify the service operator is trusted, and avoid putting passwords in shell history, logs, or committed files.

## Reference(s):

- [Workspace API and command reference](references/workspace-api.md)
- [ClawHub skill page](https://clawhub.ai/zhaoolee/skills/notes-export-api)
- [Publisher profile](https://clawhub.ai/user/zhaoolee)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands; invoked scripts can return JSON, HTML, Markdown, or PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an explicitly configured Notes service URL and credentials; no default service endpoint is used.]

## Skill Version(s):

0.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
