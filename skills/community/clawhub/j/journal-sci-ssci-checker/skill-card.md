## Description:

Checks whether psychology academic journals are indexed by SCI or SSCI to support literature-quality screening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiaqi-guo-0114](https://clawhub.ai/user/jiaqi-guo-0114)

### License/Terms of Use:

MIT-0

## Use Case:

External users and research-support agents use this skill to check whether a named psychology journal appears in a bundled SCI/SSCI list before continuing paper-quality evaluation or corpus filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Journal-index results may be stale or incomplete because the skill is backed by a bundled local journal list.

Mitigation: Confirm important publication decisions against Web of Science or Journal Citation Reports, and update the journal list on the intended annual maintenance cycle.

Risk: The update script is currently a placeholder and is not evidence of a live Web of Science or JCR integration.

Mitigation: Review and test any future implementation that adds real API calls, scraping, credentials, or network fetching before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiaqi-guo-0114/skills/journal-sci-ssci-checker)
- [Web of Science Master Journal List](https://mjl.clarivate.com/)
- [Journal Citation Reports](https://jcr.clarivate.com/)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Markdown or JSON describing the matched journal, detected index category, and pass/fail result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a bundled journal list and fuzzy matching; preprint articles are skipped by the skill guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
