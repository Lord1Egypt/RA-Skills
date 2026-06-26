## Description: <br>
Query free financial data APIs -- stocks, crypto, macro, SEC filings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anotb](https://clawhub.ai/user/anotb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to ask an agent for `omd` commands that retrieve market, crypto, macroeconomic, SEC filing, and related financial data from free external providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party `open-market-data` npm package and its `omd` executable. <br>
Mitigation: Install only when the package and linked project are trusted for the intended environment. <br>
Risk: Configured provider credentials may be exposed if terminal output from `omd config show` is shared. <br>
Mitigation: Prefer environment variables for API keys and avoid sharing command output that displays configuration values. <br>
Risk: Automatic routing and fallback can send a query to different external data providers. <br>
Mitigation: Use `--source` when the agent or operator needs to control which provider receives a query. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anotb/open-market-data) <br>
- [open-market-data project homepage](https://github.com/anotb/open-market-data) <br>
- [Publisher profile](https://clawhub.ai/user/anotb) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text, JSON] <br>
**Output Format:** [Markdown with bash command examples and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include provider selection flags, API-key configuration guidance, and commands that call external financial-data services.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
