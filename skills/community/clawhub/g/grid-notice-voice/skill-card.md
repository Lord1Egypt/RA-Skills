## Description:

Turn a written grid-matter list into one grid notice voice clip per labeled cue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External office teams use this skill to turn an existing grid-matter notice list into 8 to 20 labeled voice clips while preserving supplied facts, pronunciation guidance, voice rights, and billing confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Beatra device token grants broad access including billable generation, voice cloning, task and artifact access, and wallet spend.

Mitigation: Review the requested access before installing, keep the token local, and revoke the device in Beatra Console when the installation is no longer trusted or needed.

Risk: Clone and speech operations can spend account credits, and unsafe retries can duplicate paid work.

Mitigation: Read live pricing, require explicit confirmation before paid stages, use one opaque client_request_id per logical request, and retry only byte-identical uncertain submissions.

Risk: Silent automatic updates can replace package code and instructions before normal commands run.

Mitigation: Disable automatic updates with the provided update command when review stability is required, and rely only on verified package update paths.

Risk: Voice cloning can misuse a person's likeness if file access is mistaken for consent.

Mitigation: Require explicit likeness and voice rights, inspect the authorized sample, and never treat local file access as cloning consent.

Risk: Generated notices can incorrectly imply approvals, enforcement results, or facts absent from the source list.

Mitigation: Use only the supplied grid-matter list and review every clip against the source text and pronunciation table.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beatra-ai/skills/grid-notice-voice)
- [Grid notice voice workflow](artifact/references/workflow.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Installation registration](artifact/references/installation-registration.md)
- [Tasks and results](artifact/references/tasks-and-results.md)
- [Billing, errors, and recovery](artifact/references/billing-errors-and-recovery.md)
- [Bundled MCP Client diagnostics](artifact/references/mcp-connection.md)
- [Automatic updates and safety](artifact/references/automatic-updates-and-safety.md)
- [Uninstall and disconnect](artifact/references/uninstall-and-disconnect.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with JSON payload examples and shell commands; generated voice artifacts are delivered as audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a supplied grid-matter list, pronunciation details for names, explicit rights for cloned voices, and Beatra task polling for final billing and artifact details.]

## Skill Version(s):

0.1.2 (source: server release metadata and package manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
