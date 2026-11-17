## Description:

Extract text and metadata from PDF files using PyMuPDF, with optional JSON output for agent-readable results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nantes](https://clawhub.ai/user/nantes)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect local PDF files, extract page text and document metadata, and optionally write the extracted content to JSON for downstream reading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The stated current-directory file boundary can be bypassed with symlinks, allowing unintended local file reads or overwrites.

Mitigation: Review before installing, run only in a trusted working directory, avoid untrusted symlinks, use a virtual environment with a pinned PyMuPDF version, and do not rely on the current-directory restriction until path handling is fixed to reject or safely resolve symlinks.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text summary or JSON file containing PDF metadata and extracted page text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional page limit and optional .json output path.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
