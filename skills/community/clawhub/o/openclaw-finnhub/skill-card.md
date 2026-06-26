## Description: <br>
Provides real-time U.S. stock quotes and financial data using the Finnhub API and Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keyfrog-21K](https://clawhub.ai/user/keyfrog-21K) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and market-data users use this skill to fetch current U.S. stock quote values from Finnhub through a Python helper script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime needs access to a Finnhub API key through an environment variable. <br>
Mitigation: Use a limited API key where possible and avoid pasting the key into prompts, source files, or logs. <br>
Risk: The helper contacts Finnhub to retrieve market data. <br>
Mitigation: Run it only in environments where outbound requests to Finnhub are expected and approved. <br>


## Reference(s): <br>
- [Finnhub API](https://finnhub.io) <br>
- [ClawHub release page](https://clawhub.ai/keyfrog-21K/openclaw-finnhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text quote output and concise Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Finnhub API key in the finnhub_api_key environment variable and network access to Finnhub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
