## Description: <br>
Bakes, inspects, and manages scoped lnd macaroons for least-privilege agent access, including preset roles, custom permissions, signer scoping, and rotation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Roasbeef](https://clawhub.ai/user/Roasbeef) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators managing lnd nodes use this skill to create, inspect, rotate, and configure least-privilege macaroons for agents instead of sharing broad admin credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Macaroon and TLS certificate paths expose bearer credentials if copied, stored, or logged insecurely. <br>
Mitigation: Protect macaroons and TLS certificates like passwords, store generated macaroons with 0600 permissions, and avoid sharing them between agent roles. <br>
Risk: Using admin.macaroon or broad custom permissions can grant excessive lnd control. <br>
Mitigation: Use the narrowest preset or custom permission set, avoid admin.macaroon except during tightly controlled setup, and inspect generated macaroons before deployment. <br>
Risk: Running lncli, jq, or Docker from an untrusted environment can affect credential generation or inspection. <br>
Mitigation: Run the script only with trusted local tooling and trusted container contexts, then verify the target node and resulting permissions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Roasbeef/lnd-macaroon-bakery) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with bash commands and configuration snippets; script execution can produce macaroon files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated macaroons are credential files and should be protected with restrictive file permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
