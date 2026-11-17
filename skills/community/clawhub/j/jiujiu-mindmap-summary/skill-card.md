## Description:

Generates JSON mind-map summaries in the simple_mind_map format from supplied text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cx17030204-dotcom](https://clawhub.ai/user/cx17030204-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to summarize provided text into a JSON mind map. It is intended for workflows that need simple_mind_map output from a text input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user text and an API key to an under-disclosed HTTP service on 127.0.0.1:8000.

Mitigation: Review the local service before use and avoid submitting confidential, proprietary, regulated, or secret-bearing text unless you control and trust that service.

Risk: The skill documentation mentions a shared trial API key.

Mitigation: Replace any shared trial key with a unique key and prefer authenticated HTTPS or protected local IPC before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cx17030204-dotcom/skills/jiujiu-mindmap-summary)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, configuration]

**Output Format:** [Markdown heading followed by pretty-printed JSON returned by the generation service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and the JIUJIUMINDMAP_API_KEY environment variable.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
