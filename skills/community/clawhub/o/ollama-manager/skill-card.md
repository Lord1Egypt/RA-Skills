## Description: <br>
Manage Ollama models across multiple machines by inspecting loaded and stored models, disk usage, usage history, fleet health, and recommendations for model placement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage local Ollama fleets, review model inventory and performance, and prepare pull or delete actions with explicit confirmation before changes are made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pulling Ollama models can consume substantial bandwidth and disk space. <br>
Mitigation: Ask for explicit user confirmation before pull actions and review the target model, node, and expected resource impact. <br>
Risk: Deleting a model can remove local availability for workloads that still depend on it. <br>
Mitigation: Show the exact model, target node, and disk space to be freed before requesting confirmation to delete. <br>
Risk: The local management endpoint can expose fleet state or allow management actions if reachable by untrusted users. <br>
Mitigation: Run the router and nodes only on machines the user controls and keep the localhost management endpoint protected. <br>
Risk: The skill depends on the third-party ollama-herd package and repository. <br>
Mitigation: Install and run it only when the user trusts that package and repository. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/twinsgeeks/ollama-manager) <br>
- [ollama-herd package](https://pypi.org/project/ollama-herd/) <br>
- [ollama-herd repository](https://github.com/geeks-accelerator/ollama-herd) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, analysis] <br>
**Output Format:** [Markdown with inline bash and SQL command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target local Ollama Herd endpoints and local fleet-manager data paths.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
