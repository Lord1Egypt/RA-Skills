## Description:

Extracts title, keywords, and abstract metadata from academic PDFs and returns structured JSON for literature organization, citation preparation, and quick paper review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y-egg](https://clawhub.ai/user/y-egg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and literature-management users can use this skill to extract a paper title, keywords, and abstract from a supplied PDF into JSON for downstream citation and data-management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send extracted PDF text to Moonshot's external AI API when an API key is present.

Mitigation: Review before installation or use, and avoid confidential, unpublished, regulated, or license-restricted PDFs unless this external data flow is approved.

Risk: The artifact does not document the remote data flow, dependency pinning, consent handling, or a local-only mode.

Mitigation: Prefer a reviewed version that documents the remote service, asks for consent, pins dependencies, and offers a local-only option.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/y-egg/skills/pdf-literature-parser)
- [Moonshot API endpoint](https://api.moonshot.cn/v1)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON object with title_apa, keywords, and abstract fields, plus concise setup and command-line guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a PDF path input; when MOONSHOT_API_KEY is configured, up to the first 5,000 characters of extracted PDF text may be sent to Moonshot's external API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
