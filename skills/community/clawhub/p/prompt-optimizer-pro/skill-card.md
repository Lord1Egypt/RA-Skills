## Description:

Prompt Optimizer helps users improve, diagnose, score, translate, compare, and save prompts for model-agnostic LLM workflows using templates and local prompt history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkpareek0315](https://clawhub.ai/user/mkpareek0315)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn rough prompts into clearer model instructions, generate prompt templates, diagnose weak outputs, and manage a local prompt library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores prompt history and saved prompts on local disk, which may include sensitive prompts, credentials, private business data, or regulated personal information.

Mitigation: Avoid using sensitive content unless local file permissions are understood, and clear the stored history and library when needed.

Risk: The skill can activate broadly for many prompt-writing requests and may persist more user content than expected.

Mitigation: Review when the skill activates and inspect saved files under ~/.openclaw/prompt-optimizer/ before continued use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkpareek0315/skills/prompt-optimizer-pro)
- [Publisher profile](https://clawhub.ai/user/mkpareek0315)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style text with prompt examples, local setup commands, JSON configuration snippets, and prompt guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local settings, prompt library, and history files under ~/.openclaw/prompt-optimizer/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
