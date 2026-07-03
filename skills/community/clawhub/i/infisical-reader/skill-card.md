## Description: <br>
Direct REST API reader for Infisical secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[achikochikorogaru](https://clawhub.ai/user/achikochikorogaru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to authenticate with Infisical through Universal Auth, list accessible projects, and retrieve secret values for a selected workspace and environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve and print Infisical secret values, including raw values when requested. <br>
Mitigation: Use a least-privilege Machine Identity scoped only to needed projects and environments, avoid bulk or raw secret output, and request raw values only when necessary. <br>
Risk: Compromised or over-broad Infisical credentials could expose many downstream API keys or credentials to an agent session. <br>
Mitigation: Store credentials securely, rotate them if exposed, and review agent prompts and outputs before allowing secret retrieval. <br>


## Reference(s): <br>
- [Infisical Reader on ClawHub](https://clawhub.ai/achikochikorogaru/infisical-reader) <br>
- [Infisical](https://infisical.com) <br>
- [API reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON from shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Secret values are masked by default unless raw output is explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
