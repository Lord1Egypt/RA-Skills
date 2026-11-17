## Description:

Provides agent guidance for using the mma-bridge command-line tool to interact with Meteor Master AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mordom0404](https://clawhub.ai/user/mordom0404)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to control Meteor Master AI through mma-bridge commands, inspect running instances, query meteor detection results, start analyses, export outputs, and manage saved detections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive stream URLs, local file paths, proxy settings, coordinates, and device metadata through Meteor Master AI API responses.

Mitigation: Treat getCurrentInfo and getDataDetail output as sensitive, avoid sharing raw responses, and redact stream credentials, paths, coordinates, and device metadata before reuse.

Risk: The skill supports irreversible or state-changing operations such as delete, collect, uncollect, analyze, and export actions.

Mitigation: Require explicit user confirmation before issuing state-changing commands, especially bulk delete requests, and confirm selected IDs and target port before execution.

Risk: The skill depends on a locally installed mma-bridge npm package and a reachable Meteor Master AI MMABridge instance.

Mitigation: Install only from a trusted mma-bridge package source, pin or verify the package where possible, avoid administrator installs, and use the list command to target the intended running instance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mordom0404/skills/mma-bridge)
- [MMA Bridge API specification](references/api_spec.md)
- [getCurrentInfo API](references/getCurrentInfo.md)
- [getDataList API](references/getDataList.md)
- [getDataDetail API](references/getDataDetail.md)
- [deleteGroup API](references/deleteGroup.md)
- [collect API](references/collect.md)
- [incollect API](references/incollect.md)
- [exportTrackImg API](references/exportTrackImg.md)
- [exportGroupVideo API](references/exportGroupVideo.md)
- [analyzeVideoFile API](references/analyzeVideoFile.md)
- [analyzeImageFolder API](references/analyzeImageFolder.md)
- [analyzeLiveStream API](references/analyzeLiveStream.md)
- [stopAnalyze API](references/stopAnalyze.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target a local Meteor Master AI MMABridge instance, commonly on port 9000.]

## Skill Version(s):

1.2.7 (source: server-resolved release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
