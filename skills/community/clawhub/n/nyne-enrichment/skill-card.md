## Description: <br>
Enrich any person by email, phone, LinkedIn URL, or name using the Nyne Enrichment API, returning contact information, social profiles, work history, education, and optional social media posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MichaelFanous2](https://clawhub.ai/user/MichaelFanous2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide agent-driven person enrichment workflows through the Nyne API, including request submission, status polling, and presentation of returned profile data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad third-party people enrichment and may expose sensitive personal data. <br>
Mitigation: Use it only for legitimate, authorized enrichment, treat inputs and results as sensitive data, and follow applicable privacy and compliance requirements. <br>
Risk: Example workflows write enrichment responses to /tmp/nyne_enrich.json, which can retain personal data after use. <br>
Mitigation: Delete or securely store result files after review and avoid printing or logging sensitive outputs unnecessarily. <br>
Risk: Optional newsfeed and AI-enhanced search modes can collect more data than a basic lookup needs. <br>
Mitigation: Enable newsfeed or AI-enhanced search only when the additional information is necessary for the user's authorized purpose. <br>
Risk: The skill requires Nyne API credentials. <br>
Mitigation: Provide credentials through environment variables, do not echo or log full secrets, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [Nyne API](https://api.nyne.ai) <br>
- [Nyne Person Enrichment API](https://api.nyne.ai/person/enrichment) <br>
- [ClawHub skill page](https://clawhub.ai/MichaelFanous2/nyne-enrichment) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NYNE_API_KEY and NYNE_API_SECRET; API results are asynchronous and require polling by request_id.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
