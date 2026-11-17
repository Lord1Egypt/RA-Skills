## Description:

Turn rough project notes into polished portfolio case studies with metrics, visuals checklist, and interviewer talking points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, developers, and portfolio builders use this skill to convert rough project material into case study drafts, visuals checklists, interview talking points, and FAQ answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scaffold script can overwrite an existing output file when given a path that already exists.

Mitigation: Write scaffold output to a new file in the current project folder and avoid absolute paths, traversal paths, symlinks, or important existing files.

Risk: The skill may process project notes, metrics, screenshots, or links supplied by the user.

Mitigation: Use it only with information the user is comfortable sharing with the active agent session, and keep assumptions or unverified facts clearly marked.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/portfolio-case-study-forge)
- [Case Study Template](artifact/resources/case_study_template.md)
- [Example Prompt](artifact/examples/example-prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown drafts and checklists, with optional JSON scaffold files from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should mark assumptions clearly and avoid fabricating metrics, credentials, legal certainty, receipts, or evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact CHANGELOG; artifact SKILL.md frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
