## Description:

Execute queries to Grok AI via Playwright browser automation without requiring an X API KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aquarius-wing](https://clawhub.ai/user/aquarius-wing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send prompts to Grok through a logged-in X browser session and return the captured answer. It is intended for users who want Grok responses without using an X API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates a logged-in X/Grok browser session and stores reusable account data locally.

Mitigation: Use only on a machine where storing an X/Grok session is acceptable, keep session/ private, exclude it from shared folders and backups, and remove it when no longer needed.

Risk: The scraper can perform unattended account activity, especially when scheduled through cron.

Mitigation: Avoid scheduled execution unless the user accepts unattended X/Grok account activity and review output/run.log and output/notify-login-expired regularly.

Risk: Some scripts launch Chromium with --no-sandbox.

Mitigation: Prefer a dedicated OS account or container and remove the --no-sandbox flag where the host environment supports sandboxed Chromium.

Risk: X/Grok DOM changes can break scraping or produce empty, partial, or UI-contaminated output.

Mitigation: Review output/latest.md before relying on results and use the bundled inspect and selector-fix workflow when extraction fails.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aquarius-wing/skills/grok-scraper)
- [Grok Web App](https://x.com/i/grok)
- [DOM Selector Fix Guide](dom-selector-fix.md)
- [DOM Selector Fragility Notes](learn/dom-selector-fragility.md)
- [Record Mode Empty Output Notes](learn/record-mode-empty-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files and terminal status output; optional WebM recording when record mode is enabled]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the latest captured Grok response to output/latest.md and timestamped markdown files under output/.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
