## Description: <br>
Guides agents in building formula-driven Excel financial models with OfficeCLI, including 3-statement, DCF, LBO, SaaS unit economics, sensitivity, scenario, debt schedule, and fundraising models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iceyliu](https://clawhub.ai/user/iceyliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and finance teams use this skill to have an agent create auditable Excel financial models with separated inputs, calculations, outputs, formulas, validation gates, and OfficeCLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup instructions ask users or agents to run unverified remote installer code. <br>
Mitigation: Verify the OfficeCLI installer source and prefer a pinned release, package-manager install, or manually downloaded binary with checksum or signature verification before execution. <br>
Risk: Financial model formulas, cached values, or circular references can produce misleading workbook outputs if delivery gates are skipped. <br>
Mitigation: Run the skill's balance, cache, hardcode, convergence, and visual audit gates before relying on generated workbook results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iceyliu/skills/officecli-financial-model) <br>
- [OfficeCLI releases](https://github.com/iOfficeAI/OfficeCLI/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with bash and JSON command examples; generated workbook output is .xlsx.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on a single formula-driven workbook with model-specific validation gates.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
