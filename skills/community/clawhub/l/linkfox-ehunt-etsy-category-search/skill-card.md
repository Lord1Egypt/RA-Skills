## Description: <br>
Searches locally synced EHunt Etsy category data through the LinkFox MCP service to find category names, IDs, and parent IDs for product or shop filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace operators, product researchers, and agents using LinkFox/EHunt use this skill to look up Etsy category IDs from a locally synced category library before product or shop queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Category results may be stale or empty when the local EHunt Etsy category library has not been synced recently. <br>
Mitigation: Sync the category library before searching and verify category freshness when accuracy matters. <br>
Risk: The skill can trigger on broad Etsy category lookup requests even when the user has not explicitly named EHunt. <br>
Mitigation: Confirm whether the user wants EHunt/local synced category data or another source before relying on the returned IDs. <br>
Risk: Optional command-line debugging depends on a LinkFox API key. <br>
Mitigation: Use LINKFOXAGENT_API_KEY only in the local environment or secret store and avoid exposing it in prompts, logs, or shared outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-ehunt-etsy-category-search) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands] <br>
**Output Format:** [Markdown instructions with tool names, parameters, and optional command-line debugging guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires locally synced EHunt Etsy category data; optional command-line debugging requires LINKFOXAGENT_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
