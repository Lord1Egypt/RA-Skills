## Description:

Grant proposal writing assistant for NIH (R01/R21), NSF, and other mainstream funding applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, grant writers, and proposal teams use this skill to draft NIH, NSF, and other mainstream grant proposal sections, budget justifications, and review checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can read or overwrite local files through user-supplied input and output paths.

Mitigation: Run it in a sandboxed workspace, pass only proposal paths you control, avoid absolute or traversal paths, and do not target existing important files for output.

## Reference(s):

- [NIH R01 Grant Proposal Template](references/NIH_R01_template.md)
- [NSF Standard Grant Template](references/NSF_template.md)
- [Budget Templates by Category](references/budget_templates.md)
- [Grant Proposal Review Checklist](references/review_checklist.md)
- [Specific Aims Examples](references/specific_aims_examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown templates and review guidance, with optional command-line output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates proposal sections, full proposal templates, budget justifications, and checklist-style reviews.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
