## Description:

Guide users to VideoAny Image-to-Video, an uncensored AI video generator with multi-model support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoq1](https://clawhub.ai/user/gaoq1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to get concise guidance for turning a source image and prompt into a VideoAny web workflow. The skill helps select among listed image-to-video models and produce copy-ready inputs, but actual generation occurs on VideoAny.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill steers image-to-video requests toward an uncensored third-party web workflow.

Mitigation: Review VideoAny's terms, content rules, and organizational acceptability before using or recommending the workflow.

Risk: Users may upload sensitive, private, or proprietary images and prompts to VideoAny.

Mitigation: Do not upload restricted content unless privacy, rights, and data-handling requirements have been checked.

Risk: The skill declares shell execution even though the inspected helper scripts are mostly informational.

Mitigation: Review the shell permission before installation and run helper scripts only from a trusted copy of the skill.

## Reference(s):

- [VideoAny Image-to-Video](https://videoany.io/image-to-video)
- [ClawHub Skill Page](https://clawhub.ai/gaoq1/skills/image-to-video-any)
- [ClawHub Publisher Profile](https://clawhub.ai/user/gaoq1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with optional shell command examples and copy-ready web workflow inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No automatic upload or video generation; helper scripts print guidance for a third-party web workflow.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
