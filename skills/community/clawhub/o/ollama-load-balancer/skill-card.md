## Description: <br>
Guides agents through deploying and operating an Ollama load balancer for distributed Llama, Qwen, DeepSeek, and Mistral inference with mDNS discovery, health checks, queue management, failover, retry, and cleanup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy, query, monitor, and troubleshoot an Ollama load-balanced inference fleet across multiple machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and operating the load balancer affects a local Ollama fleet and stores latency data and logs under ~/.fleet-manager. <br>
Mitigation: Install only for intended fleet management, review the PyPI package source before use, and account for persistent local operational data. <br>
Risk: Model pull and delete actions can consume substantial storage or remove models from load balancer nodes. <br>
Mitigation: Require explicit confirmation before pulling or deleting models. <br>
Risk: Restarting or stopping load balancer services can disrupt active inference workloads. <br>
Mitigation: Confirm before restarting or stopping services, and report offline nodes instead of attempting remote access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twinsgeeks/ollama-load-balancer) <br>
- [ollama-herd package](https://pypi.org/project/ollama-herd/) <br>
- [ollama-herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions] <br>
**Output Format:** [Markdown with bash, Python, and SQL snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may query local load balancer APIs and persistent data under ~/.fleet-manager.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
