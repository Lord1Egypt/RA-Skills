## Description: <br>
Build and deploy autonomous TypeScript agents for the OpenServ platform using the OpenServ SDK, companion OpenServ client, runnable and runless capabilities, platform-delegated generation, and workflow provisioning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[issa-me-sush](https://clawhub.ai/user/issa-me-sush) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to create, provision, run, deploy, and troubleshoot OpenServ agents that expose capabilities, handle platform tasks, use platform-delegated generation, and participate in workflows or paid x402 calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may rely on local secrets such as wallet private keys, OpenServ API keys, auth tokens, and optional LLM provider keys. <br>
Mitigation: Keep .env files and wallet keys out of version control, restrict local secret access, and rotate any exposed tokens. <br>
Risk: Local development can expose an agent through a WebSocket tunnel, and production agents can expose public endpoints. <br>
Mitigation: Review webhook and tunnel exposure before running agents, and use DISABLE_TUNNEL=true with a controlled public endpoint for production deployments. <br>
Risk: Capabilities can delete files, trigger paid x402 calls, or perform on-chain ERC-8004 registration that requires funded wallets. <br>
Mitigation: Add authorization or confirmation checks around file deletion, paid, and on-chain actions, and wrap registration in error handling so failures do not prevent the agent from starting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/issa-me-sush/openserv-agent-sdk) <br>
- [OpenServ SDK Reference](reference.md) <br>
- [OpenServ SDK Troubleshooting](troubleshooting.md) <br>
- [Basic agent example](examples/basic-agent.ts) <br>
- [Task management example](examples/task-management.ts) <br>
- [File operations example](examples/file-operations.ts) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, shell, JSON, and environment-variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes agent setup patterns, SDK/API usage examples, deployment notes, troubleshooting guidance, and security-sensitive credential handling notes.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
