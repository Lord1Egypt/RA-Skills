## Description: <br>
Manage passwords with generation, strength checks, and storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and security-minded users use this skill to generate passwords and PINs, estimate password strength and entropy, create diceware-style passphrases, and optionally check whether a password appears in known breach data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live passwords may be exposed when entered as command-line arguments. <br>
Mitigation: Prefer generated or test passwords, and avoid passing production or reusable secrets through command-line arguments. <br>
Risk: The optional breach-check feature contacts Have I Been Pwned with a password-derived SHA-1 prefix. <br>
Mitigation: Use breach checking only when the user accepts sending that SHA-1 prefix to the external service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain3/password) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated passwords, passphrases, PINs, strength ratings, entropy estimates, breach-check status, and usage guidance may be emitted depending on the selected command.] <br>

## Skill Version(s): <br>
3.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
