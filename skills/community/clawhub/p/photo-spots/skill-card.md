## Description: <br>
Photo Spots helps agents find photogenic travel locations and related Fliggy travel options by running flyai CLI searches and formatting sourced results with booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to find photogenic viewpoints, city walks, art districts, and related travel services in the user's language, using flyai/Fliggy results rather than model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run the flyai/Fliggy CLI globally. <br>
Mitigation: Review and approve the CLI installation before use, or install it manually in a controlled environment. <br>
Risk: Travel requests can be written to a local .flyai-execution-log.json file. <br>
Mitigation: Avoid entering sensitive itinerary or personal details unless logging is disabled, or delete the local log after use. <br>
Risk: Results depend on real-time CLI output and can be incomplete if the CLI, network, or service is unavailable. <br>
Mitigation: Use the documented retry and fallback flow, report failures honestly, and do not answer from model memory. <br>


## Reference(s): <br>
- [Templates](references/templates.md) <br>
- [Playbooks](references/playbooks.md) <br>
- [Fallbacks](references/fallbacks.md) <br>
- [Runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables and concise travel guidance with booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output; listed results should include detailUrl booking links and the flyai brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
