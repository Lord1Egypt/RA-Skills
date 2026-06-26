## Description: <br>
Track baby sleep, feeding, diapers, and growth via Huckleberry app API. Use for logging baby activities through natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronn](https://clawhub.ai/user/aaronn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External caregivers and parents use this skill to log and review baby sleep, feeding, diaper, and growth activity in Huckleberry through natural-language requests and CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs Huckleberry login credentials and can read or update sensitive baby-tracking records. <br>
Mitigation: Use protected environment variables or a tightly permissioned credentials file, do not commit credentials, and install only when this access is acceptable. <br>
Risk: The skill can create or change baby activity, growth, and history records. <br>
Mitigation: Verify important entries in the Huckleberry app and keep AI attribution notes on logged or updated entries. <br>
Risk: The skill depends on a third-party Python package and may use a GitHub dependency for feature coverage. <br>
Mitigation: Review or pin the dependency before deployment, especially in managed or shared environments. <br>


## Reference(s): <br>
- [Huckleberry on ClawHub](https://clawhub.ai/aaronn/openclaw-huckleberry-skill) <br>
- [py-huckleberry-api](https://github.com/Woyken/py-huckleberry-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and CLI output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, huckleberry-api, and Huckleberry account credentials to execute live logging or history commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
