## Description: <br>
Routes OneScience AI4S requests to coding, runtime, debugging, and installation skills for model, data, training, inference, and research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onescience-ai](https://clawhub.ai/user/onescience-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to route OneScience work across code planning, model and data pipeline implementation, SLURM runtime submission, debugging, and DCU environment installation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read SSH configuration and run commands against remote DCU hosts. <br>
Mitigation: Require explicit approval before reading ~/.ssh/config, selecting an SSH host, or executing any remote command. <br>
Risk: The skill can submit SLURM or SCnet jobs and upload generated files. <br>
Mitigation: Review every generated file and require final confirmation before upload, job submission, or file overwrite. <br>
Risk: Installer guidance includes removing an existing onescience directory. <br>
Mitigation: Avoid that command by default, or require manual approval and a backup decision before any deletion. <br>
Risk: Generated code, tests, and runtime plans may be incorrect or unsafe for a target environment. <br>
Mitigation: Review and scan generated outputs before deployment, and treat test results as valid only when backed by execution evidence. <br>


## Reference(s): <br>
- [OneScience Repository](https://gitee.com/onescience-ai/onescience.git) <br>
- [OneScience Coder Workflow](artifact/onescience-coder/references/workflow.md) <br>
- [OneScience Model Index](artifact/onescience-coder/assets/models/model_index.md) <br>
- [OneScience DataPipe Index](artifact/onescience-coder/assets/datapipes/datapipe_index.md) <br>
- [OneScience Component Index](artifact/onescience-coder/assets/contracts/component_index.md) <br>
- [End-to-End Pipeline Test Guide](artifact/onescience-debug/references/e2e_pipeline_test.md) <br>
- [Earth DataPipe Test Guide](artifact/onescience-debug/references/earth_datapipe_test.md) <br>
- [Model Test Guide](artifact/onescience-debug/references/model_test.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with structured pipeline plans, code or configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SLURM job submission guidance and remote installation steps when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
