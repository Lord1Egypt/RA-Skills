## Description:

Helps ChatGPT and Codex resume multi-step work from source-linked checkpoints that preserve requirements, evidence, and pending actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users managing long-running projects use this workflow to preserve source-linked requirements, track verified progress, and resume the next authorized action after a handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkpoints may preserve project requirements and source references in a persistent location.

Mitigation: Review checkpoint storage and access before saving; omit secrets and unnecessary private data.

Risk: A stale or incomplete checkpoint can misstate progress or prompt a repeated operation.

Mitigation: Reconcile with authoritative sources, check the outcome of pending operations before retrying, and verify saved records on handoff.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ciklopentan/skills/long-task-context-gpt)
- [Continuation checks](references/continuation-checks.md)
- [Project checkpoint template](references/project-checkpoint-template.md)
- [Research basis and limits](references/research-basis.md)
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or JSON checkpoint and plain-text continuation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source-linked requirements, current state, pending actions, and the next recheck; saved files require available storage tools.]

## Skill Version(s):

1.1.0 (source: server-resolved release and SKILL.md heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
