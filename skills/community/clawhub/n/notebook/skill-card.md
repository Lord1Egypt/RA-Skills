## Description:

Local-first personal knowledge base for tracking ideas, projects, tasks, habits, and any object type you define. YAML-based with no cloud lock-in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to define personal object types, create and search YAML-backed notebook entries, link related items, and prompt deeper expansion of ideas, tasks, projects, habits, books, people, or other custom objects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Type names can escape the intended notebook data folder and create, modify, or delete files outside the notebook area.

Mitigation: Run the skill only in a low-privilege workspace, avoid untrusted type names or imported notebook files, and review filesystem changes before relying on important notes.

Risk: The security verdict is suspicious for this release.

Mitigation: Review the local file behavior before installation and update dependencies before using the skill for important note data.

## Reference(s):

- [ClawHub Notebook skill page](https://clawhub.ai/thesethrose/skills/notebook)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with notebook CLI commands and local YAML-backed file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes notebook data under the configured workspace and emits terminal-readable status, lists, object details, and expansion questions.]

## Skill Version(s):

1.0.2 (source: server release evidence; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
