## Description:

Advertises a voice-cloning workflow for Kling and Vidu audio clone models through a remote model API that requires TEAM_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lrshu](https://clawhub.ai/user/lrshu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to invoke a third-party remote model endpoint for voice-clone generation from a selected model and prompt. Reviewers should confirm the runtime interface and endpoint configuration before production use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's runnable code can send prompts, credentials, and media files to a remote endpoint beyond the advertised voice-clone use case.

Mitigation: Use only with a trusted publisher, scoped TEAM_API_KEY, and trusted TEAM_BASE_URL; avoid sensitive prompts, local paths, or media unless the endpoint has been reviewed.

Risk: The documented voice-clone example does not match the script's actual command-line interface.

Mitigation: Verify supported flags and expected model inputs before installing or using the skill in production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lrshu/skills/lrshuai-voice-clone)
- [Publisher Profile](https://clawhub.ai/user/lrshu)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Command-line invocation guidance with JSON or text responses from the remote API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TEAM_API_KEY; TEAM_BASE_URL can configure the remote endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
