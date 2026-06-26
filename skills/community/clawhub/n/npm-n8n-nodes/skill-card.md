## Description: <br>
Build, structure, and publish npm packages for n8n custom community nodes, including node scaffolding, credentials, HTTP handling, testing, and npm publishing guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build and publish n8n community node packages, including node files, credential definitions, local testing, and npm release preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential examples can be copied into real n8n nodes and adapted in ways that expose API keys, OAuth tokens, or wallet-related secrets. <br>
Mitigation: Use n8n credential types that mask secrets, prefer header-based authentication over query-string keys, avoid logging full credential objects or tokens, and scope npm, API, and OAuth tokens tightly. <br>
Risk: Publishing guidance may affect packages released to npm and used in live n8n workflows. <br>
Mitigation: Review package contents before publishing, run build and lint checks, verify the n8n package metadata, and test locally before release. <br>


## Reference(s): <br>
- [Skill source](artifact/SKILL.md) <br>
- [Programmatic node example](references/examples/nodes/programmatic-node.md) <br>
- [Declarative node example](references/examples/nodes/declarative-node.md) <br>
- [Trigger node example](references/examples/nodes/trigger-node.md) <br>
- [Webhook node example](references/examples/nodes/webhook-node.md) <br>
- [API key credential patterns](references/examples/credentials/api-key-patterns.md) <br>
- [OAuth2 credential patterns](references/examples/credentials/oauth2-patterns.md) <br>
- [HTTP requests and binary data](references/concepts/http-and-binary.md) <br>
- [Error handling](references/concepts/error-handling.md) <br>
- [Project files template](references/templates/project-files.md) <br>
- [Local testing](references/templates/local-testing.md) <br>
- [Publishing](references/templates/publishing.md) <br>
- [Common gotchas](references/gotchas/common-gotchas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include npm package structure, n8n node and credential snippets, local testing steps, and publishing checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
