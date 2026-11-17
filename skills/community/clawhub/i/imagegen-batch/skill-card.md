## Description:

This skill guides an agent through generating batches of images while preventing filename collisions, handling watermarks, and organizing the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT

## Use Case:

People using image-generation agents can create coordinated batches of illustrations, covers, and other image assets, then name, crop, and archive the results consistently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The prompts and filename requirements are Chinese-language.

Mitigation: Confirm that the user's language and workflow support Chinese prompts and filenames before using the skill.

Risk: The security scan had partial component coverage and a tool-misuse analysis parser limit.

Mitigation: Review the skill's behavior and tool use before enabling it in an agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/imagegen-batch)
- [Image style library](references/style-library.md)

## Skill Output:

**Output Type(s):** [Image files, Shell commands, Code, Guidance]

**Output Format:** [Generated image files with Markdown guidance, shell commands, Python code, and JSONL manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch size, output directory, naming, dimensions, and optional cropping or framing depend on the task.]

## Skill Version(s):

1.5.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
