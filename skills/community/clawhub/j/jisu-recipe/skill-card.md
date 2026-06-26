## Description: <br>
Looks up recipes by keyword or category through JisuAPI and returns recipe categories, recipe lists, and recipe details for cooking questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer cooking questions by searching recipes, browsing recipe categories, and retrieving detailed ingredients and steps from JisuAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using a JisuAPI AppKey for recipe searches and detail lookups can consume external API quota or billing. <br>
Mitigation: Use a dedicated JisuAPI key for this skill and monitor quota or billing for recipe API usage. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/jisu-recipe) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI Recipe API](https://www.jisuapi.com/api/recipe/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; recipe lookup responses depend on the external JisuAPI service.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
