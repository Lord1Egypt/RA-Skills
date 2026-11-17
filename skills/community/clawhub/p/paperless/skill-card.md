## Description:

Interact with Paperless-NGX document management system via ppls CLI. Search, retrieve, upload, and organize documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickchristensen](https://clawhub.ai/user/nickchristensen)

### License/Terms of Use:


## Use Case:

People using Paperless-NGX use this skill to have an agent search, retrieve, upload, download, and organize documents through the ppls CLI. It is suited for document library workflows that depend on Paperless-NGX metadata such as tags, correspondents, document types, and dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using plaintext HTTP for a non-local Paperless server can expose API tokens or document traffic.

Mitigation: Use HTTPS for non-local Paperless servers and create a least-privilege, revocable API token.

Risk: A global, unpinned ppls CLI install can change behavior across releases or affect other projects on the same machine.

Mitigation: Install a pinned ppls version in an isolated project or container when reliability matters.

Risk: API tokens can be exposed through shell history or shared configuration.

Mitigation: Avoid placing tokens directly in shared commands, shell history, logs, or checked-in configuration.

## Reference(s):

- [Paperless skill on ClawHub](https://clawhub.ai/nickchristensen/skills/paperless)
- [ppls on GitHub](https://github.com/NickChristensen/ppls)
- [Paperless-NGX Docs](https://docs.paperless-ngx.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with ppls CLI commands and JSON-oriented command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ppls CLI plus PPLS_HOSTNAME and PPLS_TOKEN environment configuration.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
