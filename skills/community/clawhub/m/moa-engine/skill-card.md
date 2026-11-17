## Description:

moa-engine orchestrates specialized agent roles to analyze complex tasks through task classification, structured critique, synthesis, expert routing, and recursive self-improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiwifruit13](https://clawhub.ai/user/kiwifruit13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical decision makers use this skill when they need multi-perspective analysis, high-risk decision review, cross-domain solution design, or deep architecture review. It provides an agent workflow for classifying tasks, assigning expert roles, running structured critique, and synthesizing final guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a prompt-based, heuristic orchestration framework.

Mitigation: Install and use it only when heuristic agent orchestration is acceptable for the task, and review outputs before acting on them.

Risk: The skill can retain raw run logs that may contain sensitive or regulated information.

Mitigation: Avoid feeding secrets, personal data, regulated data, or confidential material into raw execution logs.

Risk: The skill can update persistent expert-routing state.

Mitigation: Use a scoped copy of the profile registry and review signal files before applying updates.

Risk: Generated system prompts may be combined with untrusted task content.

Mitigation: Separate trusted instructions from untrusted task content before sending generated prompts to a model.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kiwifruit13/skills/moa-engine)
- [PROJECT_OVERVIEW.md](references/PROJECT_OVERVIEW.md)
- [architecture-overview.md](references/architecture-overview.md)
- [moa-system-guide.md](references/moa-system-guide.md)
- [moa-meta-prompt.md](references/moa-meta-prompt.md)
- [moa-tag-system.md](references/moa-tag-system.md)
- [moa-routing-design.md](references/moa-routing-design.md)
- [moa-rhi-guide.md](references/moa-rhi-guide.md)
- [fitness-function.md](references/fitness-function.md)
- [patch-spec.md](references/patch-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with XML-style structures, JSON summaries, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prompt templates, risk scans, task classifications, expert profile recommendations, and registry update guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
