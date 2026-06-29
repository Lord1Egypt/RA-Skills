## Description: <br>
Multi Agent Codegen uses a four-agent Plan, Write, Test, and Refine workflow to turn a natural-language software request into runnable Python code, tests, and review notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colbertlee](https://clawhub.ai/user/colbertlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they want an agent-assisted workflow to convert software, tool, or script requests into a single-file Python implementation with tests and a quality review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Python code and tests may be incorrect, incomplete, or unsafe to run without review. <br>
Mitigation: Review generated files and execute them in an isolated workspace before relying on the output. <br>
Risk: The CLI can install Python dependencies on first run and uses an API key for MiniMax-M3 calls. <br>
Mitigation: Review requirements and CLI behavior before execution, use a virtual environment, and provide only scoped EM_API_KEY or MINIMAX_API_KEY credentials. <br>
Risk: The server security review found no blocking signal but advises manual review of requested commands, network access, credentials, persistence, and broad file or account access. <br>
Mitigation: Inspect SKILL.md and scripts before installation, then scan and monitor the skill in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/colbertlee/multi-agent-codegen) <br>
- [Publisher profile](https://clawhub.ai/user/colbertlee) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files, Python code, pytest code, CLI text, and optional JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes plan.md, code.py, test_code.py, and refine.md under ~/.openclaw/workspace-coding-advisor/output/multi_agent_codegen; requires EM_API_KEY or MINIMAX_API_KEY for LLM calls.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
