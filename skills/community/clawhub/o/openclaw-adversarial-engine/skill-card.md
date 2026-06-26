## Description: <br>
Adversarial Engine coordinates four model roles to debate designs, validate generated Python, use knowledge-base retrieval, stream progress, and stop when a judge model determines convergence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run multi-role adversarial reviews of architecture, implementation, and security tradeoffs, with optional generated-code execution and real-time debate updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run model-generated Python locally. <br>
Mitigation: Disable generated-code execution unless it runs in a real sandbox with strict filesystem, network, timeout, and process controls. <br>
Risk: The artifact contains an embedded API key. <br>
Mitigation: Remove or rotate the embedded key and provide credentials through a managed secret store or environment configuration. <br>
Risk: The local HTTP and WebSocket endpoints can start debate jobs without authentication. <br>
Mitigation: Bind services to localhost, add authentication, and restrict network exposure before use. <br>
Risk: Prompts and knowledge-base files may be sent to external model endpoints or stored locally. <br>
Mitigation: Avoid sensitive prompts or knowledge-base files unless local storage and external model transmission are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timo2026/openclaw-adversarial-engine) <br>
- [Publisher profile](https://clawhub.ai/user/timo2026) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text debate summaries with generated code snippets, execution results, and status events.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit real-time HTTP/WebSocket status updates when its local service components are used.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
