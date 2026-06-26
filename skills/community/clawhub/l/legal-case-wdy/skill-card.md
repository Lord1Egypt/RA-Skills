## Description: <br>
Legal case wdy helps an agent retrieve relevant legal provisions and similar case examples from Wendaoyun for user-described disputes, then format legal consequences and suggested next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rose-develop](https://clawhub.ai/user/rose-develop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and legal support users use this skill to help an agent research legal provisions and similar cases for described disputes. The output should be treated as legal research support rather than professional legal advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Case summaries may contain personal, financial, or legally sensitive details that are sent to Wendaoyun's API. <br>
Mitigation: Avoid unnecessary names, IDs, addresses, and sensitive financial details; confirm privacy compliance before submitting case descriptions. <br>
Risk: Legal research output may be mistaken for professional legal advice. <br>
Mitigation: Treat retrieved laws, similar cases, and analysis as reference material and consult qualified legal counsel before making legal decisions. <br>
Risk: The WENDAOYUN_API_KEY is a credential that could be exposed through prompts, logs, or copied commands. <br>
Mitigation: Store the key in an environment variable, avoid sharing it in chat or logs, and revoke it promptly if exposure is suspected. <br>


## Reference(s): <br>
- [Wendaoyun Open Platform](https://open.wintaocloud.com/home) <br>
- [Wendaoyun legal provisions API endpoint](https://h5.wintaocloud.com/prod-api/api/invoke/get-laws) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with formatted legal provisions, case summaries, optional analysis, and setup commands when configuration is missing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WENDAOYUN_API_KEY. Sends user case descriptions to Wendaoyun APIs; default top_k is 3, maximum top_k is 5, and the documented daily quota is 200 API calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
