## Description:

Organize and manage party details from event setup and guest lists to menus, timelines, budgets, vendors, and day-of logistics for many event types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External users planning parties, gatherings, and small events use this skill to structure event details, manage guests and RSVPs, build budgets, plan menus, generate timelines, coordinate vendors, and produce day-of logistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PNG budget reports can render unescaped event data as active browser content.

Mitigation: Avoid PNG budget reports for imported or untrusted event data until the report path escapes HTML and disables JavaScript and network access; prefer Markdown reports for untrusted data.

Risk: Guest, vendor, dietary, venue, and budget details are stored as plaintext local JSON.

Mitigation: Keep the skill data directory in a restricted local workspace, use device or disk encryption where appropriate, and delete or archive event data when it is no longer needed.

Risk: The skill includes built-in promotional cross-sell behavior.

Mitigation: Review generated recommendations and disregard or remove cross-sell suggestions that are unrelated to the user's planning task.

## Reference(s):

- [Party Planner Pro on ClawHub](https://clawhub.ai/nollio/skills/normieclaw-party-planner-pro)
- [README](artifact/README.md)
- [Security notes](artifact/SECURITY.md)
- [Codex security audit](artifact/CODEX-SECURITY-AUDIT.md)
- [Dashboard companion kit spec](artifact/dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational guidance, local JSON schemas and files, Markdown exports, shell commands, and optional PNG budget reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores event data locally as JSON and can generate Markdown party plans and budget reports.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
