## Description:

Runs the Apify Google Maps Email Extractor actor to build public business email lead lists with related Google Maps place, contact, and diagnostic fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hundevmode](https://clawhub.ai/user/hundevmode)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn lead-generation requests into Apify actor payloads, run controlled Google Maps email extraction jobs, and return structured rows for CRM, spreadsheet, automation, and agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lead-search inputs and extracted contact data are sent to Apify under the user's account.

Mitigation: Install and run the skill only when that transfer is acceptable for the intended workflow and account policies.

Risk: The actor can collect person-like emails or personal profile URLs when personal data collection is enabled.

Mitigation: Set includePersonalData=false unless there is a lawful, consent-aware reason to collect those fields.

Risk: Apify token exposure can occur if credentials are hardcoded, printed, or passed through command history.

Mitigation: Set APIFY_TOKEN in the environment, avoid command-line token arguments, and use a tightly scoped Apify token where possible.

Risk: Hosted actor usage can incur charges.

Mitigation: Set a budget guard with maxTotalChargeUsd or the script's --budget-usd option before running extraction jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hundevmode/skills/google-maps-email-extractor-apify)
- [Project homepage](https://github.com/hundevmode/apify-google-maps-email-extractor-agent-skill)
- [Apify actor store page](https://apify.com/x_guru/google-maps-email-extractor)
- [Apify actor console source](https://console.apify.com/actors/f3dlnXVnBc6v8JMNK/source)
- [Input and output contract](references/input-output-contract.md)
- [Sample input](references/sample_input.json)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON actor results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN and can use an Apify budget guard; output rows may include public business emails, person-like contact fields when enabled, websites, phones, social profiles, addresses, ratings, coordinates, Google IDs, and run diagnostics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
