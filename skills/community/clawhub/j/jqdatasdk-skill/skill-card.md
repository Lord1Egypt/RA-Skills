## Description: <br>
Provides agent guidance, examples, and API references for using JoinQuant jqdatasdk to retrieve market, financial, factor, and related quantitative trading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IdiosyncraticDragon](https://clawhub.ai/user/IdiosyncraticDragon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative analysts use this skill to write Python workflows with jqdatasdk for strategy development, backtesting, data analysis, API troubleshooting, and SDK extension work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication may involve JoinQuant usernames, passwords, or tokens. <br>
Mitigation: Keep credentials in environment variables or a secret manager, and avoid hard-coding or logging them. <br>
Risk: Using the SDK sends authentication details and data queries to JoinQuant. <br>
Mitigation: Run the skill only where external JoinQuant access is expected and permitted. <br>
Risk: Installing or importing jqdatasdk from an unverified source could expose the environment to package-supply-chain risk. <br>
Mitigation: Install dependencies in a virtual environment and verify the jqdatasdk package source before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/IdiosyncraticDragon/jqdatasdk-skill) <br>
- [jqdatasdk API reference](references/api.md) <br>
- [Official jqdatasdk repository](https://github.com/JoinQuant/jqdatasdk.git) <br>
- [JoinQuant official API documentation](https://www.joinquant.com/help/api/) <br>
- [JoinQuant fundamentals data dictionary](https://www.joinquant.com/data/dict/fundamentals) <br>
- [JoinQuant index data](https://www.joinquant.com/indexData) <br>
- [JoinQuant industry classification](https://www.joinquant.com/data/dict/plateData) <br>
- [Third-party JoinQuant API type definitions](https://github.com/stairclimber/joinquant_api.git) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes jqdatasdk authentication, data-query, SQLAlchemy query, error-handling, performance, and API-extension examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
