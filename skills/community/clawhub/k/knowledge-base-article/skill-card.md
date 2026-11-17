## Description:

Turns support notes into a plain-language US knowledge base article with sources, review dates and accessibility notes. Use when the user asks for knowledge base article template, help center article writer, internal support doc template. For US support leads, technical writers and customer success teams who own a help center or an internal knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US support leads, technical writers, and customer success teams use this skill to turn support notes into sourced, accessible knowledge-base article drafts and editor review checklists.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Support notes may contain customer personal, account, ticket, or health information, and the workflow does not automatically redact input.

Mitigation: Anonymize notes before processing; do not include real customer identifiers or health information.

Risk: Running the digest again in the same output folder replaces digest.md, and unsupported claims could reach a published article if a draft is not reviewed.

Mitigation: Use a dedicated output folder, preserve drafts as needed, verify claims against cited sources, and have the article owner review and publish it.

Risk: The optional Windows application is unsigned; a listed checksum alone does not establish that it is safe.

Mitigation: The app is unnecessary for this workflow; avoid it unless you make a separate trust decision and verify the download independently.

## Reference(s):

- [US rules and standards for support articles](artifact/references/kb-article-standards.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/knowledge-base-article)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown article draft, source-gap digest, review block, accessibility notes, and publication checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts require human source and editorial review; the skill does not publish articles. The digest script overwrites digest.md in its output folder.]

## Skill Version(s):

1.0.6 (source: artifact/SKILL.md frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
