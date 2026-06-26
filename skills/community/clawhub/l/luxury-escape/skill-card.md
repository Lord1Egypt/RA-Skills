## Description: <br>
Luxury Escape helps agents design premium travel plans using real-time FlyAI/Fliggy search results for flights, hotels, attractions, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel planners use this skill to request premium itineraries with first-class or business-class flights, luxury hotels, attractions, and bookable options. Agents use it when real-time travel availability and pricing are required rather than static travel advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run a global third-party travel CLI. <br>
Mitigation: Install only in an environment where global npm packages are acceptable, and review the CLI package before use. <br>
Risk: Travel searches may be sent to FlyAI/Fliggy services. <br>
Mitigation: Avoid entering passport, payment, contact, or other highly sensitive personal details unless the deployment has approved that data flow. <br>
Risk: Raw travel queries may be retained locally in .flyai-execution-log.json. <br>
Mitigation: Check for and delete .flyai-execution-log.json when local query retention is not desired. <br>


## Reference(s): <br>
- [Luxury Escape ClawHub page](https://clawhub.ai/xiejinsong/luxury-escape) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Luxury travel playbooks](references/playbooks.md) <br>
- [Fallback guidance](references/fallbacks.md) <br>
- [Execution log runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables with booking links and inline shell commands for setup or retry guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires real-time flyai CLI output; should not emit raw JSON or unsourced travel recommendations.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
