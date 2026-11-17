## Description:

Parses literature text and returns a Chinese summary, keywords, and core conclusions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyt0302](https://clawhub.ai/user/lyt0302)

### License/Terms of Use:

MIT-0

## Use Case:

Readers, students, researchers, and agents can use this skill to convert submitted literature text into a concise Chinese summary, keywords, and core conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill treats every user message as document text and can override normal assistant behavior.

Mitigation: Use it only where a default literature summarizer is intended, or change the trigger to activate only on explicit literature-analysis requests.

Risk: The fixed Chinese-only output format may be unsuitable when the user expects clarification, another language, or a different response structure.

Mitigation: Allow clarification and user-selected output language before using the fixed summary, keywords, and conclusions format.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyt0302/skills/literature-parser)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Chinese text with labeled sections for summary, keywords, and core conclusions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fixed response sections: summary, keywords, and core conclusions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
