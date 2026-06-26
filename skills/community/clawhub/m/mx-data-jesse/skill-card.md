## Description: <br>
Queries Eastmoney financial data for market, financial, relationship, and business information using natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jessecq1995](https://clawhub.ai/user/jessecq1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current Eastmoney financial datasets and convert API responses into readable previews plus local output files for further analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and API credentials are sent to an external Eastmoney financial data API. <br>
Mitigation: Install only if the Eastmoney/Miaoxiang provider is trusted, keep MX_APIKEY in a protected environment variable, and avoid sending secrets or sensitive internal financial questions unless sharing them with that provider is acceptable. <br>
Risk: Raw financial query results are saved locally and may contain sensitive or proprietary data. <br>
Mitigation: Protect the output directory, restrict access to generated Excel, text, and JSON files, and delete saved outputs when they are no longer needed. <br>


## Reference(s): <br>
- [Eastmoney Miaoxiang homepage](https://marketing.dfcfs.com/views/finskillshub/indexIoMv0EzE) <br>
- [ClawHub skill page](https://clawhub.ai/jessecq1995/mx-data-jesse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files] <br>
**Output Format:** [Terminal markdown preview plus Excel, text description, and raw JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MX_APIKEY, sends query text to the Eastmoney API, and saves results under the configured local output directory.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
