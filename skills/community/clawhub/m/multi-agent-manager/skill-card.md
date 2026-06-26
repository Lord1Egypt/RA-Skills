## Description: <br>
Monitor, visualize, and coordinate multiple OpenClaw agents with status views, task tracking, and JSON output for debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[victory2694](https://clawhub.ai/user/victory2694) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams running multiple OpenClaw agents use this skill to inspect agent state, monitor activity, coordinate messages, and trace task flow while debugging or managing agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring and JSON output can expose workspace paths, agent IDs, model names, session counts, and recent activity. <br>
Mitigation: Run the skill only in terminals, logs, and shared environments where that local agent metadata is acceptable to display. <br>
Risk: The communication helper can send user-provided messages to configured agents. <br>
Mitigation: Review the target agent and message before using the helper, and use it deliberately for intended coordination tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/victory2694/multi-agent-manager) <br>
- [README.md](artifact/README.md) <br>
- [Reference README](artifact/references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Terminal text, JSON, and Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in watch mode and may display workspace paths, agent IDs, models, sessions, and message results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
