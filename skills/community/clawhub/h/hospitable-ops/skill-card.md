## Description:

Operate, debug, and automate Hospitable through its Public API using a read-first workflow, safe write verification, and non-price calendar controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangwill2023](https://clawhub.ai/user/jiangwill2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Hospitable properties, reservations, and calendars, verify API behavior, and apply controlled non-price calendar operations such as blocks or check-in/check-out restrictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Hospitable token could be sent to an unintended host if the base URL is overridden.

Mitigation: Use a tightly scoped Hospitable token and set HOSPITABLE_BASE_URL only when the destination is fully trusted.

Risk: The write probe can perform broader raw API writes than the documented calendar-only safety posture.

Mitigation: Review write requests before execution, limit direct use to confirmed non-price calendar operations, and verify effects with delayed readback.

## Reference(s):

- [Hospitable Public API v2 endpoint](https://public.api.hospitable.com/v2/)
- [Hospitable Ops ClawHub page](https://clawhub.ai/jiangwill2023/skills/hospitable-ops)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports current status, tested object and date, accepted or rejected request, delayed readback, operational conclusion, and the largest remaining gap.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
