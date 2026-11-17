## Description:

Optimize prompts for clarity and effectiveness. Use when user says "improve this prompt", "optimize my prompt", "make this clearer", or provides vague/unstructured prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tolibear](https://clawhub.ai/user/tolibear)

### License/Terms of Use:

MIT

## Use Case:

Developers and other agent users use Promptify Skill to turn vague or unstructured requests into optimized prompts. The skill can ask clarifying questions, gather codebase context, or use web research when the prompt calls for it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated clipboard commands can be unsafe when prompts contain quotes or shell-like text.

Mitigation: Review the generated command before running it, or copy the optimized prompt manually.

Risk: Codebase and web modifiers can expose local project context or prompt details during research.

Mitigation: Use those modifiers only when local context review or web research is intended and acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with a prompt code block, a clipboard shell command, and a short explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May incorporate image context, conversation context, codebase research, or web research depending on prompt content and modifiers.]

## Skill Version(s):

3.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
