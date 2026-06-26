## Description: <br>
MasterChef helps agents answer recipe and ingredient questions by querying the api.yummy.chat recipe knowledge base and translating between English and Chinese when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yummy-chat](https://clawhub.ai/user/yummy-chat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up recipes by dish name or discover dishes from one to three ingredients. The skill sends translated Chinese dish or ingredient terms to api.yummy.chat and returns formatted recipe or dish results in the user's language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dish names or ingredient lists are sent to the disclosed api.yummy.chat external service. <br>
Mitigation: Avoid entering sensitive personal context and use clear recipe requests so the skill is invoked only when recipe lookup is intended. <br>
Risk: The API only accepts Chinese input and returns Chinese output, so translation errors can affect recipe or ingredient results. <br>
Mitigation: Review translated dish names, ingredient lists, cooking steps, and tips before relying on the returned recipe. <br>
Risk: Network or service errors can prevent recipe lookup or ingredient search. <br>
Mitigation: Handle unavailable API responses by asking the user to try again later or refine the dish or ingredient request. <br>


## Reference(s): <br>
- [MasterChef ClawHub page](https://clawhub.ai/yummy-chat/masterchef) <br>
- [api.yummy.chat base API](https://api.yummy.chat) <br>
- [Ingredient search endpoint](https://api.yummy.chat/ingredients) <br>
- [Recipe lookup endpoint](https://api.yummy.chat/howtocook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown recipe or dish results with JSON API calls executed through curl] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May translate user input to Chinese for the API and translate Chinese API responses back to the user's language.] <br>

## Skill Version(s): <br>
0.6.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
