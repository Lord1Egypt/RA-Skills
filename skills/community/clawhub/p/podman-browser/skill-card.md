## Description:

Podman Browser runs a headless Chromium browser via Podman and Playwright to fetch text or HTML from JavaScript-rendered web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardodantas](https://clawhub.ai/user/ricardodantas)

### License/Terms of Use:

GPL-3.0 License

## Use Case:

Developers and agents use this skill to retrieve rendered page text or HTML from JavaScript-heavy websites without installing browser dependencies locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs supplied web pages in a browser/container setup with reduced isolation, including host IPC and disabled Chromium sandboxing.

Mitigation: Use trusted URLs, avoid sensitive internal sites, review the container settings before deployment, and prefer stronger sandboxing for regular use.

Risk: The container image is referenced by tag and pulled at runtime, which can change what code executes over time.

Mitigation: Use a prebuilt image pinned by digest before routine or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ricardodantas/skills/podman-browser)

## Skill Output:

**Output Type(s):** [Text, HTML, Shell commands]

**Output Format:** [Plain text or HTML emitted to stdout, with command-line options documented in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports URL input plus --html, --wait, and --selector options.]

## Skill Version(s):

1.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
