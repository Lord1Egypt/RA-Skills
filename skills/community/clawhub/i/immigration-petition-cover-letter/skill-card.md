## Description:

Use this skill when a licensed immigration attorney, BIA-accredited representative, or supervising paralegal needs to draft a USCIS petition or application cover letter for I-129, I-140 (EB-1A/EB-1B/EB-1C/EB-2 NIW), I-485, I-589, I-918/I-914, or N-400 filings; it maps exhibits to eligibility criteria, flags missing evidence, computes filing fees, and produces a draft cover-letter packet for attorney-of-record review and signature before filing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Immigration attorneys, BIA-accredited representatives, in-house immigration counsel, and supervised paralegals use this skill to prepare draft USCIS petition or application cover-letter packets. It helps structure eligibility criteria, exhibit mapping, filing logistics, fee worksheets, unresolved-information lists, and attorney-review self-checks before filing.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill may process sensitive immigration, identity, criminal-history, medical, asylum, trafficking, or victim-related facts.

Mitigation: Use it only in an appropriate legal-support workflow, minimize sensitive narrative detail, keep full identifiers in structured fields rather than narrative text, and apply the user's confidentiality controls.

Risk: Draft outputs could be mistaken for legal advice or a final filing-ready work product.

Mitigation: Keep every output labeled as a draft, require attorney-of-record review and signature, and do not let the agent file, sign forms, speak to agencies, or substitute for counsel.

Risk: USCIS fees, form editions, and filing addresses can change.

Mitigation: Require independent verification against current USCIS sources before filing, and mark unknown current fees or filing channels for verification instead of inventing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/immigration-petition-cover-letter)
- [Open-Skill-Hub issues](https://github.com/archlab-space/Open-Skill-Hub/issues)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft packet with structured sections, checklists, tables, and self-check output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs must remain draft-only, avoid unauthorized legal advice, protect sensitive identifiers, and require attorney-of-record review and signature before filing.]

## Skill Version(s):

0.1.1 (source: server release evidence and CHANGELOG, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
