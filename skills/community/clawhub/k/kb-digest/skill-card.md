## Description:

kb-digest turns URLs, PDFs, pasted text, or URL batches into structured knowledge cards, summaries, Q&A sets, mind maps, or podcast-style scripts using a configured LLM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vineindalvik](https://clawhub.ai/user/vineindalvik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to digest web pages, PDFs, pasted text, or URL batches into reusable knowledge-management artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrary URL fetching can expose internal or confidential network resources if the runtime has broad egress.

Mitigation: Use only approved public URLs or run with network egress controls; avoid localhost, private services, and cloud metadata addresses.

Risk: Processed source content is sent to the configured LLM endpoint.

Mitigation: Avoid confidential PDFs, private notes, and internal URLs unless the LLM endpoint is trusted and approved for that data.

Risk: Feishu push shares generated content with the configured webhook destination.

Mitigation: Treat webhook pushes as external sharing and verify the destination before enabling FEISHU_WEBHOOK_URL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vineindalvik/skills/kb-digest)

## Skill Output:

**Output Type(s):** [text, markdown, json, files]

**Output Format:** [Console text, Markdown knowledge cards, Markdown mind maps, JSON Q&A, or saved Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated in Chinese by default; URL and PDF inputs are truncated before LLM processing.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
