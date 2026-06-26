## Description: <br>
Manage and audit OpenClaw secrets by coordinating gateway restarts, converting plaintext credentials to SecretRef format, and validating configuration accuracy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlab1201](https://clawhub.ai/user/jlab1201) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to audit OpenClaw deployments for plaintext credentials, migrate secrets to SecretRef-backed configuration, and coordinate validation without disrupting gateway operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential or repository operations may expose or change sensitive OpenClaw configuration if run against the wrong files. <br>
Mitigation: Review target paths, commands, and credential scope before applying migrations; use only credentials and repositories you intend the skill to operate on. <br>
Risk: Gateway restart or reload steps can disrupt active OpenClaw sessions. <br>
Mitigation: Run gateway operations sequentially with a single authorized operator and validate gateway health before continuing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jlab1201/openclaw-secrets-hygiene) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell, JSON, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces audit reports, migration plans, configuration templates, validation checklists, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
