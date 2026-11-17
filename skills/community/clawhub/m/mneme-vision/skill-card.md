## Description:

Use local visual memory tools to index and search photos and videos from creator media libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bkennedyshit](https://clawhub.ai/user/bkennedyshit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and OpenClaw users use this skill to index local photo and video folders, run natural-language or visual-similarity search, inspect media, and manage local GPU memory around media workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses an unpinned local MCP server package for media indexing and search.

Mitigation: Install only from a trusted source, pin the MCP package to a reviewed version when possible, and run it with access limited to intended media directories.

Risk: The skill can index selected local photo and video folders, which may include private or sensitive media.

Mitigation: Index only folders the user explicitly selects and avoid uploading local media to cloud services unless the user separately requests that action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bkennedyshit/skills/mneme-vision)
- [Mneme Homepage](https://mneme.nepa-ai.com)
- [Mneme MCP Server](https://github.com/bkennedyshit/polymathes/tree/main/mneme)
- [OpenClaw Polymath](https://github.com/bkennedyshit/openclaw-polymath)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise text, shell commands, configuration snippets, and previewable media result metadata when supported]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return media_artifacts.v1 JSON for host-rendered media previews; local paths should be exposed through compact links or copy actions when supported.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
