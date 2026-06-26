## Description: <br>
Use the Labradoc CLI to authenticate and call Labradoc API endpoints for tasks, files, users, API keys, email, Google/Microsoft integrations, and billing from OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zamedic](https://clawhub.ai/user/zamedic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure Labradoc CLI authentication and perform account, document, task, email, integration, billing, and raw API operations from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose API tokens, OAuth codes, PKCE verifiers, or printed access tokens during authentication workflows. <br>
Mitigation: Treat credentials as secrets and avoid running token-printing or code-exchange commands in shared chats, logs, or CI. <br>
Risk: The skill can perform powerful Labradoc account and document actions, including uploads, email retrieval, billing, API-key changes, raw API requests, archive, and reprocess operations. <br>
Mitigation: Require explicit user confirmation before executing account-changing, billing, document mutation, email retrieval, or raw request commands. <br>
Risk: Installing an unpinned latest CLI binary can make behavior depend on a moving external release. <br>
Mitigation: Prefer a pinned Labradoc CLI release and verify its checksum before use. <br>


## Reference(s): <br>
- [Labradoc CLI Reference](references/labradoc-cli.md) <br>
- [Labradoc CLI Integrations](references/integrations.md) <br>
- [Labradoc Profile](https://labradoc.eu/profile) <br>
- [Labradoc CLI Releases](https://github.com/zamedic/labradoc-cli/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer to CLI commands that call external Labradoc services and can read or write local output files when the user requests file operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
