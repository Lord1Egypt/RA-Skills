## Description:

Force every user-facing string from an AI agent into plain language a non-technical human can read.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monikazapisek](https://clawhub.ai/user/monikazapisek)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to rewrite agent task titles, status messages, errors, action previews, plans, and handoff summaries so non-technical readers can understand what is happening and what to do next.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may over-rewrite exact technical output, raw errors, identifiers, paths, or strict formats that a user intentionally needs.

Mitigation: Use it only for user-facing prose, and preserve required technical values in metadata, code blocks, logs, or parenthetical context when exact wording matters.

Risk: The skill tells an agent to push back when a user asks to keep technical terminology, which can conflict with legitimate expert workflows.

Mitigation: Confirm the audience and output destination; for technical readers, keep plain-language headlines while retaining precise terms as secondary details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/monikazapisek/skills/legible-agent-output)
- [Article Sources](references/articles-sources.md)
- [Jargon Categories](references/jargon-categories.md)
- [Before / After Examples](examples/before-after.md)
- [Evaluation Evidence](EVIDENCE.md)
- [Smashing Magazine - Designing For Agentic AI](https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/)
- [Hatchworks - Agent UX Patterns](https://hatchworks.com/blog/ai-agents/agent-ux-patterns/)
- [Exalt Studio - UX for AI Startups](https://exalt-studio.com/blog/uiux-design-for-ai-startups-best-practices-for-agents-tools-interfaces)
- [boost.ai - Common Conversational AI Mistakes](https://boost.ai/blog/common-conversational-ai-mistakes/)
- [Orange Loops - 9 UX Patterns to Build Trustworthy AI Assistants](https://orangeloops.com/2025/07/9-ux-patterns-to-build-trustworthy-ai-assistants/)
- [Medium Bootcamp - What UX Designers Should Understand About AI Agents](https://medium.com/design-bootcamp/what-ux-designers-should-understand-about-ai-agents-ded69d00ebf6)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain-language text or Markdown rewritten for user-facing agent output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No runtime network access, MCP server, code execution, or file generation is required by the skill.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
