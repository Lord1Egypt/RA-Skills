## Description:

Generate polished corporate PowerPoint decks from user content using a light H3C-style template with layout helpers, icon support, QA, and scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksfrist](https://clawhub.ai/user/ksfrist)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn supplied content into light-themed corporate PowerPoint decks, improve existing PPTs, and apply template-consistent layouts, icons, QA checks, and scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory may retain unfiltered PPT feedback or best-practice notes.

Mitigation: Use a dedicated memory directory, avoid storing sensitive presentation content, and periodically review or delete memory/ppt-feedback.md and memory/ppt-best-practices.md.

Risk: Untrusted feedback stored in shared agent memory could influence later deck-generation behavior.

Mitigation: Review feedback before adding it to shared memory and keep project-specific feedback isolated from unrelated agent work.

## Reference(s):

- [Page Types Catalog](references/page-types.md)
- [ClawHub skill page](https://clawhub.ai/ksfrist/skills/ppt-light-corporate)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with Python code snippets and generated PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [QA and scoring workflows can produce local text reports and append PPT feedback or best-practice notes to memory files.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
