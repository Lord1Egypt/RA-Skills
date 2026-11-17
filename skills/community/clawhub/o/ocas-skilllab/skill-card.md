## Description:

Skilllab helps agents maintain skill libraries by auditing, merging, renaming, deleting, publishing, sanitizing, critiquing, and improving skills across profile directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use Skilllab to manage agent skill libraries, evaluate skill quality, sanitize content, and prepare skill packages for publication or synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous audit behavior can execute code from other installed skills.

Mitigation: Run autonomous evaluation only in a sandbox with no secrets, no network, and a disposable copy of the skill library.

Risk: Workflows can broadly mutate, archive, sanitize, commit, and push skill files.

Mitigation: Preview rename, delete/archive, sanitize, publish, commit, and push actions before allowing them.

Risk: The security verdict is suspicious for normal installation.

Mitigation: Install only when the agent is expected to manage local skill libraries and git-backed skill repositories.

## Reference(s):

- [Support File Map](references/support-file-map.md)
- [Critique Rubric](references/critique-rubric.md)
- [Skill Sanitize Checklist](references/skill-sanitize-checklist.md)
- [Skill Publish Spec Compliance Checklist](references/skill-publish-spec-compliance-checklist.md)
- [Skill Sync Discovery](references/skill-sync-discovery.md)
- [Secret History Rewrite](references/secret-history-rewrite.md)
- [Tool Integration Pattern](references/tool-integration-pattern.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with checklists, command examples, and generated edits or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform local skill-library and git operations when agent permissions allow; preview high-impact actions such as rename, archive, sanitize, publish, commit, or push.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog report 3.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
