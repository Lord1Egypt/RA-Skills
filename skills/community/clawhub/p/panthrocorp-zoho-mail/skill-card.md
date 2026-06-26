## Description: <br>
Full read/write Zoho Mail access for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panthrocorp](https://clawhub.ai/user/panthrocorp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let OpenClaw agents manage a Zoho Mail mailbox, including reading, sending, replying, deleting, and marking messages after OAuth setup. <br>

### Deployment Geography for Use: <br>
Global; the artifact documents Zoho EU data-centre endpoints. <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad Zoho Mail access, including reading, sending, marking, and deleting messages. <br>
Mitigation: Install only for a mailbox approved for agent use, prefer a dedicated or constrained mailbox, and require human approval for send and delete workflows. <br>
Risk: OAuth client secrets and token encryption keys are sensitive operational credentials. <br>
Mitigation: Protect the OAuth client secret and ZOHO_MAIL_TOKEN_KEY, and keep them in an approved secret-management path. <br>
Risk: Manual binary installation can introduce supply-chain risk if artifacts are not verified. <br>
Mitigation: Verify release checksums before manual binary installs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/panthrocorp/panthrocorp-zoho-mail) <br>
- [Project Homepage](https://github.com/PanthroCorp-Limited/openclaw-skills) <br>
- [Zoho API Console](https://api-console.zoho.eu/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Text] <br>
**Output Format:** [JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Zoho OAuth credentials and can read, send, reply, delete, and mark mailbox messages.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release metadata, dist/metadata.json, and changelog; released 2026-04-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
