## Description: <br>
Generate secure random passwords using Python's secrets module with customizable length and character set options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users can use this skill to generate one or more local random passwords with configurable length, symbols, and numbers for account setup or service-account workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated passwords are printed to the terminal and could be exposed through logs, screen sharing, terminal capture, or nearby observers. <br>
Mitigation: Run the skill in a private terminal, avoid persistent logging, and clear visible output after transferring the password to an appropriate secret store. <br>
Risk: Documentation examples may include sample passwords or password patterns that should not be reused for real accounts. <br>
Mitigation: Generate fresh passwords for each account and do not reuse sample strings from documentation or prior terminal output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/password-generator-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text passwords and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated passwords are printed to stdout; length, count, symbols, and numbers are user-configurable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
