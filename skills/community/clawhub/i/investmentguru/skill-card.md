## Description: <br>
Analyzes A-share, Hong Kong, and U.S. stocks using methods attributed to 20 Chinese and international investment figures, combining market data with valuation, fundamentals, technical, and sentiment signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amitabhama](https://clawhub.ai/user/amitabhama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to fetch stock market data and generate multi-perspective stock analysis reports. It is intended for informational financial analysis workflows, not as a substitute for professional investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the release ships an embedded market-data API token. <br>
Mitigation: Remove and rotate the hardcoded token, and require users to provide their own credentials when that data source is needed. <br>
Risk: The security review says the skill can auto-trigger broadly on stock-related language. <br>
Mitigation: Require explicit user confirmation before running analysis or acting on outputs from broad keyword matches. <br>
Risk: The security review says the skill gives direct buy or sell guidance without adequate safeguards. <br>
Mitigation: Clearly label outputs as informational analysis and require human financial review before any investment decision. <br>
Risk: The security review flags finance and privacy risks around market-data use. <br>
Mitigation: Disclose all market-data providers and review what query data may be sent to external services before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amitabhama/investmentguru) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [manifest.json](artifact/manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown-like stock analysis reports, Python API responses, and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include market-data-based buy, hold, sell, or watch recommendations and should be reviewed as informational analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and setup.py; artifact manifest lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
