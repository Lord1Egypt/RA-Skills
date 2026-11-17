## Description:

Measures multilingual text layout with Pretext and generates Markdown, JSON, and Canvas-oriented layout reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baojun-billion](https://clawhub.ai/user/baojun-billion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to measure multilingual text, calculate wrapped line layouts, estimate UI element height, and generate layout reports for virtual lists, Canvas/SVG rendering, editors, and layout validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published package bundles browser diagnostic and development tooling that can run local servers, automate desktop browsers, and post reports to URL-controlled endpoints.

Mitigation: For production use, keep to the normal text-measurement API or trim the package to the runtime dist library; run bundled diagnostics only in a reviewed, controlled local environment.

Risk: Bundled diagnostic pages can be risky when opened from untrusted links or combined with unreviewed report endpoints.

Mitigation: Open diagnostic pages only from trusted local package paths and review any report collection endpoint before execution.

## Reference(s):

- [Pretext GitHub](https://github.com/chenglou/pretext)
- [Pretext Demo](https://chenglou.me/pretext)
- [Pretext README](https://github.com/chenglou/pretext#readme)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration]

**Output Format:** [Structured measurement objects, Markdown reports, JSON reports, and Canvas layout configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are derived from caller-provided text plus font, width, line-height, whitespace, and Canvas styling options.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
