## Description: <br>
Generates secure random passwords locally and checks password strength with entropy and crack-time estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alone86136](https://clawhub.ai/user/alone86136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users use this skill to generate local passwords with configurable length and character sets, or to estimate the strength of a password before relying on it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Passwords checked through the documented command-line argument form may be visible in local shell history or process listings. <br>
Mitigation: Avoid checking valuable existing passwords with the command-line argument form; use it for test passwords or adapt the checker to read from a hidden prompt or stdin. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alone86136/local-password) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated passwords and strength checks run locally using Python standard library scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
