## Description: <br>
Store, retrieve, list, and manage secrets using gopass, including CRUD operations, secret generation, TOTP, recipients, mounted stores, and clipboard operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erdGeclaw](https://clawhub.ai/user/erdGeclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and operators use this skill to have an agent provide gopass command guidance for storing, retrieving, generating, searching, syncing, and removing password-store entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose secrets through show or clipboard operations. <br>
Mitigation: Require explicit confirmation before showing or copying secrets, and avoid clipboard use on untrusted machines. <br>
Risk: The skill can delete secrets or folders from a gopass store. <br>
Mitigation: Confirm the target path before delete or recursive delete actions, and list or back up affected paths first. <br>
Risk: The skill can sync a password store through Git. <br>
Mitigation: Verify configured Git remotes before syncing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erdGeclaw/gopass) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command guidance assumes gopass, GPG, and an initialized password store are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
