## Description: <br>
Distill successful multi-step OpenClaw sessions into reusable learned skills before compaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaocaijic](https://clawhub.ai/user/xiaocaijic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill after successful multi-step OpenClaw sessions to convert useful traces into reusable learned skills. It is intended for preserving concrete commands, file paths, failure triggers, and snippets when the same workflow may be useful later. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session traces may contain secrets, private source code, customer data, paths, or commands that should not be preserved in a reusable skill. <br>
Mitigation: Review and redact traces before distillation, use a controlled output directory, and inspect generated learned skills before reuse. <br>
Risk: Preserved commands or edits may be unsafe if replayed automatically in a different project, account, or environment. <br>
Mitigation: Treat generated workflows as guidance, not automatic execution plans, and confirm commands and file edits against the current context before use. <br>


## Reference(s): <br>
- [Trace Format](references/trace-format.md) <br>
- [ClawHub skill page](https://clawhub.ai/xiaocaijic/procedural-distiller) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Code, Files, Guidance] <br>
**Output Format:** [Generated skill directory containing SKILL.md, agents/openai.yaml, and memory.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local CLI reads JSON traces and writes learned skills under the configured output root when success and minimum tool-call criteria are met.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
