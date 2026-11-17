## Description:

Owner-only private workflow for a Halala sales process that refreshes access, collects small sample lists, and optionally prepares detail notes.

This skill is for research and development only.

## Publisher:

[rony99](https://clawhub.ai/user/rony99)

### License/Terms of Use:

MIT-0

## Use Case:

The publisher uses this private skill on a controlled host to refresh login, collect limited sales or procurement list and detail artifacts, and summarize them for the owner. It is not a general public workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles login tokens and related session data.

Mitigation: Install only on the owner's controlled machine, keep the workdir private, and protect or rotate QIANLIMA_TOKEN and related credentials.

Risk: Optional detail analysis can send tender details, contacts, and extracted attachment text to a configurable external AI endpoint.

Mitigation: Avoid detail analysis unless this data sharing is approved; when used, configure a trusted HTTPS endpoint and token.

Risk: The security verdict requires review before broader use.

Mitigation: Review dependency locking and the configured data flow before any deployment outside the owner's private workflow.

## Reference(s):

- [Private workflow contract](references/contract.md)
- [ClawHub skill page](https://clawhub.ai/rony99/skills/my-halala-sales-vp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with shell command snippets and local JSON or Markdown artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a private workdir for runtime, data, and output files; optional detail analysis can send collected data to the configured model endpoint.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
