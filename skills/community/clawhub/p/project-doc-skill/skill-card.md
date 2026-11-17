## Description:

Create or maintain a PROJECT.md source-of-truth doc for any project, quiz-first with project-type branches. Use only when the user explicitly asks for project documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tooled-app](https://clawhub.ai/user/tooled-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to create or maintain a concise PROJECT.md source-of-truth after an explicit documentation request. It captures project purpose, stack, build/run details, structure, decisions, changelog entries, and notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or edit PROJECT.md in a project root.

Mitigation: Confirm the intended project root and that PROJECT.md creation or editing is desired before installation or use.

Risk: Package metadata shows a hash or version mismatch according to the security guidance.

Mitigation: Verify the release with the publisher or registry when provenance integrity matters for the environment.

## Reference(s):

- [PROJECT.md section templates](artifact/references/templates.md)
- [ClawHub skill page](https://clawhub.ai/tooled-app/skills/project-doc-skill)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Markdown PROJECT.md content and concise conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or edits only PROJECT.md at the confirmed project root; no shell-command execution is evidenced.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
