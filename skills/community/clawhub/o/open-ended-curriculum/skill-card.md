## Description:

Generates progressively harder, non-repeating curriculum challenges for an agent and includes scripts for scoring novelty, value, feasibility, and alignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill when they want an agent to generate open-ended self-training tasks that increase in difficulty, avoid near-duplicates, and remain measurable through simple scoring. The skill also offers an optional learner workflow that records outcomes, preferences, and recurring errors to improve future use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The learner workflow can keep local history, notes, error records, and user preferences.

Mitigation: Use it only when persistent memory is intended, avoid recording sensitive information, and periodically review or clear learned_patterns.json.

Risk: The skill asks agents to write learned records back into SKILL.md.

Mitigation: Require human review before any instruction update, inspect the diff, and rescan the skill before deployment.

Risk: Automatically generated curriculum challenges may be unsuitable for the user's context even when they score well.

Mitigation: Review generated challenges before acting on them and adjust the seed, step count, or constraints when outputs are misaligned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/open-ended-curriculum)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-producing Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Curriculum output includes seed, steps, challenges, saturation status, maximum difficulty, and per-challenge scoring fields.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
