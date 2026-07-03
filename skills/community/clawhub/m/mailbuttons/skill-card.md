## Description: <br>
Wire up a governed email inbox for an AI agent using Mailbuttons, with sandbox-only setup, policy-gated send and receive flows, stack-specific scaffolded code, and human approval for production or external sending. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mailbuttons](https://clawhub.ai/user/mailbuttons) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add a Mailbuttons sandbox inbox to an AI agent, generate and review an email policy, scaffold framework-specific send and inbound handling code, and run a sandbox self-test before requesting human approval to go live. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbuttons sandbox API keys or account keys could be exposed if copied into generated files or prompts. <br>
Mitigation: Read credentials from environment variables, keep secrets out of generated code, and stop on authentication errors rather than retrying blindly. <br>
Risk: An agent could be asked to bypass sandbox limits, external-send approval, sender allowlists, or production promotion controls. <br>
Mitigation: Use proposal and promotion request flows only; do not grant capabilities, widen token scope, enable external sending, or approve production changes from the agent. <br>
Risk: Inbound email content can contain unsafe instructions or quarantined data that should not control the agent. <br>
Mitigation: Treat inbound text as untrusted data, rely on governed reads, and do not retrieve or reconstruct withheld quarantined message bodies. <br>


## Reference(s): <br>
- [Mailbuttons](https://mailbuttons.com) <br>
- [Mailbuttons Developer Documentation](https://mailbuttons.com/developers) <br>
- [Wiring Mailbuttons into a Claude Agent SDK app](references/claude-agent-sdk.md) <br>
- [Wiring Mailbuttons into a LangChain / LangGraph app](references/langchain.md) <br>
- [Wiring Mailbuttons into plain TypeScript or Python](references/plain-sdk.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with inline code examples and generated configuration or scaffold files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MAILBUTTONS_API_KEY from the environment and keeps generated integrations sandbox-only until a human approves promotion.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
