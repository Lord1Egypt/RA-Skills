## Description:

OpenClaw Guardian is a security-layer plugin for OpenClaw that checks exec, write, and edit tool calls with blacklist rules, LLM intent verification, and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatcatmaofei](https://clawhub.ai/user/fatcatmaofei)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add a review layer around risky OpenClaw tool calls before execution. It is intended to help catch destructive shell commands and sensitive file edits while preserving fast handling for ordinary operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent conversation text may be sent to a configured model provider during LLM intent checks.

Mitigation: Confirm provider data-handling requirements and add redaction or scoping controls before using the plugin with sensitive conversations.

Risk: The security evidence says the advertised protections appear incomplete or possibly not loadable.

Mitigation: Verify that the plugin loads in the target OpenClaw environment and treat it as defense-in-depth rather than a complete safety boundary.

Risk: Dangerous operations may bypass blacklist coverage if session scoping, path coverage, or bypass cases are incomplete.

Mitigation: Require documented path coverage and targeted tests for blacklist bypass, session scoping, and redaction behavior before relying on it.

## Reference(s):

- [OpenClaw Guardian README](references/README.md)
- [ClawHub skill page](https://clawhub.ai/fatcatmaofei/skills/openclaw-guardian)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration]

**Output Format:** [String responses and JSONL audit entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Blacklist hits can trigger LLM intent checks and append tamper-evident audit log entries.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact plugin metadata also reports 2.0.0 and package metadata reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
