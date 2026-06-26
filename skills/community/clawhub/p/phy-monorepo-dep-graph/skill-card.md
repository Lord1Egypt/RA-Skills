## Description: <br>
Analyzes npm/yarn/pnpm, Cargo, and Go monorepos by reading manifest files to map internal dependencies, detect cycles and orphaned packages, flag coupling and version mismatches, and produce ASCII or Mermaid dependency graphs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to understand internal package relationships in monorepos before refactors, dependency cleanup, build troubleshooting, or architecture review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository package names, dependency relationships, or architecture details may be exposed when the agent summarizes a monorepo. <br>
Mitigation: Use the skill only in trusted chats and repositories where sharing manifest-derived structure is acceptable. <br>
Risk: Analysis depends on local manifest files and may miss dependency behavior that is not represented in package.json, Cargo.toml, go.mod, or workspace metadata. <br>
Mitigation: Review generated dependency findings before acting on cleanup, refactor, or build-order recommendations. <br>


## Reference(s): <br>
- [Canlah AI](https://canlah.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-monorepo-dep-graph) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with ASCII dependency trees, Mermaid diagrams, tables, and inline shell or code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include suggested remediation steps, impact analysis, and test commands based on local manifest inspection.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
