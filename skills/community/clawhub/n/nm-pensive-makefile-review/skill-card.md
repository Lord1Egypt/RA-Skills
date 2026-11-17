## Description:

Audits Makefiles for build correctness, portability, and recipe duplication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when reviewing Makefile changes, improving build automation, checking portability, identifying duplicated recipes, and deciding whether build-system changes are ready to approve.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Make-related inspection or testing commands may execute project-defined Makefile logic in the reviewed repository.

Mitigation: For untrusted repositories, avoid make -pn, make -n, and target testing unless explicitly approved in a sandbox with secrets removed.

Risk: Generated Makefile changes or --apply workflows may alter build behavior without enough containment.

Mitigation: Only allow apply-style generation after explicit approval, then review the resulting clean diff before accepting changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-makefile-review)
- [ClawHub publisher profile](https://clawhub.ai/user/athola)
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown review report with command snippets, findings, recommendations, and optional generated Makefile target templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity labels, file and target context, dependency analysis, duplication candidates, portability findings, missing-target checklists, and approve/block recommendations.]

## Skill Version(s):

1.9.19 (source: ClawHub release metadata; artifact frontmatter reports 1.9.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
