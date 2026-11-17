## Description:

Generates meme captions, common meme template suggestions, and short reaction text for topic-based meme creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to draft meme captions, select familiar meme formats, and produce short reaction or template text for social posts and messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided command text can be retained in local log files by one bundled script.

Mitigation: Avoid passing secrets, private project names, or sensitive search terms; use a disposable or reviewable MEME_GENERATOR_DIR and clear local logs when needed.

Risk: The advertised meme purpose does not fully match all bundled utility behavior.

Mitigation: Review available commands before use and limit execution to the expected local meme text and template workflows.

Risk: Script output includes unavoidable publisher branding.

Mitigation: Review generated text before publishing or sharing it in contexts where branding is not appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/meme-generator)
- [BytesAgain homepage](https://bytesagain.com)
- [BytesAgain feedback](https://bytesagain.com/feedback)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys are required; MEME_GENERATOR_DIR can be set to change the local data directory.]

## Skill Version(s):

2.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
