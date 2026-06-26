## Description: <br>
Detect provider models, deduplicate them, remove unusable ones, register missing models into OpenClaw, and safely keep provider-native model ids/names during model catalog sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zqh2333](https://clawhub.ai/user/zqh2333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to keep OpenClaw model catalogs aligned with provider model lists, remove unusable models, and validate registry changes before scheduling automated sync jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite OpenClaw model configuration and remove unusable models from the registered catalog. <br>
Mitigation: Run a dry-run sync first, back up ~/.openclaw/openclaw.json, and review proposed additions and removals before applying changes. <br>
Risk: The sync and validation scripts use provider credentials to query model and chat-completions endpoints. <br>
Mitigation: Install only in environments where the agent is allowed to access provider API keys, and limit credential scope where the provider supports it. <br>
Risk: The recurring sync job can restart the OpenClaw gateway after updates. <br>
Mitigation: Enable recurring sync and restart behavior only after one successful sync, one successful validation run, and confirmation that primary and fallback settings are correct. <br>
Risk: The skill may write reusable operational notes to .learnings after debugging or corrections. <br>
Mitigation: Disable or require approval for .learnings writes in workspaces that may contain sensitive information. <br>


## Reference(s): <br>
- [Model Sync Policy](references/model-sync-policy.md) <br>
- [Model Sync Policy JSON](references/model-sync-policy.json) <br>
- [API Failover Upgrade Notes](references/api-failover-upgrade.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, code] <br>
**Output Format:** [Markdown guidance with shell commands, JavaScript helper scripts, JSON policy, and generated sync or validation reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce OpenClaw configuration updates and model-registry reports after validation.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
