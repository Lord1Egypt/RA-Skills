## Description:

A Chinese-language novel-writing workflow that helps agents plan, draft, continue, rewrite, and quality-check fiction from short stories through long-form novels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwl2005](https://clawhub.ai/user/lwl2005)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and agents use this skill to structure Chinese fiction projects, build outlines and character/state records, draft chapters, continue existing manuscripts, rewrite chapters, and run staged quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft, rewrite, continuation, or state-saving workflows may overwrite manuscript or state files if the target paths are unclear.

Mitigation: Before file-saving or continuation steps, specify the manuscript folder and files, and ask the agent to confirm filenames before writing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lwl2005/skills/novel-writer-engine)
- [Writing Style Guide](artifact/references/writing-styles.md)
- [Genre Templates](artifact/references/genre-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown prose with optional JSON state snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update manuscript drafts and state files when the user asks the agent to save progress.]

## Skill Version(s):

3.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
