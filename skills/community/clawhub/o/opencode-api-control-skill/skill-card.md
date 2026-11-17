## Description:

A powerful skill to control Open Code CLI via a local web server API. Allows executing commands, managing sessions, and automating code generation remotely in the local network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[malek262](https://clawhub.ai/user/malek262)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to orchestrate OpenCode coding sessions through a local API, including session creation, provider selection, task submission, progress monitoring, and diff summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents unauthenticated network control of a code-writing service.

Mitigation: Keep the OpenCode server bound to 127.0.0.1 unless real authentication and network controls are added.

Risk: The skill asks agents to trust generated changes without directly inspecting source files.

Mitigation: Use a disposable project directory and review generated diffs and source files before trusting or deploying results.

Risk: Prompts, logs, state files, or third-party providers may expose secrets or proprietary code.

Mitigation: Avoid sending secrets or proprietary code through prompts, logs, state files, or model providers.

## Reference(s):

- [API Quick Reference](Reference/API_QUICK_REFERENCE.md)
- [Complete Workflow Examples](Reference/COMPLETE_EXAMPLES.md)
- [Event Monitoring Guide](Reference/EVENTS_GUIDE.md)
- [Providers & Models Reference](Reference/PROVIDERS_REFERENCE.md)
- [State Management Guide](Reference/STATE_MANAGEMENT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include OpenCode session IDs, status summaries, provider/model selections, event updates, and diff summaries.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
