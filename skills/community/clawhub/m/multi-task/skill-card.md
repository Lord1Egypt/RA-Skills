## Description: <br>
Orchestrates parallel execution of independent batch tasks by splitting work into work units and dispatching them to subagents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brightWeen](https://clawhub.ai/user/brightWeen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill when a user asks for several similar, independent tasks across files, pages, reports, or other batch inputs. It helps the agent analyze the work units, prepare isolated subagent prompts, dispatch parallel waves, monitor failures, and merge results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or unnecessary private context may be copied into multiple subagent prompts. <br>
Mitigation: Include only the minimum context each subagent needs, and avoid secrets or unrelated private data. <br>
Risk: A mistake in the task plan or prompt template can be amplified across many parallel outputs. <br>
Mitigation: Review the work-unit list, output directory, and batch size before dispatch; use a pilot run for large or sensitive batches. <br>
Risk: Parallel tasks can overwrite each other's files if output paths are not isolated. <br>
Mitigation: Use unique task IDs, unique output directories, and absolute paths for every work unit. <br>


## Reference(s): <br>
- [Advanced Patterns for Multi-Task Orchestration](artifact/references/advanced-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/brightWeen/multi-task) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with structured task plans, prompt templates, progress summaries, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs usually include per-task IDs, absolute input and output paths, wave sizing, retry notes, and final result summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
