## Description: <br>
工作日薪看板 Pro is a single-file HTML widget for real-time wage tracking, payday countdowns, Pomodoro focus timing, configurable themes, and responsive glass-style layouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lwter](https://clawhub.ai/user/lwter) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and personal productivity users use this skill to inspect, recreate, or customize a browser wage dashboard that calculates workday earnings and includes a 25-minute Pomodoro timer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The widget stores salary and work schedule settings in browser localStorage. <br>
Mitigation: Use it only in browser profiles where local storage is acceptable, and avoid entering sensitive compensation details on shared devices. <br>
Risk: The widget loads font assets from the listed CDN domains. <br>
Mitigation: Allow those requests only if acceptable for the deployment environment, or replace the font links with approved self-hosted assets. <br>
Risk: Optional weather data generation should remain user-directed. <br>
Mitigation: Fetch or provide weather data only when the user asks for it and review any generated weather file before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lwter/nexus-wage-widget) <br>
- [Daily Wage widget source](references/daily_wage.html) <br>
- [English README](readme.en.md) <br>
- [Chinese README](readme.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration instructions] <br>
**Output Format:** [Markdown with inline HTML, CSS, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference the bundled single-file HTML widget and localStorage configuration keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
