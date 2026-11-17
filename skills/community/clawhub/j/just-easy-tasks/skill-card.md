## Description:

Use when an agent needs to work with Just Easy Tasks (JET) via the jet CLI or API: configure API key/context, find, create, update, complete, comment on, link, reference, or inspect tasks and project metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-w-s](https://clawhub.ai/user/ryan-w-s)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use Jet to manage Just Easy Tasks workspaces and projects through the jet CLI or API, including task lookup, updates, completion, comments, links, references, and project metadata inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running an unreviewed global JET CLI package could execute code outside the skill artifact.

Mitigation: Install only if the JET npm package and service are trusted, prefer a reviewed or pinned CLI version, and avoid global npm installs as an administrator.

Risk: Credential and context configuration can direct task changes to the wrong workspace or project.

Mitigation: Set API keys, workspace, and project context deliberately, and use command-level overrides when operating outside the configured default.

Risk: Force and admin mutation commands can change or remove shared task-management resources.

Mitigation: Use force flags and admin command enablement only when the user explicitly asks for those workspace-level changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-w-s/skills/just-easy-tasks)
- [Just Easy Tasks service](https://justeasytasks.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JSON-oriented, non-interactive CLI examples for scripts where appropriate.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
