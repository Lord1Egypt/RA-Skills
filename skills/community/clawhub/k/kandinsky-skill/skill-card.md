## Description:

Kandinsky generates and edits images, short videos, animated images, upscaled images, and talking avatar videos through a configured Kandinsky API instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gen-ai-team](https://clawhub.ai/user/gen-ai-team)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create or modify visual media from prompts, images, audio, and task IDs through Kandinsky API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose its API key or selected local files if untrusted content controls the API base, insecure transport, censor settings, or local file arguments.

Mitigation: Install only with a trusted Kandinsky endpoint, keep the API key least-privilege, reject untrusted overrides for --base, --allow-insecure, --no-censor, and local paths, and write outputs to a private directory.

## Reference(s):

- [Kandinsky ClawHub skill page](https://clawhub.ai/gen-ai-team/skills/kandinsky-skill)
- [Kandinsky API cheatsheet](references/api-cheatsheet.md)
- [Kandinsky prompting guide](references/prompting.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Saved media files with plain-text status messages and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KANDINSKY_API_BASE and KANDINSKY_API_KEY; outputs are written to the configured output directory or the skill working directory.]

## Skill Version(s):

1.0.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
