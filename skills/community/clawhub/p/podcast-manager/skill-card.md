## Description:

Find, subscribe to, track, and summarize podcast episodes using public RSS feeds and lightweight local tracking files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage podcast subscriptions, check recent RSS or Atom episodes, track listening state, bookmark episodes, and produce concise catch-up notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled feed-checking script can be tricked into contacting private or internal network addresses when arbitrary feed URLs are supplied.

Mitigation: Review before installing where untrusted feed URLs may be fetched; use trusted podcast feed URLs and prefer versions that revalidate redirect targets or restrict fetching to known public podcast hosts.

## Reference(s):

- [Podcast Manager ClawHub listing](https://clawhub.ai/ppopen/skills/podcast-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown responses, JSON tracking files, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local podcast subscription, state, and notes files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
