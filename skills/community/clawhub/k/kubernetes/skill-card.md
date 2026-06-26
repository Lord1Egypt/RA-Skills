## Description: <br>
Kubernetes Agent Swarm is an instruction-only multi-agent system for Kubernetes and OpenShift platform operations, covering orchestration, cluster operations, GitOps, security, observability, artifact management, and developer experience workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kcns008](https://clawhub.ai/user/kcns008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Platform engineers, SREs, and Kubernetes administrators use this skill to coordinate agent-guided cluster operations, GitOps deployments, security reviews, observability triage, artifact handling, and developer onboarding across Kubernetes and OpenShift environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents with live Kubernetes/OpenShift and optional cloud or registry authority. <br>
Mitigation: Use least-privilege kubeconfig, cloud, and registry credentials; scope access to non-production resources unless production access is explicitly required. <br>
Risk: Write, delete, secret, production, git, pull request, PagerDuty, Slack, and Teams actions can affect infrastructure or external incident workflows. <br>
Mitigation: Require explicit human approval before these actions and keep action logs for review. <br>
Risk: Broad repository commits such as git add -A can include unrelated or sensitive files. <br>
Mitigation: Use path-limited staging after human review, and inspect diffs before commit, push, or pull request creation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kcns008/kubernetes) <br>
- [Publisher Profile](https://clawhub.ai/user/kcns008) <br>
- [README](artifact/README.md) <br>
- [Swarm Configuration and Protocols](artifact/AGENTS.md) <br>
- [Quick Reference Operating Rules](artifact/QUICKREF.md) <br>
- [Troubleshooting Guide](artifact/troubleshooting/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands, YAML examples, checklists, and operational handoff notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no executable scripts are included.] <br>

## Skill Version(s): <br>
2.1.0 (source: server evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
