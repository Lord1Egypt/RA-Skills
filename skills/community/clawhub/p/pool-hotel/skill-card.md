## Description: <br>
Find hotels with swimming pools, including indoor heated pools, outdoor infinity pools, rooftop pools, and kid-friendly splash areas, using Fliggy-powered flyai CLI results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel agents use this skill to find pool-equipped hotels and format real-time booking options from flyai CLI output. It is intended for travel search and booking assistance where responses must include current results and booking links rather than model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run a global flyai CLI package. <br>
Mitigation: Install only when the CLI package is trusted, verify the installed CLI before use, and consider running it in an isolated environment. <br>
Risk: The skill may keep raw travel queries in a local execution log. <br>
Mitigation: Avoid entering sensitive personal travel details unless local logging is acceptable, and disable or delete .flyai-execution-log.json after use when appropriate. <br>
Risk: Travel results depend on external CLI output and may fail or become unavailable. <br>
Mitigation: Use the documented fallback flow, report failures honestly, and only present hotel options that include valid booking links from CLI output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiejinsong/pool-hotel) <br>
- [templates.md](references/templates.md) <br>
- [playbooks.md](references/playbooks.md) <br>
- [fallbacks.md](references/fallbacks.md) <br>
- [runbook.md](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, inline shell commands, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs must be based on flyai CLI results, include Book links when results are shown, and avoid raw JSON.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
