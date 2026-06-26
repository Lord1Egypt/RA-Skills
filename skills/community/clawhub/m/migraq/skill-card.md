## Description: <br>
MigraQ helps users plan Tencent Cloud migrations with cross-cloud resource scanning, specification matching, TCO analysis, and migration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haobinaa](https://clawhub.ai/user/haobinaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud architects, and migration teams use MigraQ to ask migration questions, compare source-cloud resources with Tencent Cloud targets, estimate TCO, and plan migration workflows. Authenticated mode is reserved for user-approved Tencent Cloud resource-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MigraQ can forward migration questions, inventories, billing details, and topology information to Tencent Cloud services. <br>
Mitigation: Share only information appropriate for Tencent Cloud processing, review prompts before sending, and clear sessions between unrelated projects. <br>
Risk: Authenticated mode can use local Tencent Cloud credentials for real create, modify, delete, cluster, or migration actions. <br>
Mitigation: Use least-privileged CAM keys, avoid persistent shell configuration for broad credentials when possible, and require explicit review of resources, costs, and rollback steps before execution. <br>


## Reference(s): <br>
- [MigraQChatCompletions API reference](references/api/MigraQChatCompletions.md) <br>
- [MigraQ ClawHub listing](https://clawhub.ai/haobinaa/migraq) <br>
- [Tencent Cloud migration API endpoint](https://cmg.ai.tencentcloudapi.com) <br>
- [Tencent Cloud MSP no-auth endpoint](https://msp.cloud.tencent.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON command results and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return a session_id for follow-up migration conversations; authenticated operations require Tencent Cloud AK/SK environment variables.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata; artifact frontmatter reports 1.1.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
