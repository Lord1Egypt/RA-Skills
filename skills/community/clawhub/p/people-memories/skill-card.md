## Description:

Capture short personal notes about people you mention, store them in a lightweight local database, and recall those details later.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charbeld](https://clawhub.ai/user/charbeld)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to save, search, summarize, export, and recall personal notes about people, including preferences, reminders, context, birthdays, and anniversaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice-triggered remember phrases can create persistent records about identifiable people without an explicit confirmation step.

Mitigation: Disable voice auto-capture or require confirmation before saving voice-derived notes.

Risk: Stored notes, exports, and logs may contain sensitive personal details in plaintext.

Mitigation: Treat the local database and exported files as sensitive, apply restrictive file permissions, redact logs, and avoid storing private details without consent.

Risk: The skill does not present built-in deletion, retention, or review controls for saved personal notes.

Mitigation: Add retention and deletion workflows, and periodically review saved records for consent, accuracy, and continued need.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [CLI text responses, Markdown or JSON exports, and local JSON records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists notes locally and can write export files when requested.]

## Skill Version(s):

0.1.0 (source: server release metadata and clawdbot.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
