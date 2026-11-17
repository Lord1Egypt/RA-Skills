## Description:

Compresses a given PDF file to reduce its size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upwell](https://clawhub.ai/user/upwell)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to compress local PDF files with selectable compression levels and receive the compressed file path plus size details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes user-selected local PDF files and writes a new compressed copy.

Mitigation: Use it only on PDFs that are appropriate to process locally and verify the generated output before sharing or replacing originals.

Risk: Medium and high compression can remove metadata and reduce image quality.

Mitigation: Keep the original PDF, choose the lowest compression level that meets the size target, and review the compressed document for fidelity.

Risk: Dependencies are range-pinned and no lockfile is included in the release evidence.

Mitigation: Prefer installing from an environment with reviewed or locked dependency versions for reproducible deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upwell/skills/pdf-compressor)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [JSON object with compression status, output path, original size, and compressed size]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a compressed PDF next to the input file using a generated filename.]

## Skill Version(s):

0.1.4 (source: ClawHub release evidence; artifact frontmatter and pyproject.toml state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
