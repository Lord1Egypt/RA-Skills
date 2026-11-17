## Description:

Noise Nuisance Log helps users document recurring residential or commercial noise incidents, analyze quiet-hours patterns and impacts, export records, and generate factual complaint letters for landlords, HOAs, or city noise offices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users, tenants, condo owners, landlords, and residents use this skill to keep contemporaneous noise-dispute records, summarize patterns, and prepare calm complaint letters for landlords, HOAs, mediation, or municipal noise offices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Noise-dispute records may contain private household details, names, addresses, phone numbers, or sensitive allegations.

Mitigation: Keep the local log file and exports out of shared or synced folders, and avoid adding personal details unless they are necessary.

Risk: Generated complaint letters may include placeholders, sensitive details, or statements that should not be sent without review.

Mitigation: Review and edit each letter before sending, keeping the language factual and limited to documented incidents.

Risk: Default quiet-hours assumptions may not match the user's local ordinance.

Mitigation: Check local rules and set the night-hours options to match the applicable ordinance before relying on violation flags.

## Reference(s):

- [Noise Ordinances, Evidence, and Escalation](references/ordinances-and-evidence.md)
- [ClawHub Skill Page](https://clawhub.ai/voronindenis5/skills/noise-nuisance-log)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, local JSON records, CSV exports, statistics, histograms, and plain-text complaint letters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores incident records locally by default in ~/.noise-log.json and can write CSV exports and complaint-letter text files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
