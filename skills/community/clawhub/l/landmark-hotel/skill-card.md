## Description: <br>
Find hotels closest to a specific attraction, landmark, or scenic spot by verifying the point of interest and searching hotels sorted by walking distance, powered by Fliggy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel users and agent operators use this skill to find hotels near landmarks, attractions, scenic areas, ancient towns, theme parks, and nature areas using real-time flyai CLI results. It helps collect parameters, verify the point of interest, run the appropriate hotel search, and format bookable results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install the flyai CLI globally with npm, which can change the execution environment and introduce package trust risk. <br>
Mitigation: Review and approve the @fly-ai/flyai-cli package before installation, and prefer a controlled or isolated environment for running the CLI. <br>
Risk: Travel searches may be shared with the flyai/Fliggy service. <br>
Mitigation: Use the skill only when users are comfortable sending destination, date, budget, and preference details to that service. <br>
Risk: The artifact describes a hidden local execution log that may store raw trip details on disk. <br>
Mitigation: Disable, avoid creating, or delete .flyai-execution-log.json when raw travel queries should not be retained locally. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>
- [ClawHub release page](https://clawhub.ai/xiejinsong/landmark-hotel) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Hotel results must come from flyai CLI output and include booking links when results are shown.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
