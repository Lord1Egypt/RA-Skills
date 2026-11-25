## Description:

Delegates to a local Muse Glimmer via ollama.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to delegate tasks to a locally hosted Muse Glimmer model through Ollama, including when prompts must stay on the machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation instructions pipe a downloaded Ollama installer directly into a shell, which could run unverified remote code.

Mitigation: Avoid the direct download-to-shell command. Use an existing Ollama installation or a trusted signed package, and review and verify any installer before running it. The scan was partial and did not establish that all referenced material was assessed.

## Reference(s):

- [Conjure plugin homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown response saved as a delegation result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt and file context are sent to a locally served Muse Glimmer model through Ollama.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
