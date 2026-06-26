## Description: <br>
Runs Google Maps place and business data extraction through an Apify actor, including local listings, contact fields, ratings, addresses, coordinates, Google identifiers, and optional public website contact enrichment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hundevmode](https://clawhub.ai/user/hundevmode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and operations teams use this skill to build and run scoped Apify Google Maps extraction jobs for local business datasets, lead lists, local SEO research, CRM enrichment, and related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Maps search inputs, URLs, and extraction jobs are sent to Apify using APIFY_TOKEN. <br>
Mitigation: Use this skill only for data you are comfortable processing through Apify, keep runs scoped, and protect the token from logs and user-facing output. <br>
Risk: Actor runs and optional add-ons can create usage costs. <br>
Mitigation: Start with small limits, use budget controls such as maxTotalChargeUsd or --budget-usd, and enable paid add-ons only when needed. <br>
Risk: Public website contact enrichment can collect emails, phone numbers, or social links that may be regulated in downstream use. <br>
Mitigation: Collect only fields needed for the use case and confirm compliance with applicable privacy, anti-spam, and data protection rules before using enriched contact data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hundevmode/google-maps-extractor-apify) <br>
- [Project homepage](https://github.com/hundevmode/apify-google-maps-extractor-agent-skill) <br>
- [Apify Google Maps Extractor actor](https://apify.com/x_guru/google-maps-extractor) <br>
- [Apify actor console source](https://console.apify.com/actors/2A4RTA5PjN7McqJXx/source) <br>
- [Input and output contract](references/input-output-contract.md) <br>
- [Sample input](references/sample_input.json) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads or results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runner output includes status, actor ID, timestamp, input used, item count, and dataset rows. Results depend on the Apify actor response and enabled extraction add-ons.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
