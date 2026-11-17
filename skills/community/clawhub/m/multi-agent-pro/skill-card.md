## Description:

Orchestrates multi-agent tasks as DAG pipelines with shared state, recovery, human approvals, and execution reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users define and run multi-agent workflows, track execution, recover from failures, and review results before approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pipeline state, reports, and snapshots can retain sensitive node outputs on disk.

Mitigation: Avoid storing secrets or personal data in node outputs; review local files before sharing.

Risk: Dashboard access or generated files can expose sensitive or untrusted pipeline data.

Mitigation: Keep the dashboard on localhost and review dashboard files generated from untrusted output.

Risk: Workflow templates can move, rename, delete, publish, or approve data.

Mitigation: Require explicit confirmation before running templates that change or release data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/fyniujin/skills/multi-agent-pro)
- [DAG scheduling guide](references/dag-scheduling-guide.md)
- [State-sharing protocol](references/state-sharing-protocol.md)
- [Error recovery patterns](references/error-recovery-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Markdown reports]

**Output Format:** [Text and Markdown guidance, JSON pipelines, Markdown reports, and HTML visualizations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pipeline state, snapshots, and reports can be written to local disk.]

## Skill Version(s):

5.5.0 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
