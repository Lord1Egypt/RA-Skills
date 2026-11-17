## Description:

QA remediation auto-fix pipeline for Monet Works content that detects and repairs banned phrases, missing disclaimers, missing CTAs, and excessive length, then outputs fixed content and a structured change report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, developers, and content operators use this skill to remediate financial-content QA findings before publication. It is designed to produce edited content plus an auditable JSON report while leaving tone, strategy, factual accuracy, NDA, and legal compliance questions for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic edits may introduce unsuitable financial or brand-sensitive wording before publication.

Mitigation: Review the fixed content and JSON change report before scheduling or publishing.

Risk: Default CTA and disclaimer templates may not match an organization's legal, compliance, or brand requirements.

Mitigation: Customize the CTA and disclaimer templates before production use.

Risk: The artifact guidance includes an unnecessary unpinned LLM package install.

Mitigation: Skip that install unless the implementation is updated to require it, or pin and review dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/skills/monet-works-content-qa-dv)
- [Publisher profile](https://clawhub.ai/user/clawdiri-ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Fixed content on stdout with a structured JSON change report on stderr or output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes distinguish fully remediated content, partial remediation that needs human review, and execution errors.]

## Skill Version(s):

0.1.0 (source: server release metadata, created 2026-03-22; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
