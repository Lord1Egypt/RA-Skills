## Description: <br>
Generate identity-consistent selfies, group photos, and other SFW images for OpenClaw characters via the tuqu.ai API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouyi531](https://clawhub.ai/user/zhouyi531) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to generate character-consistent selfies, portraits, group photos, preset-based images, and SFW image edits through Tuqu API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, face photos, and role-specific service keys may be sent to the Tuqu provider. <br>
Mitigation: Install only if the Tuqu provider is trusted, keep service keys explicit per role, and clarify retention and deletion expectations before uploading real face photos. <br>
Risk: Service keys may be exposed if callers use absolute URLs, custom base URLs, or query-string credentials. <br>
Mitigation: Use the documented Tuqu hosts by default and avoid absolute URLs, custom base URLs, and query-string credentials unless the destination has been reviewed. <br>
Risk: Paid generation, recharge, and deletion workflows can spend credits or remove stored data. <br>
Mitigation: Require explicit user confirmation before paid generation, recharge, or deletion, and check pricing or balance before cost-sensitive requests. <br>


## Reference(s): <br>
- [OpenClaw Selfie on ClawHub](https://clawhub.ai/zhouyi531/openclaw-selfie) <br>
- [Publisher profile](https://clawhub.ai/user/zhouyi531) <br>
- [tuqu.ai](https://tuqu.ai) <br>
- [Tuqu API Notes](TUQU_API.md) <br>
- [Endpoint Reference](references/endpoints.md) <br>
- [Workflow Recipes](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide authenticated API calls that return JSON fields such as imageUrl, promptUsed, model, remainingBalance, transactionId, historyItem, checkoutUrl, or payment artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
