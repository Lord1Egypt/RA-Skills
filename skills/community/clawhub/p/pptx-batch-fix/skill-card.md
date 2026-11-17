## Description:

Formats PPT/PPTX files in batches by raising undersized text to a configurable minimum, enabling wrapping, correcting out-of-bounds shapes, and detecting or removing slide numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwenqi123123](https://clawhub.ai/user/liuwenqi123123)

### License/Terms of Use:

MIT-0

## Use Case:

Office users and agents that process presentation files use this skill to produce cleaned PPTX copies with minimum font sizing, bounded shapes, and optional page-number detection or removal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PPTX layout or formatting can change unexpectedly during font resizing, wrapping, boundary correction, or page-number removal.

Mitigation: Run the skill on copies or separate output files, then inspect the generated presentation before replacing an original.

Risk: The page-number removal heuristics can remove numeric content that matches page-number patterns or appears in the lower-right page-number area.

Mitigation: Run page-number detection first and review the output presentation, especially when slides contain numeric labels near the bottom right.

Risk: The fallback dependency installation command uses an unpinned python-pptx package source.

Mitigation: Prefer the preinstalled dependency when available, or pin and trust the dependency source before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuwenqi123123/skills/pptx-batch-fix)
- [Publisher profile](https://clawhub.ai/user/liuwenqi123123)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, script output, and generated PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts read input PPTX files and write separate output PPTX files before any replacement.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
