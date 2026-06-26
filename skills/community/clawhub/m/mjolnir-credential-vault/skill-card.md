## Description: <br>
GPG AES-256 encrypted credential management for storing, retrieving, and managing passwords, API tokens, and secrets through init/add/get/list/remove operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[king6381](https://clawhub.ai/user/king6381) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to initialize and operate a local encrypted credential vault for passwords, API tokens, and service secrets, then retrieve values through Python, shell, or CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plaintext secret material is briefly written to local disk during encryption or saving. <br>
Mitigation: Use a RAM-backed temporary directory, a dedicated secrets manager, or another workflow that avoids plaintext-on-disk exposure for highly sensitive secrets. <br>
Risk: The CRED_MASTER_PASS environment variable can be exposed to same-user processes on some Linux systems. <br>
Mitigation: Prefer interactive entry, gpg-agent or pinentry, or session-scoped runtime injection, and avoid persisting the master password in shell startup files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/king6381/mjolnir-credential-vault) <br>
- [Gpg4win](https://gpg4win.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python snippets, plus command-line text or JSON from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local GPG, Python 3, and CRED_MASTER_PASS for non-interactive retrieval.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
