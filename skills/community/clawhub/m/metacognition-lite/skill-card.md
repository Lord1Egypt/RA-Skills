## Description:

Metacognitive Protocol for AI Agents: a lightweight, model-agnostic thinking framework that helps agents reduce hallucinations, fake completions, task drift, mid-task amnesia, and vague filler by using intent decoding, difficulty assessment, boundary declaration, execution monitoring, and delivery validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q7766206](https://clawhub.ai/user/q7766206)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to add a structured metacognitive layer to LLM-based agents through system prompts, framework wrappers, and delivery validation checklists. It is intended to improve task alignment, uncertainty handling, execution monitoring, and final answer completeness across model providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Best-interpretation execution can be inappropriate for irreversible or sensitive tasks.

Mitigation: Require explicit confirmation before deletion, purchases, account changes, public posting, credential use, or other irreversible or sensitive actions.

Risk: The auxiliary presentation script writes a local PowerPoint file to a hard-coded path.

Mitigation: Run the script only when a presentation file is wanted, and update the output path for the local environment before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/q7766206/skills/metacognition-lite)
- [Why Your AI Agent Fails - And How a Metacognitive Protocol Fixes It](artifact/article_why_your_ai_agent_fails.md)
- [Skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with prompt snippets, checklists, and Python example code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an optional Python presentation generator that can create a local PowerPoint file when run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
