## Description: <br>
Provides a Windows-focused deployment guide for local OpenClaw memory search using nomic-embed-text, memorySearch configuration, Nomic Atlas visualization, and intranet troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure local semantic memory search for OpenClaw, install the memory-tencentdb plugin, verify readiness, and troubleshoot Windows or intranet deployment issues. It also provides optional guidance for Nomic Atlas memory visualization and remote embedding fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional remote embedding configuration can send memory content or search queries outside the local machine. <br>
Mitigation: Prefer the local embedding setup for sensitive memory data; use a remote endpoint only after confirming it is trusted, approved, and appropriate for the data being processed. <br>
Risk: The guide includes configuration and system file edits that can affect OpenClaw memory search behavior. <br>
Mitigation: Review the OpenClaw configuration changes before applying them and verify the deployment with `openclaw memory status`. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/paudyyin/node-llama-cpp-install-guide) <br>
- [nomic-embed-text-v1.5 GGUF mirror](https://hf-mirror.com/nomic-ai/nomic-embed-text-v1.5-GGUF/resolve/main/nomic-embed-text-v1.5.Q4_K_M.gguf) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with PowerShell, bash, batch, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output for local memory search deployment and troubleshooting.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
