## Description: <br>
Interact with Mealie recipe manager (recipes, shopping lists, meal plans). Self-hosted recipe and meal planning API client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angusthefuzz](https://clawhub.ai/user/angusthefuzz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and home-lab operators use this skill to let an agent inspect and manage recipes, shopping lists, and meal plans in a trusted Mealie instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Mealie API token to change or delete recipes, shopping-list items, and meal plans. <br>
Mitigation: Use the least-privileged Mealie token available and review agent requests before allowing edit or delete commands. <br>
Risk: A token configured for an untrusted or insecure Mealie instance could expose recipe and household planning data. <br>
Mitigation: Install this only for a Mealie instance you trust, store the token in the documented environment file, and use HTTPS where possible. <br>


## Reference(s): <br>
- [Mealie](https://mealie.io) <br>
- [Mealie API documentation](https://docs.mealie.io) <br>
- [ClawHub release page](https://clawhub.ai/angusthefuzz/mealie-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node plus MEALIE_URL and MEALIE_API_TOKEN environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
