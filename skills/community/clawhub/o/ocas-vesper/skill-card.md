## Description:

Vesper generates concise morning, evening, and on-demand briefings from calendar, message, portfolio, decision, and cross-skill signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Vesper to assemble personal daily briefings, surface upcoming decisions, and summarize actionable signals without exposing internal analysis details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring briefing and update jobs can run automatically after installation.

Mitigation: Review scheduled tasks before enabling the skill, and disable or adjust cron jobs that are not wanted.

Risk: The skill aggregates personal and cross-skill data into persistent briefing records and journals.

Mitigation: Confirm the configured read and write paths, retention settings, and journal handling match the deployment's privacy requirements.

Risk: The automatic update path can replace local skill files from GitHub.

Mitigation: Prefer manual reviewed updates from signed or pinned releases, or disable the update cron job.

Risk: Manifest permissions and documented cross-skill reads may need alignment before installation.

Mitigation: Review installation permissions against the actual cross-skill data paths and narrow them where possible.

## Reference(s):

- [Vesper Briefing Templates](references/briefing_templates.md)
- [Vesper Schemas](references/schemas.md)
- [Vesper Signal Filtering](references/signal_filtering.md)
- [Journal](references/journal.md)
- [ClawHub Skill Page](https://clawhub.ai/indigokarasu/skills/ocas-vesper)

## Skill Output:

**Output Type(s):** [Text, HTML, JSON, Configuration, Shell commands, Guidance]

**Output Format:** [Plain text or minimal HTML briefings with JSON and JSONL records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes briefing files, run journals, evaluated signal records, presented decision records, and default scheduling configuration.]

## Skill Version(s):

2.7.0 (source: skill.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
