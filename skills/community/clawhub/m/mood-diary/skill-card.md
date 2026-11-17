## Description:

Mood Diary helps agents record Chinese natural-language mood journal entries, identify seven emotion types, assign 1-10 scores, extract tags, and generate daily, weekly, monthly, and trend reports from local JSON data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyby99-gif](https://clawhub.ai/user/dyby99-gif)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to keep a private local mood diary, summarize recent emotional patterns, and generate human-readable or JSON reports for reflection. It is intended for personal tracking and does not replace professional health care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mood and journal entries are sensitive personal data stored in a local JSON file.

Mitigation: Install only if local storage under ~/.openclaw/workspace/data/journal is acceptable, restrict access to the user account, and treat generated reports or JSON output as private.

Risk: The delete command removes entries without an undo flow.

Mitigation: Back up entries.json before deleting or editing important journal records.

Risk: Mood scoring and generated suggestions may be incomplete or misleading for mental health decisions.

Mitigation: Use reports for personal reflection only and seek professional help when low mood, anxiety, or other concerns persist.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dyby99-gif/skills/mood-diary)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Command-line text and optional JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local journal data to ~/.openclaw/workspace/data/journal/entries.json and can render calendar, summary, daily, weekly, monthly, and trend views.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
