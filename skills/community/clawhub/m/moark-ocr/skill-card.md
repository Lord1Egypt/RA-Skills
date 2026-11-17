## Description:

Perform Optical Character Recognition (OCR) to extract and recognize text from images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fchange](https://clawhub.ai/user/fchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run OCR on provided images through Gitee AI, then receive extracted text and a brief summary based on the user's prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images or image URLs may be uploaded to an external OCR provider.

Mitigation: Use only non-sensitive images that are intentionally approved for external processing, and avoid remote or internal URLs.

Risk: API keys can be passed on the command line.

Mitigation: Prefer the GITEEAI_API_KEY environment variable and avoid exposing keys in shell history, process listings, or logs.

Risk: The skill can process arbitrary local paths or URLs with weak input boundaries.

Mitigation: Run it in a restricted workspace or virtual environment with pinned dependencies and review inputs before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fchange/skills/moark-ocr)
- [Gitee AI API endpoint](https://ai.gitee.com/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with extracted OCR text and a brief summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITEEAI_API_KEY; the OCR script emits results under an OCR_RESULT marker for the agent to present.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
