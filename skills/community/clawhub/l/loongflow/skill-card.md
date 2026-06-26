## Description: <br>
LoongFlow guides an agent through PEES iterative optimization, using either a native async subagent loop or a LoongFlow Engine background evolutionary search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freshmand](https://clawhub.ai/user/freshmand) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when a coding, algorithm, prompt, or optimization task needs structured iteration rather than a single pass. It helps choose between a short native PEES loop and a longer background evolutionary search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run iterative jobs in the background and modify workspace files. <br>
Mitigation: Use a dedicated workspace or branch and review resulting file changes before merging or deploying them. <br>
Risk: Engine mode may install code from a moving GitHub branch. <br>
Mitigation: Review the downloaded source and pin or record the revision before using it for sensitive work. <br>
Risk: Monitoring can read LoongFlow task logs across configured workspaces and send progress summaries to a detected user. <br>
Mitigation: Review created cron jobs, task registries, and notification routing before starting tasks. <br>
Risk: Engine mode relies on API key and base URL environment variables. <br>
Mitigation: Avoid exposing API keys in task files or logs and use scoped credentials where available. <br>


## Reference(s): <br>
- [LoongFlow ClawHub page](https://clawhub.ai/freshmand/loongflow) <br>
- [Publisher profile](https://clawhub.ai/user/freshmand) <br>
- [LoongFlow repository](https://github.com/baidu-baige/LoongFlow) <br>
- [Native PEES Mode](references/native-pees.md) <br>
- [LoongFlow Engine Mode](references/engine-mode.md) <br>
- [LoongFlow Monitoring Cron](references/monitoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell and configuration snippets, plus workspace task files and progress summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create task registries, iteration artifacts, background jobs, logs, and final result summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
