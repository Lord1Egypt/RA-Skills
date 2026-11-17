## Description:

Linkfox Skill Creator guides cross-border e-commerce experts through a structured interview to turn operating, sourcing, advertising, logistics, compliance, and related business knowledge into agent-executable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lienong1122334](https://clawhub.ai/user/lienong1122334)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and cross-border e-commerce operators use this skill to create, review, and iterate practical agent skills from expert business workflows without requiring the expert to write technical instructions. It supports structured interviews, skill file generation, delegated Linkfox tool discovery, and quality evaluation handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated helper scripts can execute local Python scripts by path.

Mitigation: Review generated scripts, target script paths, and output locations before execution, especially when a workflow calls a Linkfox tool-type skill.

Risk: The skill can create persistent local skill files, generated Python scripts, data files, and evaluator reports.

Mitigation: Run it in a workspace where generated files can be inspected before use, and verify generated outputs before publishing or deployment.

Risk: The artifact includes a fallback path that may install an onboarding skill from a remote release archive.

Mitigation: Install only from the expected Linkfox source after user authorization, and verify the downloaded skill before using it.

Risk: Generated workflows may interact with sensitive environment variables or authenticated Linkfox tools.

Mitigation: Avoid running generated workflows with unnecessary sensitive environment variables, and confirm credential requirements before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lienong1122334/skills/linkfox-skill-creator)
- [Workflow overview](references/00-workflow-overview.md)
- [Stage 3 generation rules](references/04-stage-3-generate.md)
- [Delegate discovery rules](references/06-delegate-discovery.md)
- [Interview record schema](references/interview-record-schema.md)
- [Evaluator sub-agent protocol](references/evaluator/08-sub-agent-protocol.md)
- [Linkfox onboarding release archive](https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip)
- [Linkfox API key guide](https://skill.linkfox.com/linkfoxskills/guide.htm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, generated skill files, Python helper scripts, shell command examples, and structured evaluation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent local skill directories, reference files, Python scripts, data files, and evaluator reports.]

## Skill Version(s):

1.0.0 (source: release evidence, created 2026-08-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
