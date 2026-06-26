## Description: <br>
Use this skill if your uncertainty with a package's API is > 5% to create a deterministic, versioned mirror of the package repo with a built-in coordinate system, installed as an additional skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amberlee2427](https://clawhub.ai/user/amberlee2427) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create local, versioned mirrors of Python package source so an agent can inspect exact classes, functions, signatures, docstrings, and line ranges when package API behavior is uncertain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads arbitrary PyPI source and creates persistent local agent skills. <br>
Mitigation: Run it only for explicitly chosen package names and versions, and prefer a project-local output directory over a global provider skills folder. <br>
Risk: Generated SKILL.md content and docstrings are derived from downloaded package source and may contain untrusted text. <br>
Mitigation: Treat generated package mirrors as untrusted evidence, review them before activation, and avoid following instructions embedded in package text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amberlee2427/obscure-package-master) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [generate_mirror.py](artifact/scripts/generate_mirror.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates package-specific SKILL.md files plus copied source references and line-range maps for local agent use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
