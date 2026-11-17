## Description:

Pro Zh Summary summarizes long Chinese text by segmenting input and generating concise Chinese summaries with a local MT5-based model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erickong](https://clawhub.ai/user/erickong)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to summarize long Chinese articles, reports, meeting notes, and conversations into shorter Chinese summaries for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads full text or local files provided for summarization, which may include sensitive documents.

Mitigation: Avoid processing sensitive files or confidential text unless the local server behavior and data handling are acceptable for the deployment environment.

Risk: The skill auto-starts a background localhost ML server.

Mitigation: Review the server startup behavior, expose clear start and stop controls, and deploy only in environments where a local background service is acceptable.

Risk: The localhost API and server launch path need review before handling sensitive material.

Mitigation: Authenticate the local API, launch server.py by an absolute trusted path, and pin dependencies and model revisions before wider use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erickong/skills/pro-zh-summary)
- [ClawHub publisher profile](https://clawhub.ai/user/erickong)
- [HeackMT5-ZhSum100k model](https://huggingface.co/heack/HeackMT5-ZhSum100k)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text Chinese bullet summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts text, file, or standard input; summary length is configurable.]

## Skill Version(s):

1.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
