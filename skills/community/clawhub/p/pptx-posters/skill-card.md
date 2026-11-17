## Description:

Generates structured slide and academic poster outlines from existing paper abstracts or paper content, with layout guidance and optional helper code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and developers use this skill to turn existing paper abstracts or paper content into structured poster or slide outlines with assumptions, design notes, and manual review checks. It is not intended to write original research, fabricate figures, or create submission-ready academic work without review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated helper code may be unsafe if executed with untrusted abstracts or output paths.

Mitigation: Treat generated *_generator.py files as untrusted, review them before execution, and avoid running them on untrusted inputs or paths.

Risk: The release may overstate finished PowerPoint or poster generation capability.

Mitigation: Use the skill as an outline, layout, and helper-code generator; manually verify formatting, citations, figures, and final presentation quality.

Risk: Encrypted, image-only, or corrupt PDFs may not be parseable.

Mitigation: Request a text version or abstract directly when a PDF cannot be parsed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/pptx-posters)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text outlines, with optional generated Python helper code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit layout recommendations, design guidelines, figure placeholders, manual checks, and optional python-pptx helper code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
