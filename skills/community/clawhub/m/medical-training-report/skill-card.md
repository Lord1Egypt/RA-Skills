## Description:

Generates digest endoscopy medical-training activity reports for offline, hybrid, or online courses using user-provided schedules, attendance records, scores, presentation images, transcripts, and related materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caolicao1234-web](https://clawhub.ai/user/caolicao1234-web)

### License/Terms of Use:

MIT-0

## Use Case:

Medical training staff and report authors use this skill to collect course materials, summarize training content, parse Excel scores or quiz results, and generate structured DOCX activity reports for digest endoscopy training events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process medical-training materials, trainee names, scores, feedback, and local file paths.

Mitigation: Redact patient data and unnecessary personal identifiers, confirm authorization to process trainee information, and avoid exposing sensitive local paths.

Risk: The bundled workflow relies on local Python execution and document generation.

Mitigation: Use a controlled Python environment with pinned dependencies and review generated reports before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caolicao1234-web/skills/medical-training-report)
- [Information collection template](references/info_collection_template.md)
- [Template structure](references/template_structure.md)
- [Course introduction templates](references/course_intro_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON structures and shell command examples; generated reports are DOCX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes user-provided local paths and training materials; Excel parsing is used for scores, quizzes, and feedback when available.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
