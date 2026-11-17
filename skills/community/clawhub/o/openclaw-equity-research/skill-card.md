## Description:

OpenClaw Equity Research helps agents draft and review public-equity research artifacts with fresh sources, explicit assumptions, citations, and human-review guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to create first-pass equity research notes, earnings previews, model-update summaries, sector overviews, catalyst calendars, thesis trackers, and idea screens for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial facts, prices, estimates, filings, news, and calendar events may be stale, missing, delayed, or provider-dependent.

Mitigation: Verify sources, timestamps, currencies, fiscal periods, and assumptions against fresh primary sources or approved market-data providers before relying on outputs.

Risk: Research artifacts could be mistaken for investment, trading, legal, tax, accounting, or compliance advice.

Mitigation: Treat outputs as draft analyst work product, preserve the human-review note, and obtain appropriate professional or compliance review before decisions or external distribution.

Risk: The included ticker-report script can fetch data from configured providers and create local research files.

Mitigation: Run it only in an approved workspace, review output paths, and inspect generated Markdown or JSON before sharing.

## Reference(s):

- [OpenClaw Equity Research on ClawHub](https://clawhub.ai/x-rayluan/skills/openclaw-equity-research)
- [Research workflows](references/workflows.md)
- [Research standard](references/research-standard.md)
- [Research framework](references/research-framework.md)
- [Data sources](references/data-sources.md)
- [Report rubric](references/report-rubric.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown research artifacts, JSON ticker snapshots, shell commands, configuration snippets, and concise guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft analyst work product requiring source, timestamp, assumption, and human review before external use.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
