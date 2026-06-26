## Description: <br>
Ocean Io connects an agent to Ocean.io for B2B prospecting, lookalike company discovery, decision-maker identification, and enriched list export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mokto](https://clawhub.ai/user/Mokto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, GTM, and revenue teams use this skill to search Ocean.io company and people data, build lookalike prospect lists, identify decision-makers, and export selected records for outreach workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an Ocean.io API token to spend account credits through searches and exports. <br>
Mitigation: Use a revocable or limited API token when available, and approve searches or exports only after reviewing record counts and credit costs. <br>
Risk: Exports may include personal contact data for outreach workflows. <br>
Mitigation: Export or use contact data only when the organization has authorization and a lawful business basis. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Mokto/ocean-io) <br>
- [Ocean.io MCP Endpoint](https://api.ocean.io/mcp/?api-token=${OCEAN_API_TOKEN}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, CSV export links, Guidance] <br>
**Output Format:** [Markdown responses with tabular search results, credit estimates, field guidance, and export download URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Ocean.io API token; searches and exports should include record counts and credit-cost confirmation before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
