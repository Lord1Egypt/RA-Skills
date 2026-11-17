## Description:

OneScience-Skills routes AI-for-science development requests into structured workflows for OneScience coding, debugging, SLURM runtime submission, and DCU installation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onescience-ai](https://clawhub.ai/user/onescience-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill package to plan and implement OneScience model, dataset, component, training, inference, debugging, and platform setup workflows. It can produce structured implementation plans, code-oriented guidance, runtime configuration, SLURM command guidance, and test-routing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can request SSH configuration access and remote execution on a DCU host.

Mitigation: Use a dedicated workspace, select the DCU host explicitly, and redact or limit SSH configuration details before sharing output.

Risk: The installation flow can run broad setup commands and destructive directory removal on a remote host.

Mitigation: Review the target host, command list, repository commit or branch, and affected remote paths before allowing installation commands to run.

Risk: Runtime and debugging workflows can generate or submit shell commands and SLURM jobs.

Mitigation: Inspect generated scripts, resource settings, environment variables, and file paths before submission.

## Reference(s):

- [OneScience repository](https://gitee.com/onescience-ai/onescience.git)
- [Workflow guide](artifact/onescience-coder/references/workflow.md)
- [First-round implementation guide](artifact/onescience-coder/references/first_round_guide.md)
- [Second-round implementation guide](artifact/onescience-coder/references/second_round_guide.md)
- [Model test guide](artifact/onescience-debug/references/model_test.md)
- [Earth DataPipe test guide](artifact/onescience-debug/references/earth_datapipe_test.md)
- [End-to-end pipeline test guide](artifact/onescience-debug/references/e2e_pipeline_test.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks, structured workflow summaries, configuration snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated code plans, SLURM-oriented runtime guidance, DCU installation commands, and debug reports.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
