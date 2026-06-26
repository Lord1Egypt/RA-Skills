## Description: <br>
Enrich LinkedIn profile URLs with mobile phone numbers and work/personal emails using Apify actors, merging results into unified output records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hundevmode](https://clawhub.ai/user/hundevmode) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to enrich authorized LinkedIn profile URL lists with emails and phone numbers, then export merged contact records for outbound, CRM, spreadsheet, or automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitting LinkedIn profile URLs to Apify actors may disclose personal or contact data to third-party services. <br>
Mitigation: Submit only profiles you are authorized to enrich, verify actor owners, pricing, and terms, and apply applicable privacy, anti-spam, and platform-compliance rules. <br>
Risk: APIFY_TOKEN can grant access to Apify account resources. <br>
Mitigation: Store the token in an environment variable or secret store, avoid hardcoding it in workflows, and rotate it if exposed. <br>
Risk: Phone or personal-email enrichment may collect more data than needed for a workflow. <br>
Mitigation: Disable phone or personal-email branches when they are not required, and start with small URL batches before larger runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hundevmode/linkedin-email-phone-apify) <br>
- [Input contract](references/input-contract.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Apify phone actor X95BXRaFOqZ7rzjxM](https://console.apify.com/actors/X95BXRaFOqZ7rzjxM) <br>
- [Apify email actor q3wko0Sbx6ZAAB2xf](https://console.apify.com/actors/q3wko0Sbx6ZAAB2xf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON result objects and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_TOKEN and user-provided LinkedIn profile URLs; email and phone enrichment branches can run together or independently.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
