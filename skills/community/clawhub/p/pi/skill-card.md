## Description:

People Investigation guides an agent through public-records and OSINT research on a target person, including identity anchors, court records, property records, corporate filings, social media, and a structured dossier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tag-assistant](https://clawhub.ai/user/tag-assistant)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to organize people-search investigations across public records, web OSINT, court systems, property records, business filings, social media, and donation records. The expected result is a structured investigation report with source links, confidence notes, and caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can compile sensitive personal dossiers from people-search sources.

Mitigation: Use only with explicit consent and a lawful, non-harassing purpose; avoid returning home addresses, personal contact details, children, unrelated relatives, or financial proxies unless strictly necessary and authorized.

Risk: The artifact instructs agents to search private local archives, messages, payments, call logs, and memory.

Mitigation: Disable or remove private-local-source searches unless the user has clear authority over the data and the target has consented where required.

Risk: People-search aggregators and public-records snippets can mix identities and cause misattribution.

Mitigation: Verify findings against identity anchors, mark uncertainty clearly, and document disambiguation notes instead of presenting unverified leads as facts.

Risk: Investigation reports may be misused for stalking, harassment, or regulated background-check decisions.

Mitigation: Do not use the skill for harassment or FCRA-covered decisions such as employment, credit, housing, insurance, or tenant screening.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tag-assistant/skills/pi)
- [People Search & OSINT Resources](references/osint-resources.md)
- [Florida Court Systems - Quick Reference](references/court-systems.md)
- [FEC Individual Contributions](https://www.fec.gov/data/receipts/individual-contributions/)
- [CourtListener](https://www.courtlistener.com/)
- [PACER Case Locator](https://pcl.uscourts.gov/pcl/)
- [Florida Sunbiz Officer Search](https://search.sunbiz.org/Inquiry/CorporationSearch/SearchByOfficerRA)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown dossier with linked source references, confidence notes, caveats, and optional shell command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contain sensitive personal information; outputs should avoid unnecessary contact details, home addresses, family details, and other sensitive identifiers unless authorized and strictly necessary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
