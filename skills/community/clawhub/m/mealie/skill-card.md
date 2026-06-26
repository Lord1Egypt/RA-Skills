## Description: <br>
Interact with a self-hosted Mealie recipe manager through its REST API to manage recipes, meal plans, and shopping lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[g1mb01d](https://clawhub.ai/user/g1mb01d) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Mealie users can use this skill to automate recipe import, recipe lookup, meal-plan creation, and shopping-list retrieval against a self-hosted Mealie instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can upload local JSON files and create or modify persistent Mealie resources. <br>
Mitigation: Inspect the payload file and target URL before running write commands, and require explicit confirmation for add-recipe or create-plan operations. <br>
Risk: The Mealie API token grants account access and could be exposed through chat logs or shared shell history. <br>
Mitigation: Keep MEALIE_TOKEN out of prompts and shared logs, store it only in the execution environment, and rotate it if exposure is suspected. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEALIE_URL and MEALIE_TOKEN environment variables and may perform write operations against the configured Mealie account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
