## Description:

Organizes Desktop and Downloads files into type-based folders for images, documents, archives, video, audio, code, executables, and fonts, then reports the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to preview and organize cluttered Desktop and Downloads folders by file type, with generated reports showing scanned, organized, skipped, and errored files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move files in Desktop and Downloads during non-preview execution.

Mitigation: Use dry-run mode first and review the proposed moves before allowing file changes.

Risk: Same-name destination collisions may not have an explicit safe policy and could overwrite or fail unexpectedly.

Mitigation: Avoid non-preview execution until the implementation defines a collision policy such as skip, rename, or ask before replacing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-file-organizer)
- [Publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces dry-run previews and execution reports; no third-party Python dependencies are required.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
