## Description: <br>
为 K8s 初学者提供 Kubernetes 集群部署指导，支持 AllinOne 快速体验和生产环境高可用部署。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to plan, configure, deploy, validate, and troubleshoot Kubernetes clusters with kubeasz for both single-node learning environments and multi-node high-availability deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose powerful Kubernetes and Linux administration commands for real nodes. <br>
Mitigation: Review each command before execution, confirm the target hosts and cluster context, and use backups plus a maintenance plan for production systems. <br>
Risk: SSH keys, service tokens, and cluster-admin Dashboard access can grant broad control over a cluster. <br>
Mitigation: Use dedicated and revocable SSH keys, restrict token scope and lifetime, and avoid cluster-admin Dashboard tokens unless explicitly required. <br>
Risk: Downloaded scripts, manifests, and container assets may affect node or cluster integrity. <br>
Mitigation: Verify source URLs and downloaded artifacts before use, especially when pulling scripts or manifests from external locations. <br>
Risk: Firewall changes and destroy or redeploy steps can interrupt or remove production workloads. <br>
Mitigation: Avoid disabling firewalls outside isolated test networks and do not run destroy, restore, or redeploy steps on production clusters without backups and explicit approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/kubeasz-deploy) <br>
- [kubeasz project homepage](https://github.com/easzlab/kubeasz) <br>
- [kubeasz documentation](https://github.com/easzlab/kubeasz/tree/master/docs) <br>
- [kubeasz issues](https://github.com/easzlab/kubeasz/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include privileged Kubernetes, Docker, SSH, firewall, and node administration commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
