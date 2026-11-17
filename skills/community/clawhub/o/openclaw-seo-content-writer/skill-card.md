## Description:

Writes and ships SEO blog posts through a Tony + Peter workflow covering drafting, publish QA, deployment verification, and Google Search Console indexing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and SEO teams use this skill to run a repeatable blog production lane from brief and draft creation through QA, deployment verification, and Google Search Console follow-through.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can ask an agent to publish content, trigger production deployments, and submit URLs to Google Search Console.

Mitigation: Install it only for sites where those actions are intended, configure credentials with least privilege, and require explicit confirmation before source publishing, deployment, or GSC submission when needed.

Risk: SEO drafts can be thin, weakly sourced, or treated as publish-ready before operational checks are complete.

Mitigation: Use the documented preflight, content-quality audit, recovery research step, and required receipts before source publishing or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/openclaw-seo-content-writer)
- [Tony pipeline](references/tony-pipeline.md)
- [Peter closeout](references/peter-closeout.md)
- [GSC indexing](references/gsc-indexing.md)
- [Receipt contracts](references/receipt-contracts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, receipts, and command or configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational receipts for preflight, quality audit, source publish, deployment, indexability, GSC submission, and indexing status when the agent follows the workflow.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
