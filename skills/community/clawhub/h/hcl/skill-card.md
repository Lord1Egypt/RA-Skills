## Description: <br>
HumanCanHelp starts a local human-in-the-loop help session so a trusted helper can view and interact with a shared browser tab or desktop when an AI workflow is blocked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metalony](https://clawhub.ai/user/metalony) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use HumanCanHelp to hand off short blocked visual or interactive browser or desktop steps to a trusted person, then resume the automated workflow based on the helper's outcome. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A live browser tab or desktop can be exposed over a LAN or public URL, and authentication is optional. <br>
Mitigation: Use the skill only for intentional trusted handoffs, set a strong unique password for LAN or public sharing, share access through a trusted channel, and stop the server immediately after the handoff. <br>
Risk: Full-desktop VNC mode can expose more local context than a single browser tab. <br>
Mitigation: Prefer CDP browser-tab sharing when it is sufficient, and use an isolated browser profile, VM, or clean desktop session for sensitive workflows. <br>
Risk: Helpers may see or control sensitive flows such as secrets, MFA, payments, account changes, or owner-bound identity steps. <br>
Mitigation: Avoid those steps unless the real account owner is present; use the owner-action-required outcome when only the account owner can continue. <br>
Risk: Helper-side masking can hide regions and block pointer input in the helper UI, but it does not sanitize the underlying CDP or VNC transport stream. <br>
Mitigation: Do not rely on masking as a complete privacy boundary; remove or isolate sensitive content before starting the session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metalony/hcl) <br>
- [ClawHub publisher profile: metalony](https://clawhub.ai/user/metalony) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI outcome semantics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [At runtime, the CLI prints local or public helper URLs and exits with success, failure, timeout, or owner-action-required outcomes.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
