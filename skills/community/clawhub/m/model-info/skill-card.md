## Description:

Get 100% accurate current model details including model name, provider, API endpoint, and session status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viratkumar123](https://clawhub.ai/user/viratkumar123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to ask for the currently active model, provider, API endpoint, session status, token and cost usage, and runtime configuration. It is useful for debugging and understanding multi-model runtime sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad model-status trigger phrases may cause the skill to answer during ordinary model-related conversation.

Mitigation: Invoke it explicitly with a clear request such as "model info" and review responses before sharing them outside the session.

Risk: Responses can disclose local runtime/session metadata, including provider, API key source/type, endpoint, token usage, cost, and configuration details.

Mitigation: Use only in sessions where exposing that metadata is acceptable, and avoid sharing output in public or untrusted channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viratkumar123/skills/model-info)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text status response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports runtime/session metadata such as current model, provider, API key source/type, endpoint, token usage, cost, and configuration when available.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
