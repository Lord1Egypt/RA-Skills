## Description: <br>
Find mountains, lakes, waterfalls, national parks, and natural wonders. Includes trail difficulty, best seasons, and photography tips. Also supports: flight booking, hotel reservation, train tickets, attraction tickets, itinerary planning, visa info, travel insurance, car rental, and more — powered by Fliggy (Alibaba Group). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to find natural attractions, compare CLI-sourced options, and present booking links for mountains, lakes, waterfalls, national parks, and similar points of interest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and rely on the global `@fly-ai/flyai-cli` package for provider-backed travel and booking results. <br>
Mitigation: Install only after reviewing and trusting the package source, and run the CLI in an environment appropriate for travel-booking queries. <br>
Risk: The skill can retain raw travel query details in `.flyai-execution-log.json` when filesystem writes are available. <br>
Mitigation: Avoid entering sensitive personal, financial, or exact itinerary details, and check, disable, or delete the local execution log when retention is not desired. <br>


## Reference(s): <br>
- [Nature Spots on ClawHub](https://clawhub.ai/xiejinsong/nature-spots) <br>
- [Publisher profile](https://clawhub.ai/user/xiejinsong) <br>
- [Templates reference](references/templates.md) <br>
- [Playbooks reference](references/playbooks.md) <br>
- [Fallbacks reference](references/fallbacks.md) <br>
- [Runbook reference](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with booking links, comparison tables, tips, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output for travel results and instructs the agent not to answer from model memory.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
