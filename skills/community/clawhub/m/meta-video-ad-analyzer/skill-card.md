## Description:

Extract and analyze content from video ads using Gemini Vision AI. Supports frame extraction, OCR text detection, audio transcription, and AI-powered scene analysis. Use when analyzing video creative content, extracting text overlays, or generating scene-by-scene descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortytwode](https://clawhub.ai/user/fortytwode)

### License/Terms of Use:


## Use Case:

Developers and marketing analysts use this skill to extract scene descriptions, visible text, transcripts, and thumbnail references from video or image ad creatives for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media content may be sent to Google AI services during analysis.

Mitigation: Only analyze media that the user is authorized to process with those services.

Risk: OCR, transcription, and scene descriptions may be incomplete or incorrect.

Mitigation: Treat extracted text and descriptions as untrusted analysis output and review them before business, legal, or compliance decisions.

Risk: The skill depends on local media tooling and Python packages that can vary by environment.

Mitigation: Install it in a dedicated virtual environment or container and pin dependency versions when reproducibility matters.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, configuration]

**Output Format:** [Python dataclass output with structured text timelines and thumbnail references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include duration, transcript, OCR text timeline, scene timeline, thumbnail URL, and extraction status.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
