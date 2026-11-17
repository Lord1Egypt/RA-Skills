## Description:

Create source-grounded weekly HRBP decision briefs for accountable human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mwclaw](https://clawhub.ai/user/mwclaw)

### License/Terms of Use:

MIT-0

## Use Case:

HR business partners and accountable reviewers use this skill to turn approved weekly HR source packets into source-grounded draft decision briefs for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved-source packets may contain unnecessary personal or sensitive HR data.

Mitigation: Use synthetic, de-identified, or explicitly approved source packets and stop when unnecessary personal data, credentials, medical details, government identifiers, home addresses, or unrelated sensitive information appears.

Risk: A draft brief could be mistaken for an employment decision or official HR communication.

Mitigation: Keep every output marked for human review; do not make employment decisions, send communications, update HR systems, or take external action without separate human authorization.

Risk: Unsupported claims, hidden missing facts, or conflated law, policy, and practice could mislead reviewers.

Mitigation: Cite supplied source labels for material claims, list missing or conflicting facts, separate law or regulation, written policy, and operating practice, and perform independent source comparison before human disposition.

## Reference(s):

- [Evaluation Cases](references/evals.md)
- [Weekly Decision Brief Template](templates/weekly-decision-brief.md)
- [ClawHub Skill Page](https://clawhub.ai/mwclaw/skills/hrbp-weekly-decision-brief)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown draft brief with verifier findings and receipt fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft remains marked for human review; structural checker pass does not validate source support.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
