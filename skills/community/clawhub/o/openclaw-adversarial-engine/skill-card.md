## Description:

Adversarial Engine coordinates four LLM roles to debate a user topic, generate and test Python code, review security concerns, judge convergence, and optionally stream progress over WebSocket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timo2026](https://clawhub.ai/user/timo2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to run multi-model adversarial design reviews where an architect, engineer, security reviewer, and judge iterate toward a consensus. It is oriented toward technical proposal review, code-oriented validation, and real-time debate status updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unauthenticated network interfaces.

Mitigation: Bind services to localhost by default, add authentication before shared or internet-reachable use, and restrict CORS to trusted origins.

Risk: The security evidence reports automatic execution of model-generated Python under a misleading sandbox label.

Mitigation: Disable generated-code execution unless it runs in a real isolated sandbox with strict time, file-system, process, and network limits.

Risk: The security evidence reports an embedded API key.

Mitigation: Remove the embedded key, rotate the exposed credential, and load secrets only from a managed secret store or environment variable.

Risk: The security guidance warns that knowledge-base retrieval may expose local files to external model processing.

Mitigation: Enable retrieval only for approved files and document which data sources can be sent to external model providers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timo2026/skills/openclaw-adversarial-engine)
- [DashScope-compatible chat completions endpoint](https://coding.dashscope.aliyuncs.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-like debate transcripts, Python code blocks, WebSocket JSON status events, and saved session records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model reasoning, generated code, code execution results, token usage, latency, convergence score, and final consensus.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
