## Description:

Classifies, scores, prioritizes, and batches agent notifications, with persistent per-source rules that can silently drop ignored notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to reduce notification noise by classifying messages as urgent, batched, or ignored, managing per-source rules, and producing digest-style summaries for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic first-use rules can permanently change how future notifications from a source are handled, including silently ignoring important messages.

Mitigation: Use --force for test classifications, avoid auto-rules for security, billing, monitoring, or deadline sources, and regularly review rules.json.

Risk: Ignored notifications are silently dropped at runtime and only retained in dropped.json for later audit.

Mitigation: Review dropped.json regularly and periodically re-evaluate any source configured with the ignore level.

Risk: The security evidence warns not to rely on --dir until an implementation mismatch is fixed.

Mitigation: Keep the default data directory private and avoid depending on --dir for isolation until the release evidence no longer flags that mismatch.

## Reference(s):

- [Notification Triage ClawHub Release](https://clawhub.ai/jlacroix82/skills/notification-triage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI text output with inline shell commands and JSON-backed local state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces notification classifications, pending batch views, rule listings, status summaries, and digests; local state is stored in JSON files under memory/notification-triage unless configured otherwise.]

## Skill Version(s):

1.1.3 (source: SKILL.md frontmatter, clawhub.yaml, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
