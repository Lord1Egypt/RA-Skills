## Description: <br>
Use Typefully through OOMOL's oo connector to read, create, update, and delete account-authenticated Typefully drafts and social sets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a user's Typefully account through OOMOL, including reading account data and managing drafts or social sets with schema-first payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Account-authenticated actions can create, update, or delete Typefully drafts. <br>
Mitigation: Confirm the exact payload, target draft or social set, and expected effect with the user before write or destructive actions. <br>
Risk: The skill requires OOMOL-backed tooling to access the user's Typefully account. <br>
Mitigation: Install only when the user intends to grant that access, and use the server-provided connection flow for account authorization. <br>
Risk: First-time setup may require running a remote oo CLI installer. <br>
Mitigation: Verify the installer source before running setup commands, and run setup only after an auth, connection, or missing-command failure requires it. <br>


## Reference(s): <br>
- [ClawHub Typefully Skill](https://clawhub.ai/oomol/oo-typefully) <br>
- [Typefully Homepage](https://typefully.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OOMOL-managed Typefully credentials; write and destructive actions require user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
