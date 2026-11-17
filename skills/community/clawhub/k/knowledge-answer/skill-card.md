## Description:

Provides knowledge-answer response guidance that preserves the user's language and adds clickable numbered citations when answers rely on search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvinecarn](https://clawhub.ai/user/alvinecarn)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide knowledge-answer responses so they remain in the user's language and include numbered, clickable citation footnotes when search results are used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activation metadata may be affected by malformed or truncated frontmatter description text.

Mitigation: Review the skill frontmatter before deployment and confirm the activation description is complete.

Risk: Citation formatting guidance can still produce incorrect or unsupported references if source selection is weak.

Mitigation: Review cited answers for source relevance and verify that each numbered link supports the sentence it follows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alvinecarn/skills/knowledge-answer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with clickable numbered citation links when sources are used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains the user's language by default unless another language is explicitly requested.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
