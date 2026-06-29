## Description: <br>
Reviews Claude and Agent Skill directories for SKILL.md quality, trigger clarity, progressive disclosure, portability, hardcoded secrets, and maintainability, then returns a scorecard with prioritized remediation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huiyonghkw](https://clawhub.ai/user/huiyonghkw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to audit Agent Skill packages before publishing or installing them. It combines a deterministic Python checker with qualitative review guidance to identify trigger, structure, portability, documentation, and security issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has a broad review trigger and may be invoked for general skill-structure requests. <br>
Mitigation: Invoke it intentionally for Agent Skill audits and confirm the target directory before running the checker. <br>
Risk: Running local review scripts against directories containing private material can expose sensitive filenames or findings in reports. <br>
Mitigation: Review check.py before use on private directories and run it only against intended skill packages; the artifact states that secret files such as .env, .key, and .pem should not be read. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huiyonghkw/skills/hekouwang-claude-skill-doctor-skill) <br>
- [Skill writing vocabulary](artifact/references/skill-writing-vocab.md) <br>
- [NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON reports, shell commands, and code-edit recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run the bundled zero-dependency Python checker and produce prioritized remediation steps for the reviewed skill.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
