## Description: <br>
Skills creator is an AI skill generation framework that scans, registers, retrieves, generates, evaluates, tests, and optimizes agent skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xjxjdnsnak-cell](https://clawhub.ai/user/xjxjdnsnak-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create and maintain skill libraries by finding existing skills, generating new skill files or code, testing candidates, scoring results, and applying optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or newly tested skill code may execute locally with insufficient isolation. <br>
Mitigation: Run testers only inside Docker or a VM with no host mounts and no network, and review generated code before execution. <br>
Risk: Generated skill files may be written outside the intended workspace if paths are not constrained. <br>
Mitigation: Verify path containment before saving generated skills or optimization output. <br>
Risk: Configured DeepSeek or other LLM calls may send proprietary code, secrets, or sensitive task text to an external service. <br>
Mitigation: Redact sensitive content and obtain consent before using external LLM providers. <br>


## Reference(s): <br>
- [API Reference](references/api_reference.md) <br>
- [Meta-Skill Generator Architecture](references/architecture.md) <br>
- [Usage Examples](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xjxjdnsnak-cell/meta-skill-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, YAML, and Python code depending on the requested generation, evaluation, or optimization task] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local skill files, databases, scores, generated skill drafts, tests, and optimization notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
