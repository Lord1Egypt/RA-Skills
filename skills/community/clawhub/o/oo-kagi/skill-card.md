## Description:

Summarizes text or document URLs with Kagi Universal Summarizer, with optional translation and key takeaways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can submit text or document URLs for a Kagi summary. They can also request translation or key takeaways.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A missing CLI dependency may trigger an unverified online installer without a user approval step.

Mitigation: Review and approve setup commands separately, and prefer a verified release before installation.

Risk: Text and document URLs submitted for summarization pass through OOMOL to Kagi.

Mitigation: Submit only content appropriate to share with those services.

## Reference(s):

- [Kagi Universal Summarizer](https://kagi.com/summarizer/)
- [Kagi API documentation](https://help.kagi.com/kagi/api/overview.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include translation or key takeaways when requested.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
