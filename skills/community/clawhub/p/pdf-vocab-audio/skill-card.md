## Description:

Extracts English vocabulary from a PDF and generates MP3 pronunciation audio that reads each word or phrase twice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[effeceee](https://clawhub.ai/user/effeceee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and educators use this skill to turn PDF vocabulary lists into spoken English study audio. It is suited for vocabulary practice workflows where extracted words or phrases can be sent to the configured text-to-speech tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF-derived vocabulary text may be processed by an external text-to-speech service.

Mitigation: Use only PDFs whose extracted text is acceptable to share with edge-tts; avoid confidential PDFs unless the publisher adds an explicit privacy notice.

Risk: Generated MP3 files are written to a predictable location in /tmp.

Mitigation: Review generated filenames and remove outputs after use, or require a private configurable output directory before using sensitive material.

Risk: Runtime behavior depends on external binaries and Python packages.

Mitigation: Install dependencies from trusted sources and prefer pinned versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/effeceee/skills/pdf-vocab-audio)
- [ClawHub publisher profile](https://clawhub.ai/user/effeceee)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and an MP3 audio file written to /tmp]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates one MP3 vocabulary reading file named from the source PDF filename.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
