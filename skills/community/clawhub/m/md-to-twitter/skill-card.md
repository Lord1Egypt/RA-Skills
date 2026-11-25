## Description:

Converts Markdown articles into X threads and can publish them with attached images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writers use this skill to turn Markdown articles into X threads, retaining links and optionally attaching local images. They can review or copy the thread, or publish it through X.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using --post uploads images and publishes the thread through X using OAuth credentials.

Mitigation: Review the thread and image attachments before posting, and use credentials only in an environment you trust.

Risk: The security assessment flags rendering and file-writing side effects during dry runs; coverage is incomplete and some local references were unresolved.

Mitigation: Review the rendering, dry-run file behavior, and unresolved references before using image-rendering options or --dry-run.

## Reference(s):

- [md-to-twitter on ClawHub](https://clawhub.ai/j3ffyang/skills/md-to-twitter)
- [X API](https://api.x.com)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Numbered plain-text thread file (.txt)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts are split using X weighted character limits; local images can be attached and the thread can optionally be published.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
