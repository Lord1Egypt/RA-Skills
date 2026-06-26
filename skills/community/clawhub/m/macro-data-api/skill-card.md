## Description: <br>
查询货币供应量、汇率、利率和美元指数。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arsars2234](https://clawhub.ai/user/arsars2234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query U.S. macroeconomic and financial datasets, including money supply, exchange rates, interest rates, Treasury data, GDP components, and inflation indexes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to a hardcoded private HTTP macro-data service, so query names, dates, and parameters may travel unencrypted on that network. <br>
Mitigation: Install and run this skill only when you intentionally use that service; prefer trusted network access or an HTTPS-protected service where available. <br>
Risk: The helper script depends on the Python requests package, which may not be installed in every agent environment. <br>
Mitigation: Verify python3 and requests are available before use, and install dependencies through the environment's approved package-management process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arsars2234/macro-data-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the Python requests package; queries a configured HTTP FastAPI endpoint.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
