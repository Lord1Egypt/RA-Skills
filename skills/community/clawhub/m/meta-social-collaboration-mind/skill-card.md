## Description:

Provides an agent with a social-collaboration strategy selector and a local learning note mechanism, while documenting self-verification, reflection, orchestration, and continual-improvement practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to assess partner expertise, confidence, workload, trust, and mood, then choose collaboration strategies such as delegate, consult, monitor, pair, or avoid. It also provides a learner script for recording local usage outcomes and preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The learner workflow keeps and reuses local cross-session notes and preferences.

Mitigation: Treat learned_patterns.json as untrusted local data, review or clear it regularly, and avoid storing sensitive information in it.

Risk: The artifact documentation encourages future instruction changes, including possible edits to SKILL.md.

Mitigation: Require explicit human review before any automatic instruction or skill-file change is applied.

Risk: The skill documentation overstates self-verification and reflection features that are not fully implemented in the provided artifact files.

Mitigation: Treat those features as documented practices unless supporting tools are installed, and manually review collaboration guidance before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-social-collaboration-mind)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, JSON]

**Output Format:** [Markdown guidance with optional shell command examples and JSON strategy output from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learned_patterns.json when the learner script is used.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
