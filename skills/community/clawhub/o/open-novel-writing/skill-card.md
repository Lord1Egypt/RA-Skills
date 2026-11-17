## Description:

open-novel-writing helps agents support Chinese long-form novel creation from worldbuilding and outlining through chapter planning, drafting, review, revision, and batch writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[softmeng](https://clawhub.ai/user/softmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and creative-writing agents use this skill to plan, draft, review, and iteratively improve Chinese long-form fiction projects. It can also guide batch chapter generation with local project files for specs, manuscript text, and review reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch writing can overwrite chapter specifications, manuscript text, and review files in the active novel project.

Mitigation: Run the skill in a dedicated project directory and review or back up generated files before using batch mode.

Risk: Optional Python dependencies and CLI examples may vary by local environment.

Mitigation: Install dependencies only through a trusted Python environment and treat CLI examples as rough documentation to verify before use.

## Reference(s):

- [Writing Principles](references/writing_principles.md)
- [Review Criteria](references/review_criteria.md)
- [Novel Template](references/novel_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance, YAML chapter specifications, plain-text chapter drafts, Python commands, and local project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch mode can create or overwrite local chapter specifications, manuscript text, and review reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
