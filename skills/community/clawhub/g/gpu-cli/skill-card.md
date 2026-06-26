## Description: <br>
Safely run local `gpu` commands via a guarded wrapper (`runner.sh`) with preflight checks and budget/time caps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angusbezzina](https://clawhub.ai/user/angusbezzina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to let an agent inspect, preview, and run remote GPU CLI workflows for ML training, inference, notebooks, ComfyUI, and LLM serving with wrapper guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent authority to run local gpu CLI commands that can affect accounts, paid compute, and existing GPU jobs. <br>
Mitigation: Review the exact proposed command before execution and keep dry-run, confirmation, price cap, and runtime cap settings enabled unless intentionally changed. <br>
Risk: Ambiguous requests may trigger state-changing GPU resource operations. <br>
Mitigation: Use explicit subcommands and flags, prefer JSON status or inventory checks before run or stop actions, and avoid broad account or resource-management prompts. <br>
Risk: Interrupted runs may issue a broad stop command that could affect other GPU jobs. <br>
Mitigation: Check active jobs before cancellation or stop operations and confirm that the target job is the intended one. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/angusbezzina/gpu-cli) <br>
- [GPU CLI Documentation for Agent Skill](https://gpu-cli.sh/docs/ai-agent-skill) <br>
- [GPU CLI Project Repository](https://github.com/gpu-cli/gpu) <br>
- [GPU CLI Homepage](https://gpu-cli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-capable command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May stream status, logs, inventory, or execution results from the local gpu CLI through the guarded runner.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
