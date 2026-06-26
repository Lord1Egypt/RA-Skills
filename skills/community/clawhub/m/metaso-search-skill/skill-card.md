## Description: <br>
Search the web using Metaso AI Search API for live information, documentation, and research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[square123](https://clawhub.ai/user/square123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query the Metaso AI Search API for current web, news, paper, documentation, or research results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and selected options are sent to Metaso through the configured API key. <br>
Mitigation: Use only approved queries and avoid submitting secrets, private internal URLs, regulated data, or confidential proprietary text. <br>
Risk: The script depends on the local Python requests package. <br>
Mitigation: Run the skill in a trusted Python environment and install dependencies from trusted sources. <br>


## Reference(s): <br>
- [Metaso Search API Playground](https://metaso.cn/search-api/playground) <br>
- [ClawHub Skill Page](https://clawhub.ai/square123/metaso-search-skill) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON search results printed to stdout, with Markdown usage guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires METASO_API_KEY and Python with the requests package available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
