## Description:

Decode a residential lease into plain English and rank the clauses that can hurt you.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review residential lease text before signing or negotiating. It produces a plain-language clause decode, ranked red flags, exit and deposit math, questions for the landlord, and negotiable items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the lease review as legal or financial advice.

Mitigation: Present the output as plain-language lease-reading guidance and direct users to confirm jurisdiction-specific or high-dollar issues with a tenant organization or qualified professional.

Risk: Lease text may contain personal identifiers or sensitive rental details.

Mitigation: Ask users to avoid sharing unnecessary personal identifiers and work from redacted lease excerpts when possible.

Risk: Jurisdiction-dependent clauses may be misread as universally enforceable or unenforceable.

Mitigation: Flag jurisdiction-dependent points clearly and avoid declaring clauses void as universal fact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/lease-decoder)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/lease-decoder.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with a verdict, decode table, ranked red flags, calculations, questions, negotiable items, and disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires lease text and, when absent from the lease, rent, deposit, term, and rough location.]

## Skill Version(s):

50.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
