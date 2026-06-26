## Description: <br>
CallPage (callpage.io) helps agents read, create, and update CallPage data through an OOMOL-connected account instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate CallPage through OOMOL-connected credentials, including listing and retrieving calls, users, and widgets, and creating callback requests after confirming the payload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional oo CLI installer uses shell-eval commands. <br>
Mitigation: Review the installer source or use official verified installation guidance before running the installer. <br>
Risk: The create_widget_call action can create a CallPage callback request. <br>
Mitigation: Confirm the exact callback payload and intended effect with the user before execution. <br>
Risk: The skill requires connecting CallPage through OOMOL-managed credentials. <br>
Mitigation: Install only when the user is comfortable connecting CallPage through OOMOL and using OOMOL-injected credentials. <br>


## Reference(s): <br>
- [CallPage skill page](https://clawhub.ai/oomol/oo-callpage) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [CallPage homepage](https://www.callpage.io) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live connector schema before execution and returns connector responses as JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
