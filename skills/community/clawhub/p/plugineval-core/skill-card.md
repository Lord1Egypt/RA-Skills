## Description: <br>
Self-contained PluginEval quality evaluation engine. Measures 6 dimensions, detects anti-patterns, assigns badges. No external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donmeusi](https://clawhub.ai/user/donmeusi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use PluginEval Core to evaluate agent skill quality, detect documented anti-patterns, and assign quality badges before installation or publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional auto-fix write mode can modify SKILL.md and remove empty reference files in the target skill directory. <br>
Mitigation: Run the auto-fix preview first and apply --allow-write only on a version-controlled or disposable copy. <br>


## Reference(s): <br>
- [PluginEval Core ClawHub Page](https://clawhub.ai/donmeusi/plugineval-core) <br>
- [Quality Framework](references/quality-framework.md) <br>
- [Anti-Pattern Catalog](references/anti-pattern-catalog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON evaluation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only by default; optional write mode requires explicit --allow-write.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
