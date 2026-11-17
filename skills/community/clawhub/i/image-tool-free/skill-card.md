## Description:

This skill helps agents inspect image dimensions and color settings, crop and resize images, convert common formats, compress outputs, and manage EXIF/ICC metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation users, and individual creators use this skill to guide an agent through lightweight image inspection, format conversion, compression, and metadata handling for local image files. It is best suited to single-image or small workflow tasks that can be carried out with available image tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trigger text is not clearly scoped to image-processing tasks.

Mitigation: Narrow activation guidance to image inspection, conversion, compression, cropping, resizing, and metadata-management requests.

Risk: The artifact includes an unnecessary credential-environment check.

Mitigation: Remove commands that enumerate API, key, token, or secret environment variables before release or installation.

Risk: Network or API behavior is mentioned without a clear scope.

Mitigation: Document any required network access explicitly and keep default workflows local unless network use is required by the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/image-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with shell command examples and optional JSON/text/CSV output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the agent runtime and locally available image tools.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
