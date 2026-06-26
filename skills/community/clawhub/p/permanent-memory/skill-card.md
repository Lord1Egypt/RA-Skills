## Description: <br>
Auto Memory stores agent decisions, identity, and context as a permanent memory chain on the Autonomys Network that can be rebuilt from a single CID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xautonomys](https://clawhub.ai/user/0xautonomys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to upload files, save durable agent memories, and recall linked memory chains from Autonomys-backed CIDs after local state loss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved memories and uploaded files are permanent and public by default. <br>
Mitigation: Do not upload API keys, tokens, private keys, personal data, regulated data, confidential documents, or conversation history that may need deletion unless it has been minimized and encrypted first. <br>
Risk: A recalled memory chain can restore incorrect, unwanted, or sensitive prior context. <br>
Mitigation: Review the exact content and CID before saving or restoring a chain. <br>
Risk: Uploads, memory saves, and chain recall depend on AUTO_DRIVE_API_KEY. <br>
Mitigation: Configure and verify the API key before relying on the skill, and use the public gateway only for general downloads when appropriate. <br>
Risk: Free-tier uploads are limited to 20 MB per month on mainnet. <br>
Mitigation: Check remaining credits before large or repeated uploads and keep individual uploads well under the monthly limit. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/0xautonomys/permanent-memory) <br>
- [Auto Drive API Reference](references/automemory-api.md) <br>
- [Autonomys Network Overview](references/autonomys-network.md) <br>
- [Memory Chain & Resurrection Pattern](references/memory-chain.md) <br>
- [Auto Drive API Docs](https://mainnet.auto-drive.autonomys.xyz/api/docs) <br>
- [Auto Drive SDK Docs](https://develop.autonomys.xyz/sdk/auto-drive/overview_setup) <br>
- [Autonomys Agents Framework](https://github.com/autonomys/autonomys-agents) <br>
- [OpenClaw Memory Chain Example](https://github.com/autojeremy/openclaw-memory-chain) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Files, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AUTO_DRIVE_API_KEY for uploads, memory saves, and chain recall; downloads can use the public gateway without an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
