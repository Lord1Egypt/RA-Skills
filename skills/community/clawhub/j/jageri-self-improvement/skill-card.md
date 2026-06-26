## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for coding-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jageri](https://clawhub.ai/user/jageri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to record command failures, user corrections, knowledge gaps, feature requests, and reusable workflow improvements so future sessions can avoid repeated mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Learning logs and promoted instruction files can accidentally retain sensitive project context, secrets, tokens, transcripts, or raw private output. <br>
Mitigation: Record concise summaries or redacted excerpts, and do not store secrets, tokens, full transcripts, or raw private outputs in .learnings or promoted agent instruction files. <br>
Risk: The optional PostToolUse error detector inspects command output for error patterns. <br>
Mitigation: Prefer project-scoped hooks and enable the activator-only workflow unless command-output inspection is acceptable for the workspace. <br>


## Reference(s): <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .learnings markdown files and optional hook configuration when the user enables that workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
