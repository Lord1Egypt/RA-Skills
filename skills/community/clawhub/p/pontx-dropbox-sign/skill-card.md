## Description:

Integrate Dropbox Sign eSignature workflows through Pontx. Use for signature requests, templates, embedded signing, callbacks, test mode, document downloads, or HelloSign migrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration teams use this skill to plan and implement Dropbox Sign workflows through Pontx, including safe request previews, template usage, embedded signing, callback handling, downloads, and HelloSign migrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials, signing URLs, signer emails, callback bodies, and downloaded documents may expose sensitive signing workflow data.

Mitigation: Store credentials in an environment or credential manager, redact previews and logs, and apply approved access, retention, and deletion policies for documents and signer data.

Risk: A live signature request or production behavior change could be sent without adequate review.

Mitigation: Require a local dry-run preview, redacted review, and explicit approval before confirming an unchanged request; create a new preview token after any document, signer, template, field, or option change.

Risk: Unverified or duplicated callbacks could cause incorrect workflow state or premature document downloads.

Mitigation: Verify callback HMACs before trusting payload fields, process callbacks idempotently, and wait for final-file readiness before fetching completed documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pontjs/skills/pontx-dropbox-sign)
- [Pontx publisher profile](https://clawhub.ai/user/pontjs)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted previews, approval checkpoints, callback handling advice, and document retention guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
