## Description:

Analyze iMessage on macOS and Signal conversation history to summarize message volume, initiation patterns, silence gaps, tone samples, and recent exchanges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terellison](https://clawhub.ai/user/terellison)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to analyze local or exported message histories and produce conversational relationship reports. It is intended for cases where the user has clear permission to inspect the selected message history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private message histories and may expose conversations or contact details beyond the user's intended scope.

Mitigation: Run it only on message histories the user has clear permission to analyze, prefer user-exported Signal data, and use exact phone numbers or handles rather than broad searches.

Risk: iMessage analysis may require broad local file access on macOS.

Mitigation: Avoid granting Full Disk Access to a general terminal or Python interpreter unless necessary, and revoke that permission immediately after the analysis.

Risk: Terminal output can contain sensitive message content and relationship inferences.

Mitigation: Treat generated output as private, minimize copied excerpts, and confirm contextual gaps with the user before drawing conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terellison/skills/imessage-signal-analyzer)
- [signal-cli](https://github.com/AsamK/signal-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style narrative report with terminal output summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries may include private message excerpts, contact identifiers, date ranges, volume counts, initiation estimates, silence gaps, and recent-message samples.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
