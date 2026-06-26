## Description: <br>
Life Query helps agents answer everyday information requests for parcel tracking, currency exchange, China fuel prices, and global weather forecasts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eamanc-lab](https://clawhub.ai/user/eamanc-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route natural-language life queries to shell-backed lookups for shipping status, exchange rates, China fuel prices, and weather forecasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Courier tracking numbers, optional carrier codes, currency queries, province names, and city names are sent to external services. <br>
Mitigation: Install only when this data sharing is acceptable, and configure KUAIDI100_KEY and KUAIDI100_CUSTOMER for direct courier lookup when preferred. <br>
Risk: Live lookup results depend on third-party service availability and freshness. <br>
Mitigation: Treat failures or stale responses as service limitations and ask the user to retry or verify important results with the source service. <br>


## Reference(s): <br>
- [Life Query ClawHub page](https://clawhub.ai/eamanc-lab/life-query) <br>
- [Life Query homepage](https://github.com/eamanc-lab/life-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON or plain-text tables from shell commands, usually summarized in natural language] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses external web services for live courier, exchange-rate, fuel-price, and weather data.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
