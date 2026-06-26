## Description: <br>
B2B prospecting and company intelligence using the AgentSource API: users describe target companies or contacts in plain language, then the agent maps filters, previews results, enriches records, and exports CSVs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yossigolan](https://clawhub.ai/user/yossigolan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, revenue operations, recruiting, and market-research users use this skill to search for B2B companies or prospects, estimate market size, preview samples, enrich records with company/contact intelligence, and export confirmed results to CSV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles API keys and sensitive lead, contact, customer, or prospect data with weak local containment. <br>
Mitigation: Set EXPLORIUM_API_KEY yourself instead of sharing it in chat, store exports in private locations, and delete /tmp/agentsource_*.json files after sensitive runs. <br>
Risk: Search filters, entity IDs, matching records, and optional call_reasoning may be sent to Explorium's API. <br>
Mitigation: Use the skill only when that data transfer is acceptable, and omit call_reasoning for confidential searches unless the user explicitly consents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yossigolan/lead-enricher-explorium-agentsource) <br>
- [Explorium AgentSource API key setup](https://developers.explorium.ai/reference/setup/getting_your_api_key) <br>
- [Filter Reference](artifact/references/filters.md) <br>
- [Enrichment Reference](artifact/references/enrichments.md) <br>
- [Events Reference](artifact/references/events.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON, CSV files, markdown] <br>
**Output Format:** [Markdown guidance with shell commands; CLI calls write JSON result files and can export CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EXPLORIUM_API_KEY; API results are written to /tmp/agentsource_*.json and CSV exports are written to user-selected local paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
