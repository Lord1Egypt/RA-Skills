## Description: <br>
Implements hub-and-spoke lazy loading to minimize token usage in large skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to design modular agent skills that load guidance only when context, user intent, and token budget make it relevant. It is most useful for multi-domain skills with operating-system, language, workflow, or reference modules that should remain deferred until needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad triggers may activate the skill when a user only needs a narrow workflow. <br>
Mitigation: Review and narrow triggers during installation when accidental activation is a concern. <br>
Risk: Examples cover caching, telemetry, git mutation, publishing, and service-management patterns that could be unsafe if copied into runtime behavior without review. <br>
Mitigation: Keep these adaptations explicit, user-controlled, and reviewed before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-leyline-progressive-loading) <br>
- [ClawHub Metadata Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code, shell examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; modules are selected progressively to manage token budget.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
