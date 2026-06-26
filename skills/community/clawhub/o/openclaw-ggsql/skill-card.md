## Description: <br>
Generate static charts from tabular data by converting YAML chart specifications into ggsql SQL syntax based on Grammar of Graphics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanzhidongyzby](https://clawhub.ai/user/fanzhidongyzby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to turn CSV, JSON, or SQL table data into ggsql chart queries for scatter plots, line charts, bar charts, histograms, boxplots, heatmaps, and related static visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private or sensitive data may be exposed if users upload it to the ggsql WASM playground. <br>
Mitigation: Use local ggsql-cli for private data and review datasets before using any web playground. <br>
Risk: Future releases could add automatic uploads, remote rendering, or broader filesystem access that changes the risk profile. <br>
Mitigation: Review security evidence for each new version before installation or deployment. <br>
Risk: ggsql syntax is described by the artifact as alpha-stage and may evolve. <br>
Mitigation: Validate generated SQL against the installed ggsql version and keep chart-generation templates aligned with current ggsql documentation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fanzhidongyzby/openclaw-ggsql) <br>
- [ggsql official website](https://ggsql.org) <br>
- [ggsql syntax documentation](https://ggsql.org/syntax/) <br>
- [ggsql example gallery](https://ggsql.org/gallery/) <br>
- [ggsql WASM playground](https://ggsql.org/wasm/) <br>
- [ggsql upstream repository](https://github.com/posit-dev/ggsql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML specifications, SQL snippets, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ggsql chart queries and guidance for SVG or PNG chart generation; outputs are static rather than interactive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
