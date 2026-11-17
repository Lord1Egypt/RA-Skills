## Description:

Optimize prompts for clarity and effectiveness. Use when user says "improve this prompt", "optimize my prompt", "make this clearer", or provides vague/unstructured prompts. Intelligently routes to sub-agents for codebase research, clarifying questions, or web search as needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tolibear](https://clawhub.ai/user/tolibear)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Promptify to turn vague or underspecified requests into structured prompts with clear role, task, constraints, and output expectations. It can ask clarifying questions, inspect relevant project context, or gather current web context when those steps are needed for better prompt optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated clipboard shell commands can be unsafe for untrusted or complex prompt text.

Mitigation: Review the generated prompt before execution and avoid running the `echo '...' | pbcopy` command for untrusted or complex content.

Risk: Prompt optimization may broaden into project file review or web research.

Mitigation: Use the skill only where codebase and web access are acceptable, and review any agent dispatch before relying on the result.

Risk: Server-resolved GitHub import provenance is unavailable for this version.

Mitigation: Prefer installation from the verified ClawHub publisher profile and pin the intended release version.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with a fenced optimized prompt, a clipboard shell command, and a short explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include clarifying questions or synthesized codebase and web research context before producing the optimized prompt.]

## Skill Version(s):

3.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
