## Description:

Handles large user-uploaded files by saving them to local workspace storage and routing larger files to background processors so the agent can acknowledge receipt without blocking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunkaikai123](https://clawhub.ai/user/sunkaikai123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to integrate asynchronous handling for PDFs, media, images, logs, Office documents, and archives that may otherwise block a Gateway or agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files can be written to local workspace storage and processed by background Python processes.

Mitigation: Add request-size limits before writing files, isolate storage by user or job, and use unpredictable per-job paths.

Risk: Temporary, processing, and completed files may be retained longer or handled less safely than users expect.

Mitigation: Apply scheduled cleanup across all temporary states and disclose retention behavior before automatic processing is enabled.

Risk: The release evidence says the skill may overstate completed functionality, including notification and processor behavior.

Mitigation: Review implementation status before deployment and replace placeholder notification or processor logic with production handlers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sunkaikai123/skills/large-file-handler)
- [README.md](artifact/README.md)
- [INTEGRATION.md](artifact/INTEGRATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processing results may be placeholder summaries until file-type processors and real notification delivery are implemented.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
