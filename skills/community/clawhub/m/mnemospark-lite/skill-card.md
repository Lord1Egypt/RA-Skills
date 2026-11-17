## Description:

Use this skill when OpenClaw needs to store files in mnemospark-lite, pay the x402 upload flow, complete uploads, list wallet-scoped uploads, fetch download details, mint share links, or delete uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pawlsclick](https://clawhub.ai/user/pawlsclick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run mnemospark-lite cloud file storage workflows from OpenClaw, including paid uploads, wallet-scoped listing and download details, share-link creation, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend through a configured wallet during paid upload flows.

Mitigation: Require explicit user confirmation before paid uploads and run with only wallets approved for agent spending.

Risk: Bearer-scoped list tokens can expose wallet-scoped upload access if printed or persisted insecurely.

Mitigation: Keep list_scope_bearer values in secret storage or ephemeral memory and avoid normal chat or log output.

Risk: The skill can create anonymous share links and delete one or more uploads.

Mitigation: Require explicit confirmation before share-link creation and delete requests, especially bulk deletes.

Risk: Unreviewed x402 signer or dependency behavior could affect payment handling.

Mitigation: Prefer pinned, reviewed x402 dependencies or an isolated signer/runtime.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pawlsclick/skills/mnemospark-lite)
- [mnemospark-lite web app](https://app.mnemospark.ai/mnemospark-lite)
- [mnemospark-lite API base](https://api.mnemospark.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce upload IDs, public or site URLs, share URLs, bearer-scoped access guidance, and payment status fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
