## Description:

Create and monitor NotebookLM Studio content - Audio Overview, Video Overview, Infographics, and Slides - via the notebooklm-mcp-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skywalker-lili](https://clawhub.ai/user/skywalker-lili)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create, monitor, and download NotebookLM Studio outputs such as podcasts, videos, infographics, and slide decks from selected NotebookLM notebooks. It can also be triggered by upstream skills with pre-filled notebook, source file, output type, format, length, and language parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local files to NotebookLM, which may expose content that is not approved for upload.

Mitigation: Use only approved source directories and require confirmation before uploading files.

Risk: The skill launches a detached background poller, which can be hard to track or cancel if ownership is unclear.

Mitigation: Run it in an environment with clear task ownership, logs, and cancellation procedures.

Risk: Shared temporary-directory execution can expose task metadata or downloaded artifacts to unintended local users.

Mitigation: Avoid shared /tmp execution or restrict task directories to an approved, access-controlled location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skywalker-lili/skills/jclaw-notebooklm-content-creation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for creating NotebookLM Studio content and setting up background polling.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
