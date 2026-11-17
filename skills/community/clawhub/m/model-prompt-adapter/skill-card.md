## Description:

Model Prompt Adapter provides per-model Markdown addenda for workspace context files to reduce fallback-model issues such as scope creep, prompt leaking, and fabricated completion across an agent fallback chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to adapt shared workspace prompt files for mixed-model or fallback-model environments without maintaining separate prompt versions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes prompt files that influence future agent behavior.

Mitigation: Review the exact Markdown addenda before installation and apply them only in workspaces where the fallback-model guardrails are wanted.

Risk: Prompt guidance can become inaccurate or overbroad for a specific model chain or workspace policy.

Mitigation: Test the addenda in the target workflow and monitor for privacy leaks, unsolicited actions, and incorrect completion claims after applying them.

## Reference(s):

- [Cross-Model Prompting: OpenAI vs Anthropic](artifact/references/cross-model-prompting.md)
- [GPT-5.4 Documented Failure Modes](artifact/references/gpt-5.4-failure-modes.md)
- [ClawHub Skill Page](https://clawhub.ai/globalcaos/skills/model-prompt-adapter)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with workspace-file addenda]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; intended changes are Markdown prompt blocks added to existing workspace files.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
