## Description:

Generates platform-specific photography captions for Instagram, Flickr, X, Glass, Reddit, and other communities using the photo scene, equipment details, mood, and publishing context provided by the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Photographers, social media managers, and publishing teams use this skill to turn a single photo brief into distinct captions tailored to multiple photography and social platforms. It is best suited for caption drafting and platform formatting, not for replacing human judgment about creative intent, privacy, likeness rights, or copyright.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found that the skill asks for shell execution, file-write authority, and an under-explained callback URL beyond what caption drafting normally requires.

Mitigation: Install and run it with minimal permissions; avoid exec, write, API-key, and callback access unless those authorities are sandboxed and clearly needed.

Risk: Photo captions may expose private locations, sensitive metadata, likeness information, or confidential client context.

Mitigation: Do not provide sensitive photos, private metadata, credentials, or confidential publishing details unless the execution environment is trusted and constrained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/photo-caption-2)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text caption sets organized by platform]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific titles, caption bodies, equipment lines, tags, topic suggestions, and brief clarification prompts when user-supplied photo context is incomplete.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.2.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
