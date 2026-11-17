## Description:

Supports Chinese government-procurement evaluation committees in deciding whether a specific bidder response should be treated as an invalid bid, clarified or corrected, and in drafting report-ready reasoning with cited procurement rules and tender clauses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement reviewers, evaluation committee experts, and compliance professionals use this skill to assess concrete bidder-response issues against Chinese government-procurement requirements and produce structured decision-support notes for invalid-bid or clarification decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may influence consequential Chinese government-procurement evaluation decisions if its legal citations, knowledge-base results, or factual assumptions are accepted without review.

Mitigation: Treat outputs as decision support only, verify cited rules and source materials against current official references, preserve review records, and keep final invalid-bid or clarification decisions with the legally authorized evaluation committee or counsel.

Risk: The skill depends on provided bidder facts, procurement-file clauses, and optional knowledge-base access; missing or failed retrieval can make conclusions under-supported.

Mitigation: Require concrete bidder-response facts and procurement-file clauses before deciding, disclose retrieval gaps, avoid invented authorities or cases, and mark unsupported conclusions for human review.

## Reference(s):

- [Decision Framework](references/decision_framework.md)
- [Discipline Redlines](references/discipline_redlines.md)
- [Knowledge Base Mounting](references/kb_mounting.md)
- [Rejection Wording Templates](references/rejection_wording_templates.md)
- [ClawHub Skill Page](https://clawhub.ai/chesaram/skills/gp-rejection-decision-support)
- [Publisher Profile](https://clawhub.ai/user/chesaram)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown decision-support memorandum with cited clauses, risk assessment, and report-ready wording templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and should preserve source citations, uncertainty notes, and final decision authority for the evaluation committee.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, manifest.yaml, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
