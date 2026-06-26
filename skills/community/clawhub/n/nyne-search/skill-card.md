## Description: <br>
Search for people using natural language queries with the Nyne Search API, including custom filters, AI relevance scoring, contact enrichment, pagination, and light, medium, or premium search tiers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MichaelFanous2](https://clawhub.ai/user/MichaelFanous2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to submit and poll Nyne people-search requests, filter professional profiles, paginate results, and present returned profile and contact data for legitimate, authorized use cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve and display enriched personal contact and demographic data. <br>
Mitigation: Use it only for legitimate, authorized people-search workflows, show and retain only the data needed, and delete local result files containing enriched profiles. <br>
Risk: API credentials and callback URLs can expose sensitive access or result data if mishandled. <br>
Mitigation: Keep Nyne API secrets out of terminal output and logs, and use callback URLs only when they are trusted and appropriate for receiving search results. <br>


## Reference(s): <br>
- [Nyne API](https://api.nyne.ai) <br>
- [Nyne Person Search endpoint](https://api.nyne.ai/person/search) <br>
- [ClawHub listing](https://clawhub.ai/MichaelFanous2/nyne-search) <br>
- [Publisher profile](https://clawhub.ai/user/MichaelFanous2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API request commands, polling instructions, jq filters, and summaries of returned people-search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
