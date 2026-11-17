## Description:

Tracks job applications in a local markdown file, flags follow-ups, and helps draft outreach, prepare for interviews, recommend resume variants, and analyze offers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris](https://clawhub.ai/user/chris)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to maintain a local job-search tracker, monitor stalled applications, prepare for interviews, and draft job-search communications with optional Gmail, LinkedIn, browser, and web-search context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tracker may contain sensitive job-search history, recruiter contacts, salary ranges, and offer details.

Mitigation: Install only if comfortable keeping that data in a local tracker, and store the tracker in a user-controlled working directory.

Risk: Optional Gmail, LinkedIn, browser, and web-search workflows may access private account data or external pages through connected tools.

Mitigation: Use tracker-only mode by leaving Gmail or LinkedIn tools disconnected unless needed, and review connected-tool permissions before enabling them.

Risk: Externally discovered applications or follow-ups could be logged incorrectly without user review.

Mitigation: Require explicit confirmation before writing externally discovered items or follow-up logs to the tracker.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chris/skills/job-search-tracker)
- [Publisher profile](https://clawhub.ai/user/chris)
- [README](artifact/README.md)
- [CHANGELOG](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown tracker updates, dashboard summaries, email and cover-letter drafts, interview prep briefs, and negotiation guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local tracker, resume, draft, and dashboard files in the current working directory when appropriate.]

## Skill Version(s):

1.1.2 (source: frontmatter, changelog released 2026-06-08, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
