## Description: <br>
Run a full market research and strategy analysis workflow using 12 specialized prompts for market sizing, competition, personas, trends, pricing, go-to-market, financial modeling, risk, market entry, and executive synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdullah4ai](https://clawhub.ai/user/abdullah4ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, business operators, founders, analysts, and developers use this skill to turn a business description into a structured market research and strategy report. The workflow gathers business context, runs staged analyses, and delivers an executive summary, priority actions, and a saved HTML report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may collect sensitive business context, financial assumptions, and generated strategy reports during research workflows. <br>
Mitigation: Use only approved business inputs, avoid credentials, regulated data, unreleased strategy, and proprietary financials unless authorized, and review retained artifacts after completion. <br>
Risk: The workflow saves reports, logs, raw data, and feedback in the workspace, which may be accessible beyond the immediate run. <br>
Mitigation: Run in an appropriate workspace, limit access to generated artifacts, and remove or protect saved reports and logs when they contain confidential information. <br>


## Reference(s): <br>
- [McKinsey Research Skill Page](https://clawhub.ai/abdullah4ai/mckinsey-research) <br>
- [Security Guidance](references/security.md) <br>
- [Variable Map](references/variable-map.md) <br>
- [Prompts Index](references/prompts.md) <br>
- [Gotchas](references/gotchas.md) <br>
- [Saudi Market Reference](references/saudi-market.md) <br>
- [Industry Benchmarks](references/benchmarks.md) <br>
- [HTML Report Template](templates/report.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown response plus saved HTML report and supporting Markdown analysis files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final report is saved under artifacts/research/{date}-{slug}.html; intermediate analyses, raw data, execution logs, and feedback may also be saved in the workspace.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
