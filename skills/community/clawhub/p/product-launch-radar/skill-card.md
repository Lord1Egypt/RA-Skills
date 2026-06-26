## Description: <br>
Automatically tracks product launches across industry sources, filters for high-value items, and prioritizes updates for decision-makers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, investors, technical leaders, and market analysts use this skill to monitor product-launch signals, filter noisy updates, and receive concise daily or weekly briefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled and webhook-triggered notifications can send summaries to configured channels without enough clarity about webhook access controls. <br>
Mitigation: Require authenticated webhook access, review cron schedules, and confirm notification recipients before enabling automated runs. <br>
Risk: Feishu webhook URLs and email recipient settings may expose sensitive routing or credentials if handled carelessly. <br>
Mitigation: Store notification secrets in protected environment variables and restrict access to channel configuration. <br>
Risk: The release metadata includes high-impact capability tags for crypto and purchases that are not explained by the skill behavior. <br>
Mitigation: Verify the need for those capability tags and remove or reject them before deployment if they are not required. <br>
Risk: The skill depends on other aggregation, audit, and notification skills to fetch sources, score content, and deliver messages. <br>
Mitigation: Review dependent skills and their permissions before using this workflow in a shared or production environment. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/zlszhonglongshen/product-launch-radar) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Usage Examples](artifact/examples.md) <br>
- [Workflow Configuration](artifact/workflow.json) <br>
- [Runtime Configuration](artifact/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown briefs, reports, configuration updates, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prioritized launch summaries, source links, scores, notification routing, and schedule configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
