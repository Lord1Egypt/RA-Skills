## Description: <br>
Unified GPU kernel operator generation and optimization skill that detects FlagGems, vLLM, or general Python/Triton repositories and routes generation, optimization, specialization, MCP setup, and feedback workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wbavon](https://clawhub.ai/user/wbavon) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and GPU kernel engineers use this skill to generate, optimize, specialize, test, and integrate Triton operators for FlagGems, vLLM, or general Python/Triton repositories. It requires careful review because the release evidence says it can store a KernelGen MCP token, install packages, execute shell commands, edit project code, and optionally publish or share results externally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill can store a KernelGen MCP token in project configuration. <br>
Mitigation: Keep tokens out of committed files, restrict repository access, and rotate or remove the token when it is no longer needed. <br>
Risk: The security evidence says the skill can install packages, execute shell commands, and edit project code. <br>
Mitigation: Run it in a controlled branch or disposable workspace, review diffs, and run the relevant tests before accepting changes. <br>
Risk: The security evidence and artifact behavior show optional PR, chat, issue, or email sharing paths. <br>
Mitigation: Decline external sharing for sensitive repositories and review all generated content before submitting it outside the workspace. <br>


## Reference(s): <br>
- [KernelGen Skills User Guide](https://docs.flagos.io/projects/kernelgen/en/latest/skills_user_guide/skills-user-guide.html#) <br>
- [FlagGems Installation Guide](https://docs.flagos.io/projects/FlagGems/en/latest/getting_started/install.html#) <br>
- [vLLM Installation Guide](https://docs.vllm.ai/en/latest/getting_started/installation/) <br>
- [FlagGems Repository](https://github.com/FlagOpen/FlagGems) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated source files, tests, benchmarks, configuration snippets, and integration reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated or modified project files should be reviewed and tested before use.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; skill frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
