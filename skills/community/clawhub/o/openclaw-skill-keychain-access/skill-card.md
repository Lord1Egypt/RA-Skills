## Description: <br>
macOS Keychain helpers (list/get/set/delete) via the security CLI. Trigger this skill when the user needs to inspect, store, update, or remove generic passwords from the Keychain with explicit confirmation on destructive ops and guarded secret disclosure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to list, retrieve, create, update, or delete macOS Keychain generic passwords with explicit service/account filters, dry-run previews, and confirmation controls for credential changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive macOS Keychain credentials, and raw password output can place secrets in the conversation or logs. <br>
Mitigation: Use raw output only after explicit user authorization, prefer masked reads, and avoid copying secrets into persistent logs or chat history. <br>
Risk: Credential updates and deletions can alter or remove local secrets. <br>
Mitigation: Use dry-run previews, explicit service/account filters, a specific keychain path when practical, and confirmation prompts; use --yes only after the user has authorized the change. <br>
Risk: Server security evidence says the helper overstates how safely password-stdin and password-env keep stored passwords out of process arguments. <br>
Mitigation: Do not rely on stdin or environment input to fully prevent process-argument exposure until the helper is fixed or accurately documented; avoid exposing command lines and run only in trusted local contexts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppopen/openclaw-skill-keychain-access) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include masked credential metadata by default; plaintext secrets are only produced when the user explicitly requests raw output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
