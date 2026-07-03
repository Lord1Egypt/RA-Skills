## Description: <br>
Novel Weaver helps an agent run a structured novel-writing workflow with scene setup, outline planning, causality checks, gated chapter drafting, continuity validation, style checks, logic checks, fidelity review, ending verification, entity tracking, character aliases, and cross-chapter behavior summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and writing-focused agents use this skill to plan, draft, validate, and revise long-form fiction through a staged local workflow with explicit project state and quality gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores novel project content and workflow state in its local data directory. <br>
Mitigation: Use it only for content you are comfortable storing locally, and review the configured data directory before starting a project. <br>
Risk: Optional model setup may install Python packages, download large third-party models, and use trust_remote_code. <br>
Mitigation: Run optional model installation only intentionally, preferably in an isolated environment, and treat it as a separate trust decision from the base skill. <br>


## Reference(s): <br>
- [Novel Weaver on ClawHub](https://clawhub.ai/ldxs001/skills/novel-weaver) <br>
- [Execution Standards](references/execution_standards.md) <br>
- [Workflow Hooks and Gates](references/hooks.md) <br>
- [Examples](references/examples.md) <br>
- [Permissions](references/permissions.md) <br>
- [Changelog](references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands, JSON snippets, and generated novel prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include local project state updates, chapter text files, validation reports, gate status, and repair guidance.] <br>

## Skill Version(s): <br>
1.35.3 (source: frontmatter, _meta.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
