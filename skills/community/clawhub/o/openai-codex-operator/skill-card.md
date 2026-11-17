## Description:

Run OpenAI Codex CLI from OpenClaw for coding tasks in a target project directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cecwxf](https://clawhub.ai/user/cecwxf)

### License/Terms of Use:


## Use Case:

Developers and engineering operators use this skill to launch, monitor, and troubleshoot OpenAI Codex CLI tasks from OpenClaw for implementation, debugging, refactoring, review, and scripted coding workflows in a target repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Codex can read and change files in the selected repository when launched through this skill.

Mitigation: Use the skill only for repositories where that access is acceptable, verify the target workdir every time, and review diffs before keeping generated changes.

Risk: Task text used in raw command strings can create unsafe execution patterns if it includes untrusted input.

Mitigation: Avoid interpolating untrusted task text into shell command strings; keep command structure fixed and quote task content carefully.

Risk: Background Codex sessions may continue operating without immediate review.

Mitigation: Supervise background sessions, poll logs for prompts or failures, and stop sessions that are no longer needed.

## Reference(s):

- [OpenAI Codex](https://developers.openai.com/codex)
- [OpenAI Codex CLI](https://developers.openai.com/codex/cli)
- [OpenAI Codex Quickstart](https://developers.openai.com/codex/quickstart)
- [Codex docs summary](references/codex-doc-summary.md)
- [Codex usage recipes](references/codex-usage-recipes.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and tool parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include milestone status, remediation steps for missing Codex CLI or authentication, and monitoring instructions for background sessions.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
