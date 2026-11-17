## Description:

Html2screenshot converts local HTML files, URLs, or HTML strings into full-page PNG screenshots with configurable viewport and scale settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[changyogpt-code](https://clawhub.ai/user/changyogpt-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to capture complete PNG images of HTML pages for reporting, preview, validation, and visual review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrary active HTML is rendered in Chrome, and release security evidence notes disabled sandboxing.

Mitigation: Run the skill only in an isolated environment with Chrome sandboxing enabled or enforced externally, a fresh browser profile, and strict resource limits.

Risk: The documented HTTP service may be reachable on a local network without clear isolation or access controls.

Mitigation: Bind service access to localhost or add authenticated access controls and network egress restrictions before using it with sensitive or untrusted content.

Risk: External URLs or HTML can load remote resources during screenshot capture.

Mitigation: Use network egress controls and avoid sensitive inputs unless the execution environment is isolated from internal networks and credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/changyogpt-code/skills/html2screenshot)
- [ClawHub publisher profile](https://clawhub.ai/user/changyogpt-code)
- [Dataset and validation notes](artifact/dataset.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JavaScript snippets, JSON request examples, and PNG screenshot outputs from execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots are generated as full-page PNG images with viewport and device scale settings.]

## Skill Version(s):

1.0.0 (source: release evidence, artifact frontmatter, and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
