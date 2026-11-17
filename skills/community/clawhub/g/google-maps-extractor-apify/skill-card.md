## Description:

Helps agents run the Apify Google Maps Extractor actor to collect structured Google Maps place and business data, with optional public website contact enrichment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hundevmode](https://clawhub.ai/user/hundevmode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to build Google Maps extraction payloads, run the Apify actor with budget controls, and return structured place and business rows for local lead generation, local SEO, competitor research, store locator datasets, and CRM enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Apify API token.

Mitigation: Use APIFY_TOKEN from environment or secret storage, prefer a least-privilege token, and avoid printing or passing the token in user-visible commands.

Risk: Search targets, Maps URLs, Place IDs, and optional contact-enrichment inputs are sent to Apify.

Mitigation: Limit inputs to data needed for the task and use contact enrichment only for lawful, consent-aware, anti-spam-compliant workflows with clear retention limits.

Risk: Broad extraction jobs can increase cost and collect more data than intended.

Mitigation: Start with small runs and set maxTotalChargeUsd or --budget-usd before scaling.

Risk: The server security review notes supply-chain and privacy weaknesses that warrant review before use.

Mitigation: Pin installer or source versions where possible and review the skill before deploying it with production credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hundevmode/skills/google-maps-extractor-apify)
- [ClawHub Metadata Homepage](https://github.com/hundevmode/apify-google-maps-extractor-agent-skill)
- [Apify Google Maps Extractor](https://apify.com/x_guru/google-maps-extractor)
- [Apify Actor Console Source](https://console.apify.com/actors/2A4RTA5PjN7McqJXx/source)
- [Input and Output Contract](references/input-output-contract.md)
- [Sample Input](references/sample_input.json)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with JSON payloads and shell command examples; runner output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_TOKEN; optional budget controls can limit Apify run spend.]

## Skill Version(s):

1.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
