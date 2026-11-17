## Description:

Extracts per-day nutrition from a user's Lose It! data export and returns calories, macros, fiber, meal details, and available budget and exercise figures as JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stozo04](https://clawhub.ai/user/stozo04)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to retrieve a user's daily Lose It! nutrition for summaries, tracking, or downstream analysis. It supports password-based login, a downloaded export ZIP, or a saved session cookie.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: config.json can contain the Lose It! email and password in plaintext.

Mitigation: On shared machines, prefer environment variables. Keep any config file owner-only, gitignored, and outside shared or backed-up directories.

Risk: The cached liauth token is a reusable session credential, and some referenced material was unavailable for review before installation.

Mitigation: Protect the token cache and its containing directory, and review the linked project documentation before relying on the tool.

## Reference(s):

- [Lose It Nutrition on ClawHub](https://clawhub.ai/stozo04/skills/loseit)
- [Project releases](https://github.com/stozo04/loseit-cli/releases)
- [Machine-readable output contract](https://github.com/stozo04/loseit-cli/blob/main/docs/MACHINE_CONTRACT.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration instructions]

**Output Format:** [Per-day JSON on stdout, with optional human-readable tables and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-day records keyed by ISO date; users can request recent or selected days.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
