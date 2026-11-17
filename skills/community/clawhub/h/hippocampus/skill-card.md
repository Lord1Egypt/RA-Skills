## Description:

Persistent memory system for AI agents with automatic encoding, decay, and semantic reinforcement, based on Stanford Generative Agents (Park et al., 2023).

This skill is ready for commercial/non-commercial use.

## Publisher:

[impkind](https://clawhub.ai/user/impkind)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent builders use this skill to add persistent, cross-session memory to OpenClaw agents through transcript signal extraction, scored memory storage, recall, decay, and dashboard generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cross-session memory may store and reuse sensitive conversation history.

Mitigation: Enable the skill only when persistent memory is desired, review transcript access before enabling cron or memory search, and avoid storing secrets or sensitive personal disclosures.

Risk: Generated memory and dashboard files can retain or expose information after conversations have ended.

Mitigation: Inspect and delete memory/index.json, HIPPOCAMPUS_CORE.md, and generated dashboard files when retained context is no longer appropriate.

Risk: Security evidence reports script injection and dashboard rendering issues.

Mitigation: Fix those issues before using the skill in shared, adversarial, or high-sensitivity environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/impkind/skills/hippocampus)
- [Publisher profile](https://clawhub.ai/user/impkind)
- [Source repository listed in metadata](https://github.com/ImpKind/hippocampus-skill)
- [Stanford Generative Agents Paper](https://arxiv.org/abs/2304.03442)
- [Generative Agents reference implementation](https://github.com/joonspk-research/generative_agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands, JSON memory indexes, generated Markdown core-memory files, and generated HTML dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and jq; optional cron jobs run background encoding and daily decay.]

## Skill Version(s):

3.9.0 (source: evidence release.version and SKILL.md openclaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
