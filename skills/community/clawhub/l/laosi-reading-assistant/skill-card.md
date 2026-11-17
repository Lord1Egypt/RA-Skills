## Description:

阅读助手 accepts pasted text or webpage URLs and extracts four concise reading points: main idea, key arguments, action items, and open questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and knowledge workers use this skill to quickly understand long articles, papers, technical documentation, or messages by receiving a structured four-part summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic local logging may save sensitive summaries or source details.

Mitigation: Use the skill only with non-sensitive material unless logging requires explicit consent and users can inspect and delete saved records.

Risk: Broad URL fetching may retrieve private, internal, or unintended locations.

Mitigation: Restrict fetching to safe HTTP and HTTPS destinations, block local or internal targets, and enforce response-size limits before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-reading-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown reading summary with structured fields; the artifact also includes Python example code that can emit JSON-compatible extraction records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are organized around main idea, key arguments, action items, and open questions.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
