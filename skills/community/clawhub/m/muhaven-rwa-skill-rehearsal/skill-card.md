## Description: <br>
Confidential real-world-asset (RWA) portfolio agent built on MuHaven's Fhenix-CoFHE-encrypted token primitives for reading encrypted balances, staging yield claims, and drafting buy or claim intents for human confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hastodev](https://clawhub.ai/user/hastodev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External MuHaven users use this skill to inspect encrypted RWA portfolio information, review yield and audit context, and stage buy, claim, or pause actions that require user confirmation before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can stage buy, claim, and pause actions that affect wallet or account policy. <br>
Mitigation: Start in read-only mode where possible and approve buy, claim, or pause confirmations only when you initiated the action. <br>
Risk: The skill requires a MuHaven account connection and broker, so users may be exposed to sensitive credential or endpoint mistakes. <br>
Mitigation: Use the legitimate @muhaven/mcp broker and endpoint, and keep authentication in the broker-managed OS keychain rather than pasting tokens into prompts. <br>
Risk: Sandbox protections may be advisory depending on the current OpenClaw runtime. <br>
Mitigation: Confirm that the runtime enforces the declared sandbox and network restrictions before enabling non-read actions. <br>


## Reference(s): <br>
- [MuHaven homepage](https://muhaven.app) <br>
- [ClawHub skill listing](https://clawhub.ai/hastodev/muhaven-rwa-skill-rehearsal) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact manifest](artifact/manifest.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured tool responses with confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include portfolio summaries, audit status, unsigned intent proposals, and confirmation guidance.] <br>

## Skill Version(s): <br>
0.1.0-rc.1 (source: server release metadata; artifact frontmatter and package metadata report 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
