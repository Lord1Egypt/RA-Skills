## Description:

OfferCatcher turns recruiting emails into native Apple Reminders by using AI-powered parsing to extract interviews, assessments, deadlines, and related events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissoncx](https://clawhub.ai/user/nissoncx)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and OpenClaw users use this skill on macOS to scan recent recruiting email, extract interview, assessment, test, authorization, and deadline events, and create Apple Reminders that sync through iCloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented one-line install path fetches and executes a remote shell script.

Mitigation: Install through ClawHub or a pinned, verified release, and review installation commands before execution.

Risk: The skill needs Apple Mail access and can expose recruiting email subjects, senders, timestamps, and body snippets to the agent workflow.

Mitigation: Use a dedicated recruiting mailbox or account where possible, keep days and max_results small, and confirm whether the configured LLM processing is local or remote before scanning sensitive email.

Risk: Reminder-writing helpers can create, update, delete, or clear reminders when invoked with those commands.

Mitigation: Use dry-run for event application checks, avoid clear-list unless deletion is intended, and keep state output paths on trusted user-owned storage.

## Reference(s):

- [ClawHub OfferCatcher Release Page](https://clawhub.ai/nissoncx/skills/offercatcher)
- [OpenClaw Project](https://github.com/NissonCX/openclaw)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON event payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan mode returns recent Apple Mail messages as JSON with body text truncated to 2000 characters; apply mode creates Apple Reminders and emits a JSON sync summary.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
