## Description: <br>
An MCP-based recipe recommendation skill that queries recipes, filters categories, creates meal plans, and suggests daily menus through the Xiaobenyang API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and cooking assistants use this skill to retrieve recipe details, browse recipe categories, and generate meal recommendations or weekly meal plans based on people count, allergies, and avoided ingredients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves the required Xiaobenyang API key in a local .env file. <br>
Mitigation: Use it only from a protected, non-shared directory; exclude .env from source control and rotate the key if exposure is suspected. <br>
Risk: The skill depends on a user-provided Xiaobenyang API key before it can return API-backed recipe results. <br>
Mitigation: Prompt for the key when it is missing and avoid fabricating recipe data when the key is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/howtocook) <br>
- [Xiaobenyang API key portal](https://xiaobenyang.com) <br>
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries of API-backed JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recipe details, category-filtered lists, weekly meal plans, shopping lists, and direct meal suggestions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
