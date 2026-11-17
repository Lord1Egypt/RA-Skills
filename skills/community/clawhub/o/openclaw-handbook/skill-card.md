## Description:

Fetches live from docs.openclaw.ai for OpenClaw questions, using a whole-docs index, working scripts, CI-style selftest coverage, worked routing examples, and documented routes for SOUL, multi-agent, sessions, platforms, nodes, and ClawHub topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igornumeriano](https://clawhub.ai/user/igornumeriano)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to answer OpenClaw configuration, concepts, CLI, troubleshooting, provider, channel, skill, plugin, and marketplace questions from live OpenClaw documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist full user questions locally when recording routing misses.

Mitigation: Avoid asking questions that contain secrets, and prefer a patched version that redacts stored questions and stores logs with private permissions.

Risk: The security summary flags unsafe shell use with user input.

Mitigation: Review shell-command behavior before installing and prefer structured argument passing in a patched version.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/igornumeriano/skills/openclaw-handbook)
- [Publisher Profile](https://clawhub.ai/user/igornumeriano)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown answers with source URLs and occasional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are constrained to fetched OpenClaw documentation; fallback searches and routing misses may produce local logs.]

## Skill Version(s):

1.6.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
