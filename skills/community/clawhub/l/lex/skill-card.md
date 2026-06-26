## Description: <br>
Build original LangGraph agents for Warden Protocol and prepare them for publishing in Warden Studio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kulotzkih](https://clawhub.ai/user/kulotzkih) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create, test, and deploy original LangGraph-based Warden Protocol agents, including API-accessible Web3 and automation agents intended for Warden Studio publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated dependency files may introduce packages that should be reviewed before installation. <br>
Mitigation: Review generated manifests and dependency versions before running package installation commands. <br>
Risk: The initializer creates files in the selected workspace. <br>
Mitigation: Run scaffolding only in an intended project directory and inspect generated files before committing or deploying them. <br>
Risk: Agent setup and deployment workflows require API keys and environment variables. <br>
Mitigation: Keep .env files and real API keys out of source control, use deployment secret stores where possible, and avoid logging secrets. <br>
Risk: Testing deployed agents against untrusted endpoints or with real credentials can expose sensitive data. <br>
Mitigation: Use trusted endpoints, least-privilege test credentials, and avoid sending raw production prompts or secrets during validation. <br>
Risk: Warden Phase 1 limitations prohibit user wallet access and storing data on Warden infrastructure. <br>
Mitigation: Confirm generated agents do not access user wallets or persist data on Warden infrastructure before Warden Studio publication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kulotzkih/lex) <br>
- [Warden Community Agents Repository](https://github.com/warden-protocol/community-agents) <br>
- [Warden Protocol Documentation](https://docs.wardenprotocol.org) <br>
- [LangSmith](https://smith.langchain.com) <br>
- [Deployment Guide](references/deployment-guide.md) <br>
- [Installation Guide](references/installation-guide.md) <br>
- [LangGraph Patterns](references/langgraph-patterns.md) <br>
- [Quick Reference](references/quick-reference.md) <br>
- [Example Configurations](assets/example-configs.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, and generated project files when helper scripts are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports TypeScript and Python LangGraph agent scaffolding, deployment guidance, and endpoint testing workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
