## Description: <br>
君黎AI拆书 helps an agent turn a user-provided local .txt web novel into a reusable writing-reference package with one book profile, six method cards, and selected case cards, rather than a plot summary or literary review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljunn](https://clawhub.ai/user/ljunn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and writing-focused agents use this skill to analyze a local long-form Chinese web novel and organize the result into reusable creative reference assets. It is intended for book-profile, writing-method, and case-card extraction, not continuation writing, chapter rewriting, or general literary criticism. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the local novel text file selected by the user and stores source-path metadata and derived chunks in a project directory. <br>
Mitigation: Use non-confidential source texts unless local persistence is acceptable, and review or delete generated project files after the analysis is complete. <br>
Risk: Generated method cards and case cards may overgeneralize from a single work if weak evidence is retained. <br>
Mitigation: Run the provided check workflow and keep only cards with clear chunk evidence, explicit reuse value, and notes about what should not be copied directly. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ljunn/junli-story-analysis) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/ljunn) <br>
- [Practical Workflow](references/practical-workflow.md) <br>
- [Analysis Pipeline](references/analysis-pipeline.md) <br>
- [Chunk Card Guide](references/chunk-card-guide.md) <br>
- [Mode Selection](references/mode-selection.md) <br>
- [Quality Checklist](references/quality-checklist.md) <br>
- [Output Templates](references/output-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and local project folders, with shell commands for init, resume, check, finalize, and repair workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a fixed 1 + 6 + N writing-reference package: one book profile, six method cards, and as many case cards as the source material supports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
