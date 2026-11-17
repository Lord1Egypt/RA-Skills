## Description:

Generates personal health reports from local health records, including scoring, Markdown-style summaries, PDF export, and optional multi-channel webhook delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tankeito](https://clawhub.ai/user/tankeito)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal health-tracking agents use this skill to configure a health profile, read daily health notes, calculate diet, hydration, weight, symptom, and exercise scores, and generate ongoing wellness reports. The skill is intended for personal reporting workflows rather than clinical decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health details and generated reports may leave the machine when webhooks or public report URLs are configured.

Mitigation: Keep webhooks and public report hosting disabled unless needed, use only trusted official provider URLs, and inform users before enabling outbound report delivery.

Risk: The daily automation wrapper can run on a schedule and process private health files without interactive review.

Mitigation: Review or fix the daily shell wrapper before installation, run cron jobs under a dedicated non-root account, and limit file permissions to the required health record directory.

Risk: Webhook tokens, API keys, local health notes, logs, and generated PDF reports can expose personal data if configuration or output directories are readable by others.

Mitigation: Protect config/.env, MEMORY_DIR, logs, REPORT_WEB_DIR, and generated reports with restrictive permissions and rotate webhook tokens periodically.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tankeito/skills/openclaw-skill-health-report)
- [Project Homepage](https://github.com/tankeito/openclaw-skill-health-report)
- [Issue Tracker](https://github.com/tankeito/openclaw-skill-health-report/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown health report text, generated PDF files, JSON configuration, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local Markdown health records and optional environment variables; can publish report text and PDF links through configured webhooks.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact SKILL.md, README.md, and _meta.json show 1.0.9)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
