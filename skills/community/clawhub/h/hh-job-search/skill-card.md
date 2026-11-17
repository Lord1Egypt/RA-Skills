## Description:

Search, evaluate, and manage job opportunities for a candidate across the Russian market with hh.ru, Habr Career, Telegram vacancy channels/chats, and LinkedIn as a secondary source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naxofon](https://clawhub.ai/user/naxofon)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers and their agents use this skill to build a factual candidate profile, search supported job sources, score and deduplicate vacancies, maintain an application pipeline, and draft tailored application materials. Application submission, resume raising, and recruiter outreach are limited to modes that require explicit user approval.

### Deployment Geography for Use:

Global; source coverage is primarily oriented to the Russian job market.

## Known Risks and Mitigations:

Risk: Authenticated hh.ru browser automation can operate on the wrong tab or unsafe URL inputs.

Mitigation: Use a dedicated browser profile logged into only the intended hh.ru account, attach Browser Relay to the intended tab, and review URLs before any batch apply workflow.

Risk: Auto-apply and recruiter outreach can create external actions on the user's behalf.

Mitigation: Keep auto-apply and outreach disabled unless explicitly requested, restrict submissions to strong matches, and log every application or outbound message.

Risk: CSV exports may be unsafe when opened directly in spreadsheet software.

Mitigation: Treat generated CSV exports as untrusted and review them before opening or sharing.

## Reference(s):

- [Onboarding](references/onboarding.md)
- [Source strategy](references/source-strategy.md)
- [Safety rules](references/safety-rules.md)
- [Project layout](references/project-layout.md)
- [Data flow](references/data-flow.md)
- [File formats](references/file-formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, local project files, JSON/JSONL vacancy data, CSV shortlists, and tailored resume or cover-letter drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces durable workspace artifacts for profiles, search rules, sources, pipelines, logs, exports, and application materials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
