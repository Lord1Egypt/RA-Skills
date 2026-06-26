## Description: <br>
Provides Korean apartment transaction analytics by region, transaction type, and period through the eho OpenClaw tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[novb1492](https://clawhub.ai/user/novb1492) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up and summarize South Korean apartment transaction information by city or province, transaction type, and date range. It is suited for apartment price and rental transaction analysis where the user can provide clear regional and time-period inputs. <br>

### Deployment Geography for Use: <br>
Global use, with data coverage focused on South Korea. <br>

## Known Risks and Mitigations: <br>
Risk: User-provided region, apartment, transaction type, and date range are sent to an external real estate service and may appear in local logs. <br>
Mitigation: Avoid entering secrets or private personal details, and review query parameters before execution. <br>
Risk: The skill returns apartment transaction analytics from an external service that may be incomplete or unavailable for some regions or periods. <br>
Mitigation: Treat results as decision support and verify important real estate or financial conclusions against authoritative sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/novb1492/korean-apartment-real-estate-transaction-analytics) <br>
- [npm package @brokimyeah/openclaw-eho](https://www.npmjs.com/package/@brokimyeah/openclaw-eho) <br>
- [Everyhouse real transaction service](https://www.everyhouse-real-payment.com/?si=%EC%84%9C%EC%9A%B8&sn=0) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Text response containing query details and the external service response, with JSON formatted when the service returns JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires sido, typeDetail, start, and end parameters; gu, dong, and apt are optional refinements.] <br>

## Skill Version(s): <br>
1.1.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
