## Description: <br>
Recommend local LLM model routes and quantization levels using hardware, privacy, task complexity, context size, and budget constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide whether an OpenClaw workload should run on a local quantized model, start local with fallback, or require cloud escalation. It considers hardware capacity, privacy posture, task complexity, context length, and budget-sensitive routing tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task text and hardware inputs are echoed in the script's JSON output, which can expose sensitive workload details if used with confidential prompts or shared output files. <br>
Mitigation: Do not include secrets, customer content, or sensitive task details in --task, and choose --output paths deliberately. <br>
Risk: Malformed or untrusted hardware JSON can stop the routing script or produce inappropriate recommendations. <br>
Mitigation: Review hardware JSON before use and validate that memory, VRAM, and cpu_only values reflect the target machine. <br>
Risk: Routing guidance can be insufficient for critical workloads that need higher-quality evaluation or human oversight. <br>
Mitigation: Use the recommended fallback path, including cloud premium models with human review when the task is critical and privacy constraints allow escalation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevojarvisai-star/local-model-quantization-router) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON] <br>
**Output Format:** [Markdown guidance for agents plus JSON route recommendations from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script can print recommendations to stdout and optionally write the same JSON to a caller-selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, released 2026-04-30) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
