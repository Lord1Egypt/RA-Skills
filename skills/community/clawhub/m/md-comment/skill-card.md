## Description:

Open a browser tab so a human can highlight-and-comment on a Markdown file, then submit structured JSON comments the agent can read and respond to.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxl-lxz](https://clawhub.ai/user/zxl-lxz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect targeted human feedback on generated Markdown documents such as design docs, specs, READMEs, and PR descriptions before revising them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The browser viewer has security weaknesses that could expose reviewed Markdown content or comments.

Mitigation: Use the skill only when the reviewer is comfortable viewing the Markdown through a local browser UI.

Risk: Sensitive or untrusted Markdown may be unsafe until viewer dependencies and sanitization behavior are hardened.

Mitigation: Avoid sensitive or untrusted Markdown until dependencies are vendored or pinned, sanitization fails closed when unavailable, and dynamic UI uses safe DOM APIs.

Risk: The skill can launch a local server and open a browser.

Mitigation: Require explicit user approval before the agent launches the server or opens the browser.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/zxl-lxz/commentmd/tree/main/skills/commentmd)
- [ClawHub skill page](https://clawhub.ai/zxl-lxz/skills/md-comment)

## Skill Output:

**Output Type(s):** [json, guidance]

**Output Format:** [Structured JSON comments with quoted Markdown excerpts, anchor context, comment text, timestamps, and change-detection metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a comments JSON file next to the reviewed Markdown file, or export a downloadable JSON file in static mode.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
