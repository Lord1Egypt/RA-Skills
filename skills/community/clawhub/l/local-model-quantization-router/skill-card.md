## Description:

Recommend local LLM model routes and quantization levels using hardware, privacy, task complexity, context size, and budget constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose local quantized model routes and cloud fallback posture before running OpenClaw workloads, especially for privacy, cost, context-size, and hardware-constrained deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional hardware input and output paths are user-directed file operations.

Mitigation: Use explicit paths for --hardware and --output and avoid pointing --output at important files.

Risk: Routing recommendations may be insufficient for quality-critical or very large-context workloads.

Mitigation: Review the returned fallback and risk notes before relying on the recommendation for deployment decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands]

**Output Format:** [JSON recommendations with human-readable routing evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write an optional JSON output file when the user provides an explicit output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
