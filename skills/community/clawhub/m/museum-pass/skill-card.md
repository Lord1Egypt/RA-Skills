## Description: <br>
Find museums, art galleries, and exhibitions in any city, including ticket links and visiting tips, using live flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search for museum, gallery, exhibition, and memorial-hall entry options, then format real-time results with booking links and visiting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install a global third-party flyai CLI. <br>
Mitigation: Require explicit user approval before running `npm i -g @fly-ai/flyai-cli` and verify the package source before installation. <br>
Risk: Live travel and booking searches may be sent to the flyai provider. <br>
Mitigation: Avoid sending passport, payment, identity, private itinerary, or other sensitive personal details through the skill. <br>
Risk: The skill may keep hidden local logs of raw user queries in `.flyai-execution-log.json`. <br>
Mitigation: Review, disable, or delete the local execution log when raw prompts should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/museum-pass) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and concise guidance with inline booking links and occasional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should come from flyai CLI output, include detailUrl booking links, and preserve the user's language.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
