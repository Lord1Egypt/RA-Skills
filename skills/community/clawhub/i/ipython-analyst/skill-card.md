## Description:

Run Python interactively to analyze data, debug code, profile performance, validate schemas, process large files, and inspect ASTs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darkd](https://clawhub.ai/user/darkd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run interactive Python investigations for data analysis, debugging, profiling, schema validation, code inspection, log analysis, and large-file processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad interactive Python execution can run code with access to the active workspace.

Mitigation: Use the skill only for trusted analysis tasks and review code before execution.

Risk: Adding untrusted project directories to sys.path or checking requirements for attacker-controlled code can unexpectedly execute imported code.

Mitigation: Keep untrusted directories off sys.path and avoid check_requirements(script_path) for attacker-controlled files.

Risk: Debugging helpers can expose sensitive local variables or failing inputs.

Mitigation: Keep traceback locals disabled unless outputs remain private, and redact or synthesize sensitive inputs before saving them.

Risk: Helper behavior may read or write outside intended folders when given unsafe paths or baseline names.

Mitigation: Use simple baseline names and review file paths before running helpers that access the filesystem.

Risk: Installing Python packages can change the execution environment or introduce supply-chain risk.

Mitigation: Require explicit approval before any pip install.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darkd/skills/ipython-analyst)
- [Code Analysis Reference](references/code-analysis.md)
- [Data Analysis Reference](references/data-analysis.md)
- [Debugging Reference](references/debugging.md)
- [Distributed Processing Reference](references/distributed.md)
- [Environment & Session Reference](references/environment.md)
- [Machine Learning Reference](references/machine-learning.md)
- [Network Analysis Reference](references/network-analysis.md)
- [Schema Validation Reference](references/schema-validation.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, command snippets, diagnostic summaries, and generated file paths when outputs are saved]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce generated analysis files such as CSV, JSON, images, models, or reports when the user's task calls for downloadable outputs.]

## Skill Version(s):

7.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
