## Description:

Render parameterized prompt templates from a catalog with {{var}} variable filling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt engineers, and agent platform teams use this skill to list, render, and validate reusable prompt templates with named variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions tell users to download mutable remote Python code without pinning or verification.

Mitigation: Install from the reviewed bundled file, or require an immutable commit URL plus checksum or signature verification before execution.

Risk: The included verification harness can execute checks against local product directories.

Mitigation: Run the verification harness only on trusted directories or inside a sandbox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itspremkumar/skills/prompt-templates-cli)
- [README.md](artifact/README.md)
- [prompt_templates_cli.py](artifact/prompt_templates_cli.py)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text CLI output and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print missing-variable warnings before the rendered prompt.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
