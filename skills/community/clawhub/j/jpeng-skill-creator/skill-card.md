## Description:

Create new skills, modify and improve existing skills, and measure skill performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to draft, revise, test, evaluate, benchmark, and package agent skills. It supports both new skill creation and iterative improvement of existing skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or revised skill instructions may be too broad, ambiguous, or misleading.

Mitigation: Review generated skill descriptions and instructions before packaging or publishing, with particular attention to trigger scope and user-facing behavior.

Risk: The skill may create or edit local files while drafting skills, evals, benchmarks, or packages.

Mitigation: Run it in an appropriate workspace and review file changes before deployment or distribution.

Risk: Evaluation workflows can spawn agents and run local Python or Claude CLI commands.

Mitigation: Use it only where those tools are expected, inspect generated commands, and avoid running unreviewed workflows in sensitive environments.

Risk: Review pages or viewer processes may remain open after evaluation.

Mitigation: Stop any launched viewer process when review is complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-skill-creator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with code blocks, JSON snippets, file edits, and shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify skill files, evaluation metadata, benchmark outputs, packaged skill files, and review pages as part of the skill creation workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
