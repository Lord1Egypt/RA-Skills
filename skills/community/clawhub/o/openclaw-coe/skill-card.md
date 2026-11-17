## Description:

OpenClaw Chain of Execution (CoE) surfaces step-by-step execution progress for complex OpenClaw tasks, including decomposition, skill and model selection, calls, waiting states, results, warnings, and final summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyh17](https://clawhub.ai/user/liuyh17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to make long-running or complex agent tasks more transparent by showing concise execution-progress messages as work is decomposed, routed, executed, and summarized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic triggers may activate verbose execution-progress output when a user did not intend to enable it.

Mitigation: Narrow or disable automatic triggers such as '过程' if accidental activation would be distracting in the target environment.

Risk: Verbose process output could expose hidden chain-of-thought, private prompts, credentials, or sensitive intermediate data if used carelessly.

Mitigation: Use the tracker for execution status only, and redact or omit sensitive prompts, credentials, and private intermediate content from progress messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyh17/skills/openclaw-coe)
- [Publisher profile](https://clawhub.ai/user/liuyh17)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and terminal text with optional Python usage snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints concise progress messages and flushes standard output after each step; no network, credential, persistence, or destructive behavior was reported by the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
