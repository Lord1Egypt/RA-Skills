## Description: <br>
Gpu Cluster Manager helps agents guide setup and operation of a local Ollama GPU cluster that discovers machines, routes inference requests, checks status, manages models, and troubleshoots failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local AI operators use this skill to install, monitor, and troubleshoot a self-hosted GPU cluster endpoint across macOS, Linux, and Windows machines. It is intended for users who want agent help with local inference routing, dashboard checks, and model management commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide users to run a local GPU cluster service that exposes a dashboard or API on the local machine or LAN. <br>
Mitigation: Confirm the intended network exposure before starting the service, and keep access limited to trusted local networks. <br>
Risk: Cluster operation may store local logs, latency data, and usage traces under the fleet-manager data directory. <br>
Mitigation: Review local retention and privacy expectations before sharing logs or using the service on sensitive workloads. <br>
Risk: Model pull and delete actions can transfer or remove large model files. <br>
Mitigation: Require explicit user confirmation before running pull or delete commands and verify the model name and target node. <br>
Risk: On macOS, meeting detection may observe camera or microphone activity state. <br>
Mitigation: Tell users about this behavior when enabling or troubleshooting meeting-aware routing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/gpu-cluster-manager) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, curl, SQL, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local service checks and model-management commands; user confirmation is required before restarting services or pulling/deleting models.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
