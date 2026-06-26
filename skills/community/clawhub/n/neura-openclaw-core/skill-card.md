## Description: <br>
Use when an OpenClaw-style or local autonomous computer-use agent needs a single Neura Relay preflight workflow for messages, file changes, browser submits, shell commands, package or publisher changes, workflow state, memory writes, or data exports before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neurarelay](https://clawhub.ai/user/neurarelay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare refs-only preflight Action Cards and interpret Relay Decision Receipts before an OpenClaw-style or local autonomous agent performs consequential actions. It is intended for workflows involving messages, file changes, browser submits, shell commands, package or publisher changes, memory writes, and data exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for consequential local-agent actions, so using it without review or a trusted receipt path could lead to unauthorized execution. <br>
Mitigation: Require an accepted Relay Decision Receipt or explicit local policy acceptance before the developer-owned runtime executes the proposed action. <br>
Risk: Action Cards could expose sensitive material if raw payloads, secrets, credentials, customer data, or private workspace contents are included. <br>
Mitigation: Use refs-only Action Cards and reject raw message bodies, file contents, form values, command strings, package credentials, tokens, passwords, and private payloads. <br>
Risk: The security evidence reports no harmful behavior in supplied scan data, but notes that artifact files were unavailable during that adjudication. <br>
Mitigation: Review the bundled skill contents and confirm file hashes before granting sensitive access or relying on the skill in a privileged workflow. <br>


## Reference(s): <br>
- [Neura Relay OpenClaw Scenario Corpus](references/scenario-corpus.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/neurarelay/neura-openclaw-core) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or structured text containing a refs-only Action Card draft, missing-reference checklist, receipt interpretation, and runtime next step.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should avoid raw payloads, secrets, credentials, private data, and executable local actions until the receipt path is accepted.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
