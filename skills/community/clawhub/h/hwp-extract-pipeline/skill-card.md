## Description:

Extracts text from Korean HWP/HWPX files using hwp-reader, pyhwp, direct HWPX parsing, and fallback methods; advertised PDF/OCR support should be reviewed because the security evidence says it is overstated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heoboong](https://clawhub.ai/user/heoboong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to convert local Korean HWP/HWPX document attachments into JSON text output for downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill overstates PDF/OCR support.

Mitigation: Review implementation and documentation before relying on PDF/OCR extraction; correct the documentation or add the missing PDF/OCR behavior.

Risk: The skill can execute local programs and accepts a user-influenced --venv path.

Mitigation: Run it in a constrained workspace with trusted local tools, and do not pass untrusted virtual-environment paths.

Risk: Extracted document text is written to disk under an identifier-influenced filename.

Mitigation: Validate the identifier as a simple filename-safe value and handle generated *_extracted.json files as retained document contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heoboong/skills/hwp-extract-pipeline)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands]

**Output Format:** [JSON written to stdout and to a local *_extracted.json file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Run output includes id, source path, extracted text, method, notes, and elapsed time fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
