## Description:

Builds a US law firm intake packet with conflict check fields, fee and trust terms, and the limits notice that keeps intake from becoming advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US solo attorneys, intake paralegals, and small-firm administrators use the skill to draft a client intake packet, including conflict-check fields, fee and trust terms, data-handling guidance, and a limits notice. An attorney should review the packet against the applicable state's rules before use.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Client names, contact details, and matter information are sensitive and could be exposed if handled outside firm safeguards.

Mitigation: Keep client information within firm-approved systems and follow the firm's confidentiality, retention, and secure-communication rules. Do not include full Social Security numbers in the intake form.

Risk: Trust-account, conflicts, confidentiality, and intake requirements vary by state, and the packet could be mistaken for legal advice or a compliance determination.

Mitigation: Have an attorney review the packet against the applicable jurisdiction's rules; do not treat the intake or a clean lint report as legal advice or proof of compliance.

## Reference(s):

- [Law firm intake rules](artifact/references/law-firm-intake-rules.md)
- [Publisher homepage](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown intake packet sections and a YAML intake-field brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a Markdown lint report; the checker does not establish legal compliance.]

## Skill Version(s):

1.0.7 (source: SKILL.md frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
