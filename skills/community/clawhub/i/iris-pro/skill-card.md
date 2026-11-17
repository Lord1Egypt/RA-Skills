## Description:

Iris Pro reads Gmail inbox messages, scores urgency and sender importance, drafts personalised replies for actionable messages, generates weekly inbox analytics, and produces a priority action plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Gmail accounts use this skill to triage recent inbox messages, classify email categories, draft reply templates, and save inbox reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Gmail app password and accesses Gmail inbox contents.

Mitigation: Use it only after reviewing the access requirements, and revoke the Gmail app password when finished.

Risk: Message subjects, senders, classifications, and generated reply drafts are saved as local files.

Mitigation: Run it in a private directory outside synced or version-controlled folders, and protect or delete generated reports after use.

Risk: The install command uses an unsafe package installation option.

Mitigation: Run the skill in an isolated Python environment and review installation commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/iris-pro)
- [Skill homepage](https://clawhub.ai/occupythemilkyway/iris-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Console text plus generated Markdown and JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local inbox reports and draft reply text based on Gmail message metadata and snippets.]

## Skill Version(s):

1.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
