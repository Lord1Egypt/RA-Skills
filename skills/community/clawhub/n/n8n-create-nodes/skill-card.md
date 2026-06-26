## Description: <br>
Build production-ready n8n community nodes as npm packages, covering declarative and programmatic node styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rwilson504](https://clawhub.ai/user/rwilson504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold, implement, test, and publish n8n community node packages, including node classes, credentials, triggers, package configuration, and publishing steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated n8n nodes may handle OAuth tokens, API keys, or other service credentials. <br>
Mitigation: Prefer Authorization or custom headers for API keys, keep OAuth scopes minimal, use query-string secrets only when an API requires them, and avoid storing secrets in workflow static data. <br>
Risk: Generated packages commonly start from a cloned starter repository and npm dependencies. <br>
Mitigation: Review cloned source and dependencies before use, then build and test the package locally before publishing or installing it in a live n8n environment. <br>
Risk: Credential examples can lead to unsafe handling if copied without review. <br>
Mitigation: Review generated credential files for secret masking, authentication placement, and scope before connecting real services. <br>


## Reference(s): <br>
- [N8n Create Nodes source](https://github.com/rwilson504/agent-skills/tree/main/n8n-create-nodes) <br>
- [n8n Nodes Starter](https://github.com/n8n-io/n8n-nodes-starter.git) <br>
- [Credential Patterns](references/CREDENTIAL_PATTERNS.md) <br>
- [Trigger Patterns](references/TRIGGER_PATTERNS.md) <br>
- [Examples](references/EXAMPLES.md) <br>
- [Common Mistakes](references/COMMON_MISTAKES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with TypeScript, JSON, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces development guidance and implementation patterns for n8n node packages; the skill itself does not execute generated commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
