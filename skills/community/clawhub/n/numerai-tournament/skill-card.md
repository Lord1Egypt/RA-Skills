## Description: <br>
Autonomous Numerai tournament participation - train models, submit predictions, and earn NMR cryptocurrency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[obekt](https://clawhub.ai/user/obekt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and data scientists use this skill to set up Numerai credentials, download tournament data, train LightGBM models, validate predictions, and submit predictions or uploaded models to Numerai. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority to use Numerai API credentials for prediction or model uploads that may affect staked cryptocurrency outcomes. <br>
Mitigation: Use a dedicated or restricted API key when available, start with zero or minimal stake, and require manual approval before uploads or submissions. <br>
Risk: Numerai credentials may be stored locally or exposed through environment variables. <br>
Mitigation: Protect credential files with restrictive permissions and avoid sharing logs, files, or sessions that contain NUMERAI_PUBLIC_ID or NUMERAI_SECRET_KEY. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/obekt/numerai-tournament) <br>
- [Numerai](https://numer.ai) <br>
- [Numerai account settings](https://numer.ai/account) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses NUMERAI_PUBLIC_ID and NUMERAI_SECRET_KEY, requires python3 and pip, and may create local credential, data, model, and prediction files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
