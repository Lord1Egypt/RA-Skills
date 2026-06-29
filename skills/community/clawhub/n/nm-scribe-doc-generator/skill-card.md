## Description: <br>
Generates or remediates documentation with human-quality writing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to draft new documentation, remediate AI-like writing, and apply quality gates to repository docs, contributor guidance, and code comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation or agent guidance changes could introduce inaccurate, misleading, or workflow-changing instructions. <br>
Mitigation: Review proposed edits before acceptance, especially changes to AGENTS.md, CONTRIBUTING.md, aliases, symlinks, and repository-wide guidance. <br>
Risk: The remediation workflow may change wording in a way that alters intended meaning. <br>
Mitigation: Use the skill's section-by-section review flow for larger documents and require user approval for major restructuring or unclear intent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-scribe-doc-generator) <br>
- [Scribe Plugin Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe) <br>
- [Generation Guidelines](artifact/modules/generation-guidelines.md) <br>
- [Quality Gates](artifact/modules/quality-gates.md) <br>
- [Remediation Workflow](artifact/modules/remediation-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown prose with optional code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose documentation edits, quality-gate results, and remediation steps for human review.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
