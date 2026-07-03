## Description: <br>
Securely broker user-authorized Keeper vault credentials into agent-to-agent conversations using scoped access and zero-knowledge encryption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmtucker](https://clawhub.ai/user/zmtucker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when a user-facing agent needs to retrieve only user-authorized Keeper vault records and prepare a credential for another agent. It supports one-time share links, Keeper Notation references, and inline delivery when explicitly approved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists reusable Keeper authentication material that grants scoped access to shared Keeper folders. <br>
Mitigation: Protect KEEPER_SKILL_HOME as secret storage, keep it isolated per agent environment, avoid shared tenant mounts, and revoke or delete the Keeper device config when the environment is retired or suspected compromised. <br>
Risk: Inline delivery can place raw credentials into agent conversations, transcripts, or logs. <br>
Mitigation: Prefer one-time share or Keeper Notation reference delivery, and use inline delivery only after the user explicitly approves the exact recipient and record. <br>
Risk: Passing the one-time access token as a command argument can expose it through shell history or process inspection. <br>
Mitigation: Prefer KEEPER_KSM_TOKEN for bootstrap, treat the token as single-use sensitive material, and clear it after init completes. <br>
Risk: One-Time Share mode can depend on a Keeper Commander persistent-login profile with broader access than KSM. <br>
Mitigation: Use Commander only for creating one-time share links, protect KEEPER_COMMANDER_CONFIG separately, and fall back to reference delivery when the recipient has its own scoped KSM access. <br>


## Reference(s): <br>
- [Keeper Secrets Manager developer SDK documentation](https://docs.keeper.io/keeperpam/secrets-manager/developer-sdk-library) <br>
- [KSM authentication and cross-session persistence](references/ksm_auth_and_storage.md) <br>
- [Delivery modes and agent-to-agent orchestration](references/delivery_modes.md) <br>
- [ClawHub skill page](https://clawhub.ai/zmtucker/keeper-credentials) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output with suggested message text and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive credential payloads or one-time share URLs; outputs can include _sensitive markers for handling guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
