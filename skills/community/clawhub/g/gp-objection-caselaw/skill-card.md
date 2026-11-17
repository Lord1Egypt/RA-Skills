## Description:

A Chinese-language government-procurement objection response assistant that matches similar complaint decisions, compares sustained and rejected objection patterns, flags reply risks, and drafts compliant objection response letters for PRC government procurement matters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement staff, agencies, and legal reviewers use this skill after a supplier objection is received to find similar PRC government procurement complaint decisions, compare legal and factual reasoning, identify weak reply positions, and draft a structured response letter for review.

### Deployment Geography for Use:

Mainland China for PRC government procurement matters

## Known Risks and Mitigations:

Risk: The skill can produce legal-assistant guidance and draft objection responses that may be incorrect, incomplete, or inapplicable without current source support.

Mitigation: Require human legal or procurement review before sending any response, and require every legal conclusion, case reference, and objection outcome to be anchored to the configured knowledge bases or marked for verification.

Risk: The artifact includes behavior that asks agents to persist newly observed risk patterns into trusted skill instruction files.

Mitigation: Install and run the skill read-only for normal users; handle risk-pattern updates as maintainer-reviewed release changes rather than automatic runtime writes.

Risk: The skill depends on mounted IMA knowledge bases for complaint decisions, statutes, and procurement-file lookup.

Mitigation: When a required knowledge base is unavailable or a result lacks full text, downgrade the output to verification-required guidance and do not claim that matching cases or legal authorities were confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/gp-objection-caselaw)
- [README](artifact/README.md)
- [Case Matching Guide](artifact/references/case-matching-guide.md)
- [Reply Letter Template](artifact/references/reply-letter-template.md)
- [Risk Pattern Library](artifact/references/risk-pattern-library.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables and structured Chinese-language drafting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes case-match summaries, risk warnings, a draft response letter, and an internal complaint-risk preview; legal conclusions require source anchoring and human review.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
