## Description:

HokiPoki routes tasks from an agent to Claude, Codex, or Gemini through the HokiPoki CLI for second opinions, model switching, and provider/listener workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[budjoskop](https://clawhub.ai/user/budjoskop)

### License/Terms of Use:


## Use Case:

External users and developers use HokiPoki to route coding or analysis tasks to another AI CLI for a second opinion, model switch, or team provider workflow without changing tabs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad file selection can send large portions of a project, including secrets or proprietary content, to another AI provider.

Mitigation: Use specific --files or narrow --dir selections, and avoid --all unless the repository has been checked for secrets and sensitive material.

Risk: Automatic patch application can introduce unwanted or incorrect changes into a repository.

Mitigation: Prefer --no-auto-apply for sensitive work, then manually review and test the saved patch before applying it.

Risk: Making .git writable for Codex weakens normal sandbox protections around repository mutation.

Mitigation: Only make .git writable temporarily when required for the patch workflow, then restore stricter sandbox settings.

Risk: The workflow depends on installing and trusting a global HokiPoki CLI before routing work through the service.

Mitigation: Pin or independently review the CLI before using it with sensitive repositories, credentials, or customer data.

## Reference(s):

- [HokiPoki CLI Command Reference](references/commands.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends parseable HokiPoki CLI output with --json and manual patch review with --no-auto-apply.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
