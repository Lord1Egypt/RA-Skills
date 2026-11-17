## Description:

Helps users identify the proper court for PRC domestic civil litigation by analyzing case type, party residences, claim amount, relevant locations, jurisdiction agreements, exclusive jurisdiction, and special case rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuleff](https://clawhub.ai/user/xuleff)

### License/Terms of Use:

MIT-0

## Use Case:

Legal practitioners, litigants, and assistants use this skill to collect jurisdiction facts and reason through level, territorial, exclusive, and special-case court jurisdiction for civil cases in mainland China.

### Deployment Geography for Use:

Global; intended subject matter is PRC domestic civil litigation.

## Known Risks and Mitigations:

Risk: The skill can produce incorrect or outdated jurisdiction guidance because court rules and provincial thresholds may change.

Mitigation: Verify important conclusions against current court rules or a qualified lawyer before relying on them.

Risk: The skill may ask for sensitive case facts, including party residences, claim amounts, and dispute details.

Mitigation: Share only the facts needed for jurisdiction analysis and avoid unnecessary personal or confidential details.

Risk: Users may treat legal reference guidance as definitive legal advice.

Mitigation: Use the output as reference guidance and obtain professional review for consequential filing decisions.

## Reference(s):

- [Exclusive Jurisdiction](artifact/references/exclusive-jurisdiction.md)
- [Level Jurisdiction Rules](artifact/references/level-jurisdiction.md)
- [Provincial Jurisdiction Standards](artifact/references/provincial-standards.md)
- [Special Case Jurisdiction](artifact/references/special-cases.md)
- [Territorial Jurisdiction Rules](artifact/references/territorial-jurisdiction.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown or plain-text legal reference guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for case facts such as party residences, claim amounts, dispute type, locations, and jurisdiction clauses before proposing a court.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
