## Description: <br>
Howtocook is an API-backed recipe assistant for recipe search, category filtering, meal planning, shopping-list guidance, and daily menu recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Howtocook to retrieve recipes, filter by food category, generate weekly meal plans for 1-10 diners based on allergies and avoided ingredients, and produce shopping-list style guidance through the Xiaobenyang service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Xiaobenyang API key and stores it in a local .env file, which can expose credentials if the file is shared or committed. <br>
Mitigation: Keep the .env file out of source control and shared folders, prefer environment variables where practical, and rotate the API key if exposure is suspected. <br>
Risk: Recipe and meal-planning answers depend on the upstream Xiaobenyang service and should not be fabricated when the API key is missing or an upstream call fails. <br>
Mitigation: Ask the user for the required API key before use, call the provided tools for recipe data, and surface upstream errors clearly instead of inventing results. <br>


## Reference(s): <br>
- [Howtocook ClawHub listing](https://clawhub.ai/cainingnk/howtocook) <br>
- [Xiaobenyang service](https://xiaobenyang.com) <br>
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration guidance] <br>
**Output Format:** [Markdown summaries of API JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Xiaobenyang API key in XBY_APIKEY or a local .env file; recipe tools accept category, query, allergies, avoided items, and people count parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
