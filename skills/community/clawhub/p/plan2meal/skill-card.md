## Description: <br>
Manage recipes and grocery lists in Plan2Meal via chat, including adding recipe URLs, listing, searching, showing, and deleting recipes, and creating or managing grocery lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okikeSolutions](https://clawhub.ai/user/okikeSolutions) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Plan2Meal users and agents use this skill to authenticate and manage stored recipes and grocery lists through Plan2Meal commands. It is intended for explicit Plan2Meal recipe or grocery-list actions, not general cooking advice or nutrition coaching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recipe, grocery-list, and authentication traffic is routed to the configured Convex backend, and users can opt in to a shared default backend. <br>
Mitigation: Prefer a private CONVEX_URL for private use, review OAuth scopes and callback URLs, and enable ALLOW_DEFAULT_BACKEND only when shared-backend routing is acceptable. <br>
Risk: OAuth credentials and access tokens are required for Plan2Meal commands. <br>
Mitigation: Store provider credentials in environment variables, protect secrets and tokens, and avoid exposing them in agent responses. <br>


## Reference(s): <br>
- [Plan2Meal Skill Definition](SKILL.md) <br>
- [Plan2Meal README](README.md) <br>
- [Plan2Meal Output Templates](references/output-templates.md) <br>
- [ClawHub Plan2meal Page](https://clawhub.ai/okikeSolutions/plan2meal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text responses with command examples, IDs, links, counts, and error messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OAuth login links, recipe or grocery-list IDs, backend or configuration errors, and data-routing disclosures.] <br>

## Skill Version(s): <br>
1.2.5 (source: evidence.release.version, package.json, and src/index.ts) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
