## Description: <br>
分布式AI节点系统，实现跨局域网节点的任务分发、并行处理和结果聚合 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fqch1981](https://clawhub.ai/user/fqch1981) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Neuron to distribute complex prompts across trusted local-network nodes, collect parallel responses, and aggregate them into a final answer. It is most useful for multi-perspective reasoning, large analysis tasks, or environments where different trusted nodes hold different context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and results may be shared with unauthenticated peers on the local network. <br>
Mitigation: Use the skill only on trusted LANs where every peer is controlled or trusted. <br>
Risk: Sensitive, proprietary, regulated, or private prompts may be exposed to peer nodes. <br>
Mitigation: Do not use the skill for secrets or sensitive data; use distribute=false for local-only work. <br>
Risk: Network exposure can broaden who can discover or interact with the skill. <br>
Mitigation: Do not expose the discovery port outside a trusted LAN. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fqch1981/neuron) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/fqch1981) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text or Markdown with inline Python, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return local-only answers when distribution is disabled, aggregated answers from peer nodes when distribution is enabled, and node status or task-memory data through the Python API.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and scripts/__init__.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
