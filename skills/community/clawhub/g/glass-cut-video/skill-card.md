## Description:

Generate vertical WeryAI short videos of glass cutting and shattering from text prompts or public HTTPS glass images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn a glass-cutting brief or public HTTPS image into a 9:16 WeryAI video prompt, confirmed parameters, and generated video URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt text interpolated into a documented --json shell command can become local command execution.

Mitigation: Pass JSON through a shell-free argument array, stdin, or a temporary JSON file instead of building a shell command string from user text.

Risk: The skill uses a required WERYAI_API_KEY, network calls, and paid WeryAI credits.

Mitigation: Run it in a short-lived environment containing only the required API key, keep the key out of the skill package, and confirm parameters before paid wait runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/glass-cut-video)
- [WeryAI video API host](https://api.weryai.com)
- [WeryAI models API host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown response with parameter tables, command snippets, and returned video URLs or error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access, public HTTPS image URLs for image-to-video, and paid WeryAI credits for successful wait runs.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
