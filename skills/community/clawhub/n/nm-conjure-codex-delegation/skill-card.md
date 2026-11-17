## Description:

Delegates to the OpenAI Codex CLI (codex exec)

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when delegation-core selects Codex to send a coding or analysis prompt to the Codex CLI, optionally with project files, and save the delegated response as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected project files may contain credentials or other sensitive data that is sent to OpenAI as part of a delegation prompt.

Mitigation: Review the files selected for delegation and exclude credentials and other sensitive content before running the skill.

Risk: The security scan was partial because two local path references could not be resolved.

Mitigation: Resolve and review those references before relying on the scan as a complete assessment.

Risk: The skill advises against exposing a job-level API key when a job checks out untrusted repository code.

Mitigation: Do not expose a job-level API key to untrusted repository jobs; delegate from a trusted context with credentials configured appropriately.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-conjure-codex-delegation)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)
- [Codex CLI headless login issue referenced by the skill](https://github.com/openai/codex/issues/9253)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown guidance with shell command examples; delegated responses are saved as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Selected project files may be included in the prompt; output can be saved under delegations/codex/.]

## Skill Version(s):

1.10.3 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
