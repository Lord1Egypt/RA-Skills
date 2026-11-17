## Description:

Unified GPU kernel operator generation and optimization skill that detects FlagGems, vLLM, or general Python/Triton repositories and routes generation, optimization, platform specialization, MCP setup, and feedback workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wbavon](https://clawhub.ai/user/wbavon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate, optimize, test, benchmark, and specialize GPU/Triton kernel operators for FlagGems, vLLM, or general Python/Triton repositories. It can also guide KernelGen MCP setup and collect feedback for issue or email submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kernel source and repository details may be sent to the external KernelGen MCP service.

Mitigation: Use only repositories that are appropriate for external processing, remove secrets before use, and review what context will be submitted.

Risk: The workflow may store a bearer token in a project-local MCP configuration file.

Mitigation: Keep .mcp.json and related agent configuration files out of version control, scope tokens narrowly, and rotate tokens if exposed.

Risk: The agent may edit repository files and execute generated code, tests, or benchmarks.

Mitigation: Run the skill on a clean branch or disposable workspace, inspect diffs, and review generated code before execution.

Risk: Optional pull request, issue, email, or chat publishing can disclose generated files or project details.

Mitigation: Decline publishing steps until the destination, files, and message contents have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wbavon/skills/kernelgen-flagos)
- [KernelGen Skills User Guide](https://docs.flagos.io/projects/kernelgen/en/latest/skills_user_guide/skills-user-guide.html#)
- [FlagGems installation guide](https://docs.flagos.io/projects/FlagGems/en/latest/getting_started/install.html#)
- [vLLM installation guide](https://docs.vllm.ai/en/latest/getting_started/installation/)
- [FlagGems reference repository](https://github.com/FlagOpen/FlagGems)
- [Ascend Triton development documentation](https://www.hiascend.com/document)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated or modified source files, tests, benchmarks, reports, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Triton kernels, PyTorch baselines, tests, benchmark files, integration reports, MCP configuration guidance, pull request links, or feedback drafts depending on the selected workflow.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
