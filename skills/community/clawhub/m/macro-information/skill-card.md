## Description: <br>
Macro-Information helps agents query FEEDAX-powered macroeconomic news and public-opinion data, including sentiment, event tags, heat scores, regions, and time-range filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longgggggg](https://clawhub.ai/user/longgggggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and finance or policy research users use this skill to search domestic and international macroeconomic news, filter by topic, sentiment, recency, and heat, and generate summaries plus CSV and Markdown result files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security assessment flags unsafe API key handling and unclear credential instructions. <br>
Mitigation: Use a scoped, revocable FEEDAX key through an environment variable or secret store, avoid pasting keys into chat, and review the credential flow before use. <br>
Risk: Search output can reveal private research or business interests through generated files. <br>
Mitigation: Use --no-output for sensitive searches or write results only to a controlled output directory. <br>
Risk: The skill queries an HTTP endpoint and includes API key handling in request parameters. <br>
Mitigation: Treat the endpoint as unsuitable for valuable credentials unless the transport and credential flow are reviewed and accepted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/longgggggg/macro-information) <br>
- [Publisher Profile](https://clawhub.ai/user/longgggggg) <br>
- [FEEDAX](https://www.feedax.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, csv] <br>
**Output Format:** [Terminal text with optional CSV and Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FEEDAX API key and may write timestamped macro_information CSV and Markdown files unless output is disabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
