## Description:

Extract invariant principles from text and identify ideas that survive rephrasing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to distill documents, methodology notes, code comments, or other text into structured principle observations with confidence levels and source evidence. It is useful when readers need concise, reviewable patterns rather than claims of verified truth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive pasted content may be processed by the user's configured model provider.

Mitigation: Avoid submitting secrets or regulated data unless the configured agent and model provider are approved for that content.

Risk: Extracted principles are pattern observations, not verified truths.

Mitigation: Review the extracted principles and validate them against additional sources before relying on them.

Risk: Documentation mentions review artifacts in a way that may confuse users about whether files are written to disk.

Mitigation: Clarify this behavior during review; the current security evidence says the skill does not write files to disk.

## Reference(s):

- [PBE Extractor source homepage](https://github.com/live-neon/skills/tree/main/pbd/pbe-extractor)
- [PBE Extractor on ClawHub](https://clawhub.ai/leegitw/skills/pbe-extractor)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Guidance]

**Output Format:** [Structured JSON or Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes principle statements, normalized forms, confidence levels, source evidence, compression metrics, and next steps when applicable.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
