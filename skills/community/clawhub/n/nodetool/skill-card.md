## Description: <br>
Nodetool is a local-first, AGPL-3.0 visual AI workflow builder that combines ComfyUI-style nodes with n8n-style automation for LLM agents, RAG pipelines, and multimodal data flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georgi](https://clawhub.ai/user/georgi) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate Nodetool for local AI workflow execution, package documentation, model cache management, chat or server operation, proxying, and cloud deployment tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote and silent installer commands can run upstream code without interactive review. <br>
Mitigation: Download and review installers first, use pinned releases or checksums when available, and reserve silent installation for controlled environments. <br>
Risk: Auth tokens, settings, and secrets may be exposed through shell history, logs, or displayed settings output. <br>
Mitigation: Avoid pasting real tokens into commands, use environment or secret-management practices, and require explicit confirmation before showing secrets. <br>
Risk: Server, proxy, background job, synchronization, and deployment commands can expose services or change cloud resources. <br>
Mitigation: Confirm intent before starting public servers or proxies, launching background jobs, syncing data, or applying and destroying deployments. <br>


## Reference(s): <br>
- [Nodetool homepage](https://nodetool.ai) <br>
- [ClawHub Nodetool release page](https://clawhub.ai/georgi/nodetool) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that install software, start local services, manage secrets, run background jobs, synchronize data, or apply and destroy cloud deployments.] <br>

## Skill Version(s): <br>
0.6.3 (source: server release metadata; artifact package.json reports 0.6.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
