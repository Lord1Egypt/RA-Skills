## Description:

lifelog2 records short diary fragments, stores daily drafts locally, summarizes entries without rewriting them, and archives reviewed summaries to flomo and ima when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanmengli777](https://clawhub.ai/user/quanmengli777)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to capture daily thoughts, moods, and events as timestamped diary fragments, review a same-day markdown summary, and archive the approved summary to flomo and ima.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diary entries are saved in local draft files and may contain sensitive personal information.

Mitigation: Install only if local draft storage is acceptable, and avoid recording secrets or highly sensitive details unless that storage location is appropriate.

Risk: The archive command sends reviewed diary content to flomo and ima.

Mitigation: Review the generated summary before archiving, and archive only when both destinations are acceptable for the content.

Risk: Local draft cleanup occurs after both archive destinations report success.

Mitigation: If either archive step fails, keep the draft file and tell the user what failed so the content can be retried or handled manually.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quanmengli777/skills/lifelog2)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown diary entries and concise status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the user's original diary text and uses local daily draft files before user-directed archival.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
