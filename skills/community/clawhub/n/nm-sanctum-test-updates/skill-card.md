## Description: <br>
Updates, generates, and validates tests using git-workspace context and TDD/BDD methodology. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect code changes, identify test gaps, generate or update pytest/BDD test scaffolding, and validate test quality before commits or CI runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect code, create or update tests, and run validation commands, which may modify repository files or exercise untrusted project code. <br>
Mitigation: Use a clean git worktree or sandbox, review generated changes before committing, and run commands only against intended target paths. <br>
Risk: Mutation testing and broad scans can be slow or resource-intensive on large or sensitive repositories. <br>
Mitigation: Prefer targeted paths, quick mutation settings, and staged validation before running broad analysis. <br>
Risk: Generated test scaffolds or recommendations may not fully capture project-specific behavior or invariants. <br>
Mitigation: Have developers complete and review generated tests, confirm failing tests fail for the intended reason, and preserve invariant tests unless a human approves a design change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-sanctum-test-updates) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [modules/bdd-patterns.md](artifact/modules/bdd-patterns.md) <br>
- [modules/test-discovery.md](artifact/modules/test-discovery.md) <br>
- [modules/test-generation.md](artifact/modules/test-generation.md) <br>
- [modules/quality-validation.md](artifact/modules/quality-validation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, test scaffolds, and validation recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file changes and test commands; generated tests are intended for developer review and validation.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
