## Description: <br>
MetaBot is a MetaID-based AI agent skill for creating MetaBots, setting MetaBot avatars, and sending Buzz messages to the MVC network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newfish](https://clawhub.ai/user/newfish) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to create MetaID MetaBot accounts, attach avatars, and publish simple Buzz protocol messages through command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet seed phrases and possible LLM API keys may be stored in plaintext account.json. <br>
Mitigation: Use a dedicated low-value wallet, keep account.json out of source control and shared folders, and restrict local file access to trusted users. <br>
Risk: Buzz and avatar operations can publish irreversible blockchain or network actions. <br>
Mitigation: Review the selected account, message text, avatar file, and intended network action before running commands. <br>
Risk: File-based Buzz content and avatar paths can read and publish local file data. <br>
Mitigation: Avoid using @file inputs or avatar paths that contain sensitive local files. <br>


## Reference(s): <br>
- [Account Management](references/account-management.md) <br>
- [Buzz Protocol](references/buzz-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON account updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update account.json and publish irreversible network transactions when commands are executed] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
