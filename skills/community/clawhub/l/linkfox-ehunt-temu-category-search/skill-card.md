## Description: <br>
Searches locally synced EHunt Temu category data by keyword to find Chinese and English category names and category IDs for product or shop filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and sourcing operators use this skill to look up Temu category IDs from an already synced EHunt local category database, then pass those IDs into product or shop filtering workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a LinkFox API credential. <br>
Mitigation: Provide LINKFOXAGENT_API_KEY only through the environment or a managed secret store, rotate it if exposed, and do not commit credentials or response files. <br>
Risk: The bundled response helper can execute arbitrary local Python scripts and read arbitrary JSON files. <br>
Mitigation: Prefer the direct category-search script or MCP tool when possible, and use response_io.py only with the intended script and response files for this task. <br>
Risk: Persisted API responses may contain sensitive business or account data. <br>
Mitigation: Write large responses to a temporary directory outside any git working tree, extract only needed fields, and delete saved files after use. <br>


## Reference(s): <br>
- [EHunt Temu Category Search API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-ehunt-temu-category-search) <br>
- [LinkFox Tool Gateway Endpoint](https://tool-gateway.linkfox.com/ehunt/temu/temuCategorySearch) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY and a previously synced local EHunt Temu category database.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
