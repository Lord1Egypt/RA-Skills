## Description:

Scrapes Google and related review sources for businesses, detects review language about missed calls or poor phone coverage, and scores lead quality for AI receptionist outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayjjimenez](https://clawhub.ai/user/jayjjimenez)

### License/Terms of Use:


## Use Case:

Sales and operations users can analyze business review text for signs that customers could not reach staff by phone. The skill helps prioritize outreach by returning matched pain phrases, snippets, and a 0-10 pain score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional save mode appends automatically generated HOT lead rows to a local Master Lead List without a confirmation prompt or rollback.

Mitigation: Use save mode only when that write is intended, and back up the lead list before running it.

Risk: The skill scrapes third-party review sites and reads a local lead list.

Mitigation: Install and run it only in environments where that scraping and local data access are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jayjjimenez/skills/google-reviews-pain-detector)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples; detector output as terminal text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally append HOT lead rows to a local Markdown lead list when save mode is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
