## Description: <br>
AI-driven quantitative strategy iteration workflow - a complete loop of briefing, hypothesis, code generation, constitutional scan, backtest submission, forensic diagnosis, and lesson recording for QuantConnect strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tltby12341](https://clawhub.ai/user/tltby12341) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative strategy authors use this skill to run a disciplined iteration loop for QuantConnect strategies: gather context, form one testable mutation, scan generated code, submit staged backtests through companion tools, diagnose results, and record lessons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill coordinates local strategy files and records lessons in persistent memory. <br>
Mitigation: Review file paths and require confirmation before persistent memory updates. <br>
Risk: Backtest submission depends on companion skills and can trigger external QuantConnect workflows. <br>
Mitigation: Review companion skills separately and require confirmation before any backtest submission. <br>
Risk: Dependency or companion-skill drift can affect reproducibility. <br>
Mitigation: Pin Python dependencies and companion skill versions when reproducible strategy iteration is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tltby12341/phoenix-iterate) <br>
- [Publisher profile](https://clawhub.ai/user/tltby12341) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-style records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates local strategy files, local memory records, and companion backtest/forensics skills.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
