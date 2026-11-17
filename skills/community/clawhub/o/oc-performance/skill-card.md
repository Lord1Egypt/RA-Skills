## Description:

Performance analysis and optimization. Profiles code execution, identifies bottlenecks, and suggests optimizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Python and C/C++ code for performance issues, benchmark selected functions, and receive optimization suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically trusts a neighboring c-support/lib module when present, which can load code outside the reviewed artifact.

Mitigation: Install and run it only where that sibling directory is absent or controlled by trusted users; review that support code separately if present.

Risk: Security evidence says several advertised profiling, benchmarking, or analysis capabilities are broken or overstated.

Mitigation: Treat generated findings as advisory, test commands on representative code, and confirm recommendations before changing production code.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces advisory performance findings and suggested commands for profiling or benchmarking.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
