## Description: <br>
Uses the gitcode-api Python SDK for GitCode REST automation, including installation, OpenAI-style client structure, sync/async usage, repository-scoped helpers, and bundled CLI helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trenza1ore](https://clawhub.ai/user/trenza1ore) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to automate GitCode REST workflows with the gitcode-api Python SDK, including repository, pull request, user, search, and OAuth examples. It also helps agents validate the local environment and choose sync, async, or CLI usage patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses GitCode access tokens and can guide repository API operations. <br>
Mitigation: Use a least-privileged GitCode token, prefer environment variables over command-line token arguments, and keep tokens encrypted when supported. <br>
Risk: Repository write operations such as create, update, delete, merge, transfer, webhook, OAuth, or permission-changing actions can modify remote state. <br>
Mitigation: Require explicit user approval before any write or permission-changing action and review generated code or commands before execution. <br>
Risk: Installing the gitcode-api package can change the Python environment. <br>
Mitigation: Prefer a virtual environment and consider pinning the package version before installation. <br>


## Reference(s): <br>
- [GitCode API Reference](references/api-reference.md) <br>
- [GitCode API Workflow Patterns](references/workflow-patterns.md) <br>
- [Hosted SDK Quickstart](https://gitcode-api.readthedocs.io/en/latest/sdk/quickstart.html) <br>
- [GitCode API Documentation](https://gitcode-api.readthedocs.io/) <br>
- [gitcode-api on PyPI](https://pypi.org/project/gitcode-api/) <br>
- [Built-in CLI Documentation](https://gitcode-api.readthedocs.io/en/latest/sdk/cli.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON output examples from the helper CLI and response objects converted with to_dict().] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
