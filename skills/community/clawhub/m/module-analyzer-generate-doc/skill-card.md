## Description:

Java/Maven single-module deep documentation generator. Generates L3(file-level) to L2(module-level) business logic docs for specified module. Supports multi-subagent parallel processing, context compression, checkpoint resume, and auto-retry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endcy](https://clawhub.ai/user/endcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate or update natural-language business logic documentation for a single Java/Maven module. It supports onboarding, code review preparation, legacy code understanding, and incremental documentation updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the target module's source code and generates documentation, state, and logs under .ai-doc.

Mitigation: Run it only on source trees the agent is allowed to inspect, review generated .ai-doc content, and keep the project under version control before execution.

Risk: The skill may ask to persist its operating rules in TOOLS.md.

Mitigation: Do not allow TOOLS.md changes unless persistent defaults for future agent sessions are explicitly desired.

Risk: The package metadata includes an npm generate command that invokes PowerShell with ExecutionPolicy Bypass.

Mitigation: Avoid npm run generate until that command is removed or replaced with a reviewed script.

## Reference(s):

- [L3 File Documentation Template](references/l3-file-template.md)
- [L2 Module Documentation Template](references/l2-module-template.md)
- [Task Execution Guide](references/task-execution-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/endcy/skills/module-analyzer-generate-doc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation files and progress/status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates L3 file-level docs, an L2 module-level index, task state, and logs under the target project's .ai-doc directory.]

## Skill Version(s):

1.0.5 (source: server release evidence; changelog released 2026-07-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
