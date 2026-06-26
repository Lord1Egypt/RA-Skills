## Description: <br>
Jarvis Stock Price helps agents look up real-time China A-share stock prices with price movement, volume, and 5-day, 10-day, and 20-day moving averages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15910701838](https://clawhub.ai/user/15910701838) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents can use this skill to retrieve informational A-share stock data by code or name. It is suitable for quick market lookups and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the @tdx-local package and external/local market data availability. <br>
Mitigation: Verify the dependency source before installation and confirm data freshness before relying on returned prices. <br>
Risk: Stock results and the linked paid monitoring offer could be mistaken for investment advice. <br>
Mitigation: Present outputs as informational only and keep the non-investment-advice limitation visible to users. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Structured text object with stock code, name, price, change, volume, moving averages, and update time] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are informational stock data only and may depend on the availability and trustworthiness of the @tdx-local data source.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
