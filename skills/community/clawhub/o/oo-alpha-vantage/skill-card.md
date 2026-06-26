## Description: <br>
Enables agents to query Alpha Vantage market, company, forex, crypto, commodity, macroeconomic, news, and sector data through OOMOL's oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to fetch Alpha Vantage financial and market data after inspecting the live connector schema and running read-oriented connector actions with JSON payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence says scan telemetry is clean but still advises users to skim the skill before installing. <br>
Mitigation: Install only after confirming the requested connector actions match the expected Alpha Vantage use case. <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected account. <br>
Mitigation: Use the documented setup flow and avoid exposing raw Alpha Vantage tokens in prompts, files, or shell history. <br>


## Reference(s): <br>
- [ClawHub Alpha Vantage skill page](https://clawhub.ai/oomol/oo-alpha-vantage) <br>
- [Alpha Vantage homepage](https://www.alphavantage.co) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and PowerShell command examples; connector responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions return data with meta.executionId; Alpha Vantage credentials are handled through the user's OOMOL-connected account.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
