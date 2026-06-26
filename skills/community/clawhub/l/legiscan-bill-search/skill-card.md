## Description: <br>
Search and track active or completed state bills by keywords and state using the LegiScan API with customizable filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n4cra](https://clawhub.ai/user/n4cra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, policy analysts, and advocacy teams use this skill to query LegiScan for state bills matching selected keywords and produce concise bill summaries for legislative monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A LegiScan API key and selected state and keyword searches are sent to LegiScan. <br>
Mitigation: Use a LegiScan key intended for this workflow and choose search terms with the expectation that they are processed by LegiScan. <br>
Risk: Command logs or traces may expose full request URLs that include sensitive API key material. <br>
Mitigation: Avoid sharing raw command logs and redact request URLs or API keys before storing or sending troubleshooting output. <br>
Risk: Scheduled cron usage can create recurring external API searches. <br>
Mitigation: Configure cron only when recurring legislative searches are intended and review the configured state and keyword filters. <br>


## Reference(s): <br>
- [LegiScan API](https://legiscan.com/legiscan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown-formatted plain text printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LEGISCAN_API_KEY; optional state, keyword, and include-passed filters control results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
