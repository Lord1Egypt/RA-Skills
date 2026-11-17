## Description:

Gmail Labeler helps agents triage Gmail inboxes with gog, configurable labels, safe archiving, urgent-route notifications, multilingual rules, and an optional lightweight LLM review layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipematos](https://clawhub.ai/user/felipematos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to build or run Gmail automation that separates actionable from non-actionable mail, applies labels, archives low-value messages, and keeps important replies, opportunities, and urgent billing items visible in Inbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private Gmail content and can read, label, and archive mailbox messages.

Mitigation: Start in dry-run mode, review planned actions and JSONL logs, and move to label-only or full-action mode only after confirming account scope and filtering behavior.

Risk: Selected email content can be sent to a configured LLM provider for ambiguity-band review.

Mitigation: Disable LLM review unless needed, choose an approved provider/model, keep body excerpts capped, and require the allowlisted category schema.

Risk: Incorrect classification could over-archive important mail or miss urgent billing and opportunity messages.

Mitigation: Use VIP and never-archive lists, review daily false positives and false negatives, and tune thresholds and local overlay filters before full-action use.

Risk: Decision logs may contain email metadata and classification details.

Mitigation: Store logs outside the skill source tree with restricted access and retain them only as long as needed; the default retention is 30 days.

Risk: The launcher obtains a keyring secret for non-interactive Gmail access.

Mitigation: Avoid the launcher until the keyring secret is scoped to the process that needs it and the local runtime environment is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/felipematos/skills/gmail-labeler)
- [Default configuration](references/default-config.json)
- [Configuration guide](references/config-guide.md)
- [Filter catalog](references/filter-catalog.md)
- [Implementation notes](references/implementation-notes.md)
- [Logging and review](references/logging-and-review.md)
- [LLM review layer](references/llm-review.md)
- [Cron example](references/cron-example.md)
- [AIN email review schema](references/ain-email-review.schema.json)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, Python runner code, shell command examples, JSONL logging guidance, and optional strict JSON LLM review outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run, label-only, and full-action modes; default logs are JSONL with 30-day retention.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
