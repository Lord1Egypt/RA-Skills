## Description: <br>
Provides real-time and historical Indonesia Stock Exchange (IDX) market data through GoAPI for stock prices, issuer lists, market indexes, and company profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angween](https://clawhub.ai/user/angween) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to query IDX company listings, current active-stock prices, market indexes, and historical end-of-day price data through GoAPI. It helps agents format IDX market data in readable tables or lists with prices in Indonesian Rupiah. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The GoAPI key is placed in request URLs and may be exposed in logs, transcripts, or shared links. <br>
Mitigation: Use a separate revocable GoAPI key, avoid exposing full request URLs, and rotate the key if it may have been shared. <br>


## Reference(s): <br>
- [GoAPI](https://goapi.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/angween/idx-market-data) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API calls, Configuration] <br>
**Output Format:** [Markdown tables or lists with inline endpoint and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GOAPI_KEY for GoAPI requests and presents prices in Indonesian Rupiah (IDR).] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
