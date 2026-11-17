## Description:

Curates marketing claim and offer records, including exact wording, evidence, disclosures, terms, review dates, and live offer status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, growth, and compliance teams use this skill to register, update, expire, and query approved claims or offers with evidence provenance, disclosures, terms, and review dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Canonical claim or offer state could change if write authority is granted without review.

Mitigation: Grant write authority only when canonical marketing state should change, require explicit permission, and review evidence before accepting proposals.

Risk: Unsupported or overbroad marketing claims could be recorded if evidence scope is not checked.

Mitigation: Keep missing proof as none-on-file or unresolved, approve narrower wording when evidence is limited, and avoid treating proposal state as approved wording.

## Reference(s):

- [Claims Projection Contract](artifact/references/claims-ledger-schema.md)
- [Offer Claims Registry on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/offer-claims-registry)
- [Publisher Profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with structured claim or offer registry guidance and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return NEEDS_INPUT when no exact claim or offer statement is supplied; canonical writes require explicit authority.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
