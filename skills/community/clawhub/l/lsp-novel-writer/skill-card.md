## Description:

LSP Novel Writer helps agents collect Chinese web-novel requirements, generate an outline, confirm it with the user, and draft chapters into separate Markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[156554395](https://clawhub.ai/user/156554395)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writers use this skill to plan and draft Chinese web novels across popular genres. The agent guides requirements collection, outline confirmation, chapter generation, and draft file creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated chapter files may consume storage or collide with existing drafts in the selected novels folder.

Mitigation: Choose or monitor the output folder before generation, and review any existing ./novels/<novel title>/ directory before allowing chapter files to be written.

Risk: Long-form generated fiction can contain continuity, pacing, or quality issues across chapters.

Mitigation: Use the outline confirmation step and chapter self-checks for goals, plot logic, word count, hooks, and character consistency before accepting the generated draft.

## Reference(s):

- [Web Novel Writing Guide](references/writing-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown chapter files and prose guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates one Markdown file per chapter under ./novels/<novel title>/ when the agent follows the skill workflow.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
