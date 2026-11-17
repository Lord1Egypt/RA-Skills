## Description:

Create, read, validate, and manage OKF (Open Knowledge Format) knowledge bundles for AI agents using Google's vendor-neutral markdown and YAML specification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akdira](https://clawhub.ai/user/akdira)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to create, inspect, validate, and maintain OKF knowledge bundles with markdown files, YAML frontmatter, and okf-toolkit CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing okf-toolkit directly from a mutable GitHub repository.

Mitigation: Review the okf-toolkit repository before installing, prefer a pinned commit or verified release, and install it in a virtual environment or container without administrator privileges or unnecessary access to sensitive files.

## Reference(s):

- [OKF Spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- [okf-toolkit](https://github.com/akdira/okf-toolkit)
- [ClawHub skill page](https://clawhub.ai/akdira/skills/okf-knowledge-format)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML frontmatter examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct use of the okf-toolkit CLI to create, validate, index, search, and inspect OKF bundles.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
