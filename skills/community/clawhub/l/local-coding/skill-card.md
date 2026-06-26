## Description: <br>
Local Coding helps developers run local code-focused models across a device fleet for code generation, review, refactoring, and debugging through OpenAI-compatible tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route coding tasks to local models such as Codestral, DeepSeek-Coder, StarCoder, and Qwen-Coder while keeping prompts and code on their own network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local prompts, code, or traces may remain in logs or configuration under ~/.fleet-manager/. <br>
Mitigation: Avoid sending secrets in prompts and review local retention, permissions, and cleanup practices before use. <br>
Risk: The local router is intended for trusted local networks and could expose coding prompts if made broadly reachable. <br>
Mitigation: Run it only on trusted networks and restrict access to the local API endpoint. <br>
Risk: Installing or running the underlying local AI router depends on a third-party package. <br>
Mitigation: Verify the ollama-herd package and publisher before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/local-coding) <br>
- [PyPI: ollama-herd](https://pypi.org/project/ollama-herd/) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [API Reference](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, Python, JSON, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl or wget; optionally uses python3 and pip; supports macOS, Linux, and Windows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
