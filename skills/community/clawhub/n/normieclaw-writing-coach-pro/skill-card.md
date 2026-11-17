## Description:

Analyzes and improves writing by checking grammar, style, tone, readability, and consistency while adapting to the user's saved writing preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, professionals, and agent users use this skill to proofread, rewrite, and coach submitted text across emails, resumes, blog posts, reports, and other prose. It can produce quick grammar checks, full writing analysis, rewrite options, coaching explanations, profile updates, and progress reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted writing may be processed by the user's configured LLM backend, including cloud-hosted providers.

Mitigation: Review the selected LLM provider's data handling terms before using confidential text, or use a local model when text must remain on the user's machine.

Risk: Writing-derived profile, learning, session, report, and dashboard data may be retained or synced when the dashboard is present.

Mitigation: Review local data and dashboard settings before installation, disable learning or dashboard sync when the host supports it, and protect or delete stored data as personal information.

Risk: The documented reset flow permanently deletes stored Writing Coach Pro data.

Mitigation: Export needed reports or back up the data directory before running reset or deletion commands.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nollio/skills/normieclaw-writing-coach-pro)
- [Security information](SECURITY.md)
- [Setup guide](SETUP-PROMPT.md)
- [Dashboard integration spec](dashboard-kit/DASHBOARD-SPEC.md)
- [NormieClaw support](https://normieclaw.ai/support)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with issue lists, readability metrics, rewritten text, coaching explanations, profile settings, and optional markdown or PDF progress reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store local style profiles, learning logs, session summaries, exported reports, and optional dashboard records when enabled.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
