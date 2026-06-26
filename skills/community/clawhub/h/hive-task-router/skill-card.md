## Description: <br>
Intelligent task routing system that identifies task types (web/code/data/doc/chat) and routes to optimal models with appropriate execution mode (subagent/main session). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiongqiongcaocao](https://clawhub.ai/user/qiongqiongcaocao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to classify incoming work, select a configured model provider, and route code, web, data, documentation, chat, or batch tasks to an appropriate OpenClaw execution mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically delegate prompts to configured model providers or subagents, including sensitive, costly, or parallel work. <br>
Mitigation: Review routing decisions before execution and require confirmation for sensitive, high-cost, or parallel tasks. <br>
Risk: The router shell script sources a writable cache file as shell code. <br>
Mitigation: Keep the cache directory private and patch the router to parse cached values safely instead of sourcing the file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiongqiongcaocao/hive-task-router) <br>
- [Publisher profile](https://clawhub.ai/user/qiongqiongcaocao) <br>
- [Configuration guide](artifact/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and model-routing recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes tasks by keyword-detected type and may recommend subagent or main-session execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
