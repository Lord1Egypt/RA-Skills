## Description: <br>
Python package creation and PyPI distribution via pyproject.toml and entry points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create distributable Python libraries and CLI tools, configure pyproject.toml and entry points, and build or publish packages with uv and PyPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing commands or CI workflows could upload unintended artifacts or publish to the wrong registry. <br>
Mitigation: Confirm the target registry, inspect built artifacts, and use TestPyPI first when possible before publishing. <br>
Risk: PyPI or release credentials used in copied workflows could be broader than necessary. <br>
Mitigation: Protect release permissions and scope PyPI tokens narrowly before adopting any workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-parseltongue-python-packaging) <br>
- [OpenClaw Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/parseltongue) <br>
- [TestPyPI](https://test.pypi.org/legacy/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash, TOML, YAML, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes examples for pyproject.toml, uv workflows, entry points, and GitHub Actions publishing pipelines.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
