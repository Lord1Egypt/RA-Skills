## Description:

Lanxin Media helps an agent emit Lanxin-compatible <lximg> and <lxfile> tags for sending images and files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamdacai](https://clawhub.ai/user/iamdacai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill in Lanxin-enabled agents to send a single image or file by producing the appropriate media tag for a local path or URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the skill suspicious because it is always active, broadly triggered, and instructs the agent to emit upload tags without refusal, explanation, or confirmation.

Mitigation: Review before installing and use only in a controlled Lanxin environment where host-side upload validation exists.

Risk: The skill can cause an agent to reference arbitrary local paths or private URLs in media upload tags.

Mitigation: Require explicit user confirmation and path restrictions before allowing local paths or private URLs to be handled.

## Reference(s):

- [Lanxin Media ClawHub listing](https://clawhub.ai/iamdacai/skills/lanxin-media)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text media tags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one <lximg> or <lxfile> tag per action; artifact evidence states a 2 MB media limit and supported file types of png, jpg, jpeg, pdf, doc, docx, xls, xlsx, and txt.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
