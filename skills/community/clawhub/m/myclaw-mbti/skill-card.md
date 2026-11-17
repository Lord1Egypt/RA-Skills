## Description:

Claw Mbti analyzes recent natural-language interactions with an OpenClaw agent to produce a playful MBTI-style personality report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyang0807](https://clawhub.ai/user/xiaoyang0807)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users use this skill to ask their assistant for an MBTI-style personality diagnosis based on recent conversation patterns. The skill can produce a full report when enough interaction history exists, or a lighter prompt/initial impression when history is limited.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill profiles recent conversations and memory to infer personality traits, which may surface sensitive behavioral details.

Mitigation: Use only when the user is comfortable with that profiling scope, and review the generated evidence before sharing or retaining the report.

Risk: The skill can include share prompts and installation prompts in its output.

Mitigation: Confirm share/install text is appropriate for the audience, and remove promotional prompts when they are not wanted.

Risk: The GitHub install/update command fetches and runs content from a remote repository path.

Mitigation: Prefer trusted ClawHub installation flows, and review the remote repository before running GitHub install or update commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoyang0807/skills/myclaw-mbti)
- [Publisher profile](https://clawhub.ai/user/xiaoyang0807)
- [Project homepage](https://github.com/xiaoyang0807/claw-mbti)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include share prompts and installation or update commands; report content is based on recent conversation and memory when available.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
