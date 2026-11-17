## Description:

This skill helps suppliers in mainland China government-procurement disputes classify complaint issues, compare similar complaint decisions, estimate evidence-conditioned success rates from real sample counts, and plan lawful evidence collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External suppliers and complainants use this skill to assess whether a mainland China government-procurement complaint is worth pursuing, what evidence gaps matter, and which lawful evidence-collection steps fit the complaint deadline. It is an analytical aid for complaint strategy, not a legal outcome guarantee.

### Deployment Geography for Use:

Mainland China government-procurement matters

## Known Risks and Mitigations:

Risk: Users may overread a statistical win-rate estimate as a promised legal outcome.

Mitigation: Require outputs to label class cases as historical references, include sample counts and confidence notes, and advise legal or professional review before filing.

Risk: Weak, incomplete, or unavailable case evidence can make complaint predictions misleading.

Mitigation: Use only successfully retrieved and labeled complaint decisions in denominators, mark unavailable sources as pending verification, and separate strong-evidence and weak-evidence rates.

Risk: Complaint prompts may include sensitive business or evidentiary material.

Mitigation: Ask only for necessary facts and advise users to avoid sharing unnecessary sensitive information.

Risk: Evidence collection could cross legal boundaries if a user requests forged facts, malicious complaints, or unlawful collection methods.

Mitigation: Refuse requests involving fabricated evidence, malicious filing, system intrusion, or covert collection, and recommend only lawful paths such as information requests, third-party testing, and public registry checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/gp-complaint-winrate)
- [README](README.md)
- [Complaint category taxonomy](references/complaint-category-taxonomy.md)
- [Win-rate methodology](references/winrate-methodology.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured tables, sample counts, confidence notes, and numbered evidence-collection steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Win-rate estimates must be tied to real sample counts, evidence-strength layers, and confidence statements; unavailable case evidence should be marked as unverified rather than used for statistics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
