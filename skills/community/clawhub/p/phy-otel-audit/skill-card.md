## Description: <br>
OpenTelemetry instrumentation coverage auditor that scans Node.js, Python, Go, and Java source code for missing or misconfigured OTel instrumentation and produces per-file coverage findings with actionable fix snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to generate or run a local OpenTelemetry static audit for service repositories, identify instrumentation blind spots, and receive concrete remediation snippets for traces, resources, exporters, and CI gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit scans selected repository paths and can report private file names, line numbers, and source-adjacent snippets. <br>
Mitigation: Run it only on intended local paths and treat generated reports as internal when they contain private project structure or code context. <br>
Risk: A local otel_audit.py script that differs from the embedded skill code could perform unexpected actions. <br>
Mitigation: Before execution, confirm the script being run matches the embedded code supplied by the skill. <br>
Risk: Static OpenTelemetry checks can produce false positives, especially around auto-instrumentation and context that is not visible in a local source window. <br>
Mitigation: Review findings against actual instrumentation and trace behavior before using CI mode to block releases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-otel-audit) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline Python, shell, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local static-analysis reports with severity counts, file locations, remediation snippets, and optional CI failure behavior for HIGH findings.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
