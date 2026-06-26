## Description: <br>
CallerAPI (callerapi.com) enables agents to search and read CallerAPI data through an OOMOL-connected account instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up phone-number intelligence, spam reputation, business details, complaints, optional HLR carrier data, and CallerAPI account information through the OOMOL CallerAPI connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The OOMOL CLI installer is a shell or PowerShell command that can execute with the user's account permissions. <br>
Mitigation: Confirm cli.oomol.com is the official OOMOL distribution source and prefer a package-manager or signed release path if available. <br>
Risk: The skill requires a CallerAPI connection and sensitive credentials. <br>
Mitigation: Use the OOMOL connection flow so credentials are injected server-side, and avoid exposing raw API tokens in prompts, files, or shell history. <br>
Risk: Phone-number intelligence queries may involve sensitive personal or business contact data. <br>
Mitigation: Run lookups only for user-authorized purposes and review returned CallerAPI data before using it in downstream decisions. <br>


## Reference(s): <br>
- [CallerAPI homepage](https://callerapi.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-callerapi) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, json] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before sending JSON payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
