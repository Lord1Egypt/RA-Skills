## Description:

Analyze images and multi-frame sequences using OpenAI GPT series.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agents through OpenAI vision analysis for images, OCR-style text extraction, visual comparison, and multi-frame temporal review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted images, image URLs, prompts, and extracted text may be sent to the OpenAI API.

Mitigation: Avoid confidential screenshots, personal documents, regulated data, and secrets unless approved for that API use.

Risk: API credentials could be exposed if copied into code, prompts, or logs.

Mitigation: Keep OPENAI_API_KEY in secure environment configuration and out of source files and logs.

Risk: Vision outputs can be unreliable for medical diagnosis, exact object counts, small or rotated text, precise spatial reasoning, and distorted images.

Mitigation: Use the skill for assistive analysis, keep human review for high-impact decisions, and verify results against source images.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON output schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The guided API output is typically structured JSON containing analysis text, metadata, extracted data, and warnings.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
