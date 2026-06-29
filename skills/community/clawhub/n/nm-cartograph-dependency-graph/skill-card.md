## Description: <br>
Generates a Mermaid dependency graph showing import relationships between modules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze module import relationships, identify coupling or circular dependencies, and plan refactors with Mermaid dependency diagrams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation language can lead the agent to inspect more of a codebase than intended. <br>
Mitigation: Use explicit prompts with a target path, package, or module when requesting dependency analysis. <br>


## Reference(s): <br>
- [Cartograph plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, guidance] <br>
**Output Format:** [Markdown with Mermaid code blocks and concise analysis notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dependency counts, high fan-in and fan-out modules, and circular dependency notes.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
