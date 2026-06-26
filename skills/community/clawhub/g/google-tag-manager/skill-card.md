## Description: <br>
Manage Google Tag Manager containers, tags, triggers, variables, versions, and publishing workflows through the GTM API v2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonfunk](https://clawhub.ai/user/simonfunk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and marketing operations engineers use this skill to inspect and administer GTM accounts, containers, workspaces, tags, triggers, variables, versions, and publishing workflows from an agent-assisted shell workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, version, and publish live GTM resources. <br>
Mitigation: Require manual review before delete, update, create-version, or publish operations against production containers. <br>
Risk: The skill uses sensitive Google credentials to administer GTM. <br>
Mitigation: Use a least-privilege service account and keep the JSON key out of prompts and repositories. <br>


## Reference(s): <br>
- [GTM API v2 Quick Reference](references/api-reference.md) <br>
- [GTM Recipes](references/recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided GTM account, container, and Google credential configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
