## Description: <br>
Queries FEEDAX for industry news and public-opinion signals, including sentiment, industry classifications, heat metrics, and result summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longgggggg](https://clawhub.ai/user/longgggggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and business users use this skill to research industry trends, monitor positive and negative public opinion, compare industries, assess investment or policy risk, and export FEEDAX query results for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FEEDAX API keys can be exposed if pasted into chat, printed from environment files, stored insecurely, or sent over plain HTTP. <br>
Mitigation: Use a scoped, rotatable key in an environment variable, avoid commands that print complete environment files, prefer --no-output for sensitive searches, and rotate any key that may have been exposed. <br>
Risk: Search queries and credentials are sent to the configured FEEDAX endpoint. <br>
Mitigation: Use the skill only when sharing the query terms and credentials with that endpoint is acceptable under the user's data-handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/longgggggg/industry-information) <br>
- [FEEDAX](https://www.feedax.cn) <br>
- [FEEDAX industry information API endpoint](http://221.6.15.90:18011) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Conversational summaries with optional CSV and Markdown result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FEEDAX API key supplied by command-line argument, FEEDAX_API_KEY, or a local config file; --no-output can suppress result file generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
