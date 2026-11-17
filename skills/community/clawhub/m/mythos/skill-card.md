## Description:

Recurrent-depth reasoning via iterative refinement for complex analysis, multi-hop problems, design decisions, strategic planning, and questions where single-pass answers would be shallow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chitinlabs](https://clawhub.ai/user/chitinlabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and analysts use Mythos to route complex questions through silent, trace, or parallel-agent reasoning workflows. It is intended for decisions and analyses that benefit from iterative refinement, explicit lenses, and surfaced assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled CLAUDE.md snippet can persistently change how future non-trivial agent requests are routed.

Mitigation: Install only the /mythos command unless persistent global reasoning behavior is intentional, and review the snippet before adding it to CLAUDE.md.

Risk: Calibration instructions refer to external scripts from the source repository rather than scripts bundled in the marketplace artifact.

Mitigation: Inspect external calibration scripts and pin or verify the source revision before running them.

Risk: Agent mode may dispatch multiple parallel subagents, increasing cost and exposing more intermediate reasoning surface.

Mitigation: Use agent mode only for high-complexity questions or explicit deep/agent invocations, and prefer silent mode for ordinary complex questions.

Risk: Reasoning quality is not fully programmatically verifiable; the included tests are structural calibration checks.

Mitigation: Treat calibration failures as review signals and manually assess whether the selected lenses match the actual question.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chitinlabs/skills/mythos)
- [Source Homepage](https://github.com/chitinlabs/mythos-skill)
- [Agent Mode Blueprint](references/agent-blueprint.md)
- [Lens Library](references/lenses.md)
- [Prompt Templates](references/prompt-templates.md)
- [Mythos in Action - Annotated Examples](references/examples.md)
- [Mythos Reasoning Protocol - CLAUDE.md Snippet](references/mythos-init.md)
- [Tests and Calibration Notes](tests/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown answers with mode-dependent structure: compact coda, visible trace rounds, or parallel subagent findings with a merge.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include lens-path footers, load-bearing assumptions, convergence notes, and residual uncertainty depending on mode.]

## Skill Version(s):

0.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
