## Description:

Provides base64 encoding, decoding, and validation utilities for data handling and transformation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to encode, decode, validate, and detect Base64 or URL-safe Base64 data in transformation workflows. It can also help convert buffers, JSON objects, data URIs, and trusted local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File decode helpers can overwrite an existing local file when given its path.

Mitigation: Provide explicit trusted paths and avoid decodeToFile targets that point to important existing files unless overwrite is intended.

Risk: File encode helpers can read any local path supplied by the caller.

Mitigation: Use only trusted, intended input paths when encoding files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-base64-toolkit)
- [ClawHub publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [text, code, shell commands, files]

**Output Format:** [Plain text, JSON, JavaScript module exports, and file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [File helpers read from and write to caller-provided local paths.]

## Skill Version(s):

1.0.0 (source: package.json and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
