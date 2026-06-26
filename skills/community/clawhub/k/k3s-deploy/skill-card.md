## Description: <br>
Automates K3s Kubernetes cluster deployment across multiple Linux servers, including image pre-pulling, network interface detection, CNI setup, and readiness checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuelin314-bot](https://clawhub.ai/user/xuelin314-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to deploy or repair K3s clusters on Linux hosts. It supports master and worker setup, CNI configuration, image pre-pull, and cluster health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer listed Linux servers and change cluster state broadly. <br>
Mitigation: Run first in a lab or maintenance window with backups and a rollback plan. <br>
Risk: Credentials, kubeconfig files, and cluster tokens require careful handling. <br>
Mitigation: Prefer SSH keys over password arguments and protect kubeconfig and token files. <br>
Risk: Host trust and installer supply chain choices affect deployment safety. <br>
Mitigation: Verify SSH host keys and review or pin the K3s installer before execution. <br>


## Reference(s): <br>
- [K3s Kubernetes Deploy release page](https://clawhub.ai/xuelin314-bot/k3s-deploy) <br>
- [K3s cluster troubleshooting guide](references/troubleshooting.md) <br>
- [K3s installer endpoint](https://get.k3s.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, Kubernetes configuration, and generated deployment artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deployment output may include cluster-info.md and deployment-log.txt.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
