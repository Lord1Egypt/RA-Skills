## Description: <br>
Check exchange rates, currency tips, and money-saving strategies for international travel, including ATM fees, card acceptance, local payment methods, and related Fliggy-powered travel services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer currency exchange and travel money questions by checking live results through the flyai CLI. It is also framed to support adjacent travel commerce searches such as hotels, trains, attractions, insurance, and car rental when routed through the same provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to install an unpinned global FlyAI CLI. <br>
Mitigation: Review the package source and install it only in a controlled environment; pin and verify the CLI version when operational policy allows. <br>
Risk: Currency and travel queries are sent to an external provider and may return commercial booking links. <br>
Mitigation: Avoid sensitive personal data in queries and require explicit user confirmation before acting on booking or purchase links. <br>
Risk: The artifact describes hidden local logging of raw user queries. <br>
Mitigation: Disable or delete the local execution log behavior before use, and inspect `.flyai-execution-log.json` if the skill has already run. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/money-exchange) <br>
- [Templates Reference](references/templates.md) <br>
- [Playbooks Reference](references/playbooks.md) <br>
- [Fallbacks Reference](references/fallbacks.md) <br>
- [Runbook Reference](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, tips, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for factual results and includes provider booking links when results are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
