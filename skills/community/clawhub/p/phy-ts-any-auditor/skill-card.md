## Description: <br>
TypeScript `any` sprawl auditor and type-coverage enforcer that scans TypeScript projects for explicit and implicit `any` usage, TypeScript suppression comments, weak tsconfig safety settings, and type-coverage gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to audit TypeScript repositories for type-safety debt, prioritize files with high `any` density, and generate CI guidance for type-coverage enforcement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local audit commands and may generate or suggest `.type-coverage` and CI threshold settings. <br>
Mitigation: Run it only in the intended repository and review generated coverage budgets or CI thresholds before committing them. <br>
Risk: The workflow can invoke `npx --yes type-coverage` at runtime. <br>
Mitigation: For sensitive projects, pin or preinstall the `type-coverage` package instead of relying on runtime package resolution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-ts-any-auditor) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with shell commands, tables, TypeScript examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose a `.type-coverage` CI budget and threshold guidance based on local project findings.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
