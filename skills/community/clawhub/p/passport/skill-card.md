## Description: <br>
Validate and format passport or identity document data. Use when checking fields, validating numbers, generating fixtures, linting records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Passport to run local CLI actions for passport or identity-document record checking, formatting, linting, and fixture generation. The reviewed artifacts primarily log, search, and export entered values locally rather than independently validating passport data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed script can store passport numbers, names, dates of birth, or other identity-document details in plaintext local logs and exported files. <br>
Mitigation: Do not enter real sensitive identity data unless local plaintext storage and export are intended; review and delete logs or exports after use. <br>
Risk: The security review says the advertised validation capability is unsupported by the reviewed script. <br>
Mitigation: Treat the skill as local logging and formatting assistance, not authoritative passport or identity-document validation; verify results with a trusted validation source. <br>


## Reference(s): <br>
- [Passport on ClawHub](https://clawhub.ai/bytesagain-lab/passport) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell command examples; CLI output is plain text and exports JSON, CSV, or TXT files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact script stores local command history and exports under ~/.local/share/passport/.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
