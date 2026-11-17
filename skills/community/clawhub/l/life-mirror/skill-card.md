## Description:

Life-Mirror is a personal life-awareness assistant for relationship reflection, emotional support, growth decisions, task follow-up, scheduled reports, and proactive care using role-based coaching, persistent memory, and user-authorized platform signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lldfjq](https://clawhub.ai/user/lldfjq)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill as a personal coaching and life-reflection assistant that remembers preferences, analyzes authorized personal signals, helps reason about relationships and decisions, manages reminders, and produces recurring life reports. It is suited to ongoing personal support rather than one-off factual Q&A.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad platform access and builds a persistent personal profile.

Mitigation: Authorize only the platforms needed for the intended use case, avoid granting broad browser or account access, and review the local storage directory regularly.

Risk: The skill stores personal history, inferred preferences, todos, and platform synchronization state over time.

Mitigation: Do not store passwords, payment details, ID numbers, private chat exports, diary entries, or other sensitive records unless there is a deliberate local-storage policy.

Risk: The skill can add recurring background tasks and send proactive messages to bound communication channels.

Mitigation: Disable automatic scheduled jobs unless explicitly needed, verify cron jobs after installation, and keep push frequency and quiet-hour settings under user control.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lldfjq/skills/life-mirror)
- [README](artifact/README.md)
- [Execution Guide](artifact/core/execution-guide.md)
- [Profile Sync Workflow](artifact/workflows/profile-sync.md)
- [Scheduling Workflow](artifact/workflows/scheduling.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Conversational text and Markdown, with JSON-style scheduling and configuration snippets when tasks are configured.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local profile, memory, todo, and platform sync state files when configured by the user.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
