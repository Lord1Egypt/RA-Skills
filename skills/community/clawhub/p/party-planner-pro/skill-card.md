## Description:

Party Planner Pro helps an agent plan, manage, and track events through guest lists, budgets, menus, timelines, vendors, day-of logistics, and post-party wrap-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal event hosts use this skill to organize parties and gatherings from initial setup through wrap-up. It supports event planning tasks such as RSVP tracking, dietary accommodation, budget reporting, vendor coordination, menu planning, checklists, and day-of schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional PNG budget report path can render untrusted event data as active HTML, creating privacy and integrity risk.

Mitigation: Avoid PNG budget reports for untrusted event data until text is HTML-escaped, JavaScript is disabled, and network requests are blocked during rendering.

Risk: Guest, vendor, and budget imports can contain sensitive personal or financial information.

Mitigation: Review imported data before use, treat it as untrusted content, and store event data only in locations appropriate for the user's privacy needs.

Risk: The documented uninstall command removes the skill directory and local event data.

Mitigation: Back up event data before uninstalling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/party-planner-pro)
- [README](artifact/README.md)
- [Security audit](artifact/CODEX-SECURITY-AUDIT.md)
- [Security notes](artifact/SECURITY.md)
- [Dashboard companion specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational guidance, JSON event records, Markdown reports, optional PNG budget reports, and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local event data files and reports; optional PNG budget reports require Playwright.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
