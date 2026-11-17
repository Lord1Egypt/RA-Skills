## Description:

nudocs helps agents upload documents to Nudocs.ai for hosted editing, retrieve private edit links, list or export documents, and delete exact remote documents through the authenticated Nudocs CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdrhyne](https://clawhub.ai/user/jdrhyne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use nudocs to move Markdown, document, and other supported files into Nudocs.ai for hosted collaborative editing and to export edited content back to local files. It also guides exact-ID link retrieval, listing, and deletion workflows with confirmation around sensitive uploads, sharing, overwrites, and destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploads send selected documents to Nudocs for processing and may expose sensitive content outside the local environment.

Mitigation: Disclose the data boundary before upload and require explicit action-time confirmation for files containing credentials, health, financial, legal, customer, employee, or other sensitive data.

Risk: API keys or authentication details could be exposed during setup or troubleshooting.

Mitigation: Use protected local or CI secret storage, never ask users to paste keys into chat, and verify authentication through bounded CLI behavior instead of printing configuration or environment contents.

Risk: Returned edit links may grant access to hosted content if forwarded or posted.

Mitigation: Treat edit links as private by default and require separate action-time approval before sharing them with a stated audience or destination.

Risk: Pull operations can overwrite local files, and delete operations can irreversibly change remote state.

Mitigation: Resolve exact document IDs and output paths, confirm before overwrites, and obtain immediate approval before deleting the resolved document ID.

## Reference(s):

- [Nudocs CLI formats](references/formats.md)
- [Nudocs CLI source](https://github.com/PSPDFKit-labs/nudocs-cli)
- [Nudocs](https://nudocs.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include private edit links, document IDs, local file paths, and action-time confirmation prompts.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
