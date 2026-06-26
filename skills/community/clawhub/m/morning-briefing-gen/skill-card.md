## Description: <br>
Generates structured daily morning briefings from domestic and international news, finance updates, industry developments, and policy items, with action suggestions and optional scheduled delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, executives, founders, investors, and operators use this skill to produce concise morning briefings and action suggestions for daily planning. It can also be configured for recurring briefing generation when scheduling is deliberately enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring briefing generation can run at unexpected times or deliver to the wrong destination if scheduling details are unclear. <br>
Mitigation: Before enabling scheduling, confirm the exact time, timezone, destination, output path, and disable procedure. <br>
Risk: The package security report references a script that is not present in the artifact, creating an inconsistency between claims and shipped contents. <br>
Mitigation: Review the installed package contents directly and do not rely on the bundled security report alone. <br>
Risk: Briefing content may include incomplete, stale, or simulated news if the available data sources are limited. <br>
Mitigation: Review generated briefings before business use and verify important news, finance, or policy items against authoritative sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/johnsmithfan/morning-briefing-gen) <br>
- [Publisher profile](https://clawhub.ai/user/johnsmithfan) <br>
- [Security review artifact](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown briefing content and dated workspace Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scheduled briefing configuration when the user requests recurring generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
