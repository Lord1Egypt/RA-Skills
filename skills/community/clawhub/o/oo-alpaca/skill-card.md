## Description: <br>
Alpaca (alpaca.markets) helps agents read, create, and update data through Alpaca by using the OOMOL oo CLI connector instead of direct API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate Alpaca accounts and market data through an OOMOL-connected account, including account details, portfolio history, orders, positions, watchlists, market calendars, and stock or crypto market data. It is suited for agent-assisted workflows where the connector schema is checked before actions run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive Alpaca account, order, position, and portfolio data. <br>
Mitigation: Install it only for intended OOMOL-connected Alpaca accounts and treat returned financial data as sensitive. <br>
Risk: Some proposed connector actions could create, update, cancel, or otherwise affect trading or account state. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running any state-changing action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-alpaca) <br>
- [Alpaca homepage](https://alpaca.markets/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions return JSON when executed with the oo CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
