## Description: <br>
Scans a project or skill directory before publication for possible sensitive information such as webhooks, tokens, user paths, private IPs, JWTs, SSH private keys, database connections, and third-party API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m17y](https://clawhub.ai/user/m17y) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and skill publishers use this skill before publishing to ClawHub or a public repository to check selected project files for possible secrets and privacy-sensitive identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw scan output can contain real secrets or personal data if findings are copied into public channels. <br>
Mitigation: Run the scanner only on the intended project directory and redact findings before sharing output publicly. <br>
Risk: Broad scans can inspect unrelated personal files. <br>
Mitigation: Pass the specific skill or project directory rather than a home directory or broad workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/m17y/privacy-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text report with pass, warning, and fail findings; Markdown usage guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns exit code 0 when scans pass and exit code 1 when severe findings are found; strict mode returns a nonzero exit code for warnings.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
