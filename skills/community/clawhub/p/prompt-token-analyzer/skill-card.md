## Description:

Prompt Token Analyzer is a Node.js CLI tool that analyzes prompt token usage with a GPT-compatible tokenizer to help agents estimate prompt size, debug context overflow, and optimize token cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[putixiaosheng](https://clawhub.ai/user/putixiaosheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to estimate prompt token counts for files or raw text, troubleshoot context window overflow, and optimize prompts or RAG contexts before sending them to an LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks for system-wide installation with elevated privileges.

Mitigation: Review the generated script before installing it and prefer running it locally or placing it in a user-owned bin directory instead of using sudo.

Risk: The tokenizer dependency is installed without a pinned or verified package version.

Mitigation: Pin or verify the gpt-tokenizer package version before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/putixiaosheng/skills/prompt-token-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with bash commands, JavaScript CLI code, and text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; token counts are approximate and may differ from actual API usage.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
