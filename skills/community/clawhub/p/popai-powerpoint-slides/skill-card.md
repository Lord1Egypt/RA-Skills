## Description:

Create presentations (PPT) using PopAI API. Use when asked to create slides, presentations, decks, or PPT content via PopAI. Supports uploading reference files (pptx/pdf/docx/images).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zdawang000](https://clawhub.ai/user/zdawang000)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate PowerPoint decks from a topic and optional reference or template files through PopAI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation prompts and selected reference files are sent to PopAI and its S3 storage.

Mitigation: Avoid confidential, regulated, or secret material unless that transfer is approved.

Risk: The documented predictable /tmp output path could expose progress data or collide with another process on shared systems.

Mitigation: Use a securely created temporary output file for JSONL progress polling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zdawang000/skills/popai-powerpoint-slides)
- [Publisher profile](https://clawhub.ai/user/zdawang000)
- [PopAI](https://www.popai.pro)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [JSON Lines progress events and final PPTX/web URLs, typically summarized to the user as Markdown or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and POPAI_API_KEY. Optional local file uploads are limited to five files and final presentations are delivered as PopAI-hosted PPTX download links.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
