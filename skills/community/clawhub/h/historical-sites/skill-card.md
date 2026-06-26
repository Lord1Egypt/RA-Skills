## Description: <br>
Explore ancient ruins, monuments, UNESCO World Heritage sites, and historical landmarks with detailed cultural context and visiting guides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to find historical landmarks, UNESCO sites, ancient ruins, and related attraction options through the flyai CLI with booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify the host by installing a global npm CLI dependency. <br>
Mitigation: Review the npm package before installation and prefer installing the CLI manually in a controlled environment. <br>
Risk: The skill may persist raw travel queries in a local execution log. <br>
Mitigation: Disable, delete, or avoid retaining .flyai-execution-log.json when raw request history should not be stored. <br>
Risk: The workflow depends on third-party travel and booking data from FlyAI/Fliggy. <br>
Mitigation: Review generated booking-oriented results before use and avoid relying on responses that lack CLI-sourced booking links. <br>


## Reference(s): <br>
- [Skill README](README.md) <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/historical-sites) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel data; responses should include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
