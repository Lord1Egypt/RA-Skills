## Description:

工作日薪看板 Pro helps an agent recreate or adapt a single-file HTML/CSS/JavaScript wage dashboard with real-time earnings, payday countdown, Pomodoro focus timing, themes, responsive layouts, and saved settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lwter](https://clawhub.ai/user/lwter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to reproduce or modify a browser-based personal productivity widget for tracking earned wages, workday progress, payday timing, and Pomodoro focus sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Salary and work schedule settings are stored in the browser profile's localStorage.

Mitigation: Avoid entering sensitive salary data on shared browser profiles, and clear the widget's localStorage values when the profile is no longer trusted.

Risk: Opening the widget contacts the configured font CDN.

Mitigation: Review or self-host font dependencies before using the widget in restricted or privacy-sensitive environments.

Risk: The Pomodoro timer may request browser notification permission.

Mitigation: Grant notification permission only when desktop timer alerts are desired, and review browser site permissions if the widget is reused elsewhere.

Risk: The skill text mentions optional weather automation.

Mitigation: Add weather automation only intentionally, and review any added data source, network access, and permissions before deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lwter/skills/nexus-wage-widget)
- [daily_wage.html](references/daily_wage.html)
- [English README](readme.en.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTML, CSS, and JavaScript implementation details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill references a single-file widget and may include browser configuration guidance for localStorage, notifications, themes, layout, and font loading.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
