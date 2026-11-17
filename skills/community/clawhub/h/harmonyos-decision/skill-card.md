## Description:

This skill helps developers evaluate HarmonyOS native app ideas by gathering market, competitor, user, monetization, promotion, and development signals and generating a multidimensional HTML feasibility report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and founders use this skill to assess whether a HarmonyOS native application idea is worth pursuing. It supports feasibility decisions with market research, ecosystem-specific development considerations, weighted scoring, and an HTML report.

### Deployment Geography for Use:

China-focused

## Known Risks and Mitigations:

Risk: Generated HTML may include unsanitized user-provided or web-sourced text that can run unwanted browser code when opened.

Mitigation: Treat generated reports as untrusted until inserted text is escaped and a restrictive Content Security Policy is added; review reports before sharing or opening them in sensitive browser contexts.

Risk: The skill relies on web search and user-provided product ideas, which may expose sensitive concepts to external search or retrieval tools.

Mitigation: Use only product ideas and supporting details that are acceptable to send through web search workflows.

Risk: The report generator writes to a user-selected output path.

Mitigation: Choose report output paths deliberately and avoid overwriting important local files.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/bettermen/skills/harmonyos-decision)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, html]

**Output Format:** [Markdown guidance with JSON parameters and a generated HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses web search inputs and report-generator data; generated HTML should be treated as untrusted according to the release security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
