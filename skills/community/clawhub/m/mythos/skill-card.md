## Description: <br>
Recurrent-depth reasoning via iterative refinement for complex analysis, multi-hop problems, design decisions, strategic planning, and questions where single-pass answers would be shallow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chitinlabs](https://clawhub.ai/user/chitinlabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and other external users use Mythos to apply a structured recurrent-depth reasoning protocol to complex questions, design decisions, strategic planning, and multi-hop analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional broad auto-activation can make the skill apply to everyday prompts where structured deep reasoning is unnecessary. <br>
Mitigation: Review the optional CLAUDE.md snippet before global use and scope activation to prompts that need complex analysis. <br>
Risk: High-complexity or explicit agent mode can use multiple parallel model calls, increasing cost and verbosity. <br>
Mitigation: Reserve deep or agent mode for questions that benefit from independent perspectives; use quick or silent mode for routine questions. <br>
Risk: The skill can produce confident reasoning guidance even though reasoning quality is manually judged rather than programmatically verified. <br>
Mitigation: For high-stakes decisions, review load-bearing assumptions, use trace mode when auditability is needed, and validate conclusions against external evidence. <br>


## Reference(s): <br>
- [Mythos on ClawHub](https://clawhub.ai/chitinlabs/mythos) <br>
- [Project homepage](https://github.com/chitinlabs/mythos-skill) <br>
- [Agent Mode Blueprint](references/agent-blueprint.md) <br>
- [Reasoning Lenses](references/lenses.md) <br>
- [Prompt Templates](references/prompt-templates.md) <br>
- [Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Markdown, Text] <br>
**Output Format:** [Markdown response with mode-specific sections, answers, and concise reasoning footers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route between direct, silent, trace, and parallel agent modes based on complexity or explicit mode keywords.] <br>

## Skill Version(s): <br>
0.1.1 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
