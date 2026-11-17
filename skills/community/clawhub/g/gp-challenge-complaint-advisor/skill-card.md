## Description:

GP Challenge & Complaint Advisor helps suppliers and potential suppliers in Chinese government procurement matters retrieve similar complaint cases, review draft complaints, and generate complaint-letter templates using the available IMA knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External suppliers and potential suppliers use this skill to analyze Chinese government procurement challenge or complaint scenarios, check whether draft complaints contain common procedural or evidentiary issues, and prepare structured complaint templates.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated complaint documents may contain unwanted third-party signature or attribution.

Mitigation: Review generated documents before use and remove any unwanted signature or attribution.

Risk: Legal-style analysis may be mistaken for legal advice or a guaranteed complaint outcome.

Mitigation: Treat outputs as drafting and case-retrieval assistance only; consult qualified legal counsel for advice and final decisions.

Risk: Case summaries, legal provisions, or complaint statistics may be misleading if not grounded in retrieved sources.

Mitigation: Require case citations with media_id or source links, qualify frequency counts as based only on the current retrieval set, and verify current legal provisions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/gp-challenge-complaint-advisor)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown reports, draft-review findings, and complaint-letter templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should cite retrieved case sources with media_id or source links, preserve placeholders for unknown complaint facts, and state that generated analysis is not legal advice.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact manifest reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
