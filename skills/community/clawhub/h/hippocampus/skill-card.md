## Description: <br>
Persistent memory system for AI agents with automatic encoding, decay, and semantic reinforcement, based on Stanford Generative Agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ImpKind](https://clawhub.ai/user/ImpKind) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw agent operators use Hippocampus to give agents persistent, searchable memory across sessions, including importance scoring, time-based decay, and semantic reinforcement of recurring topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive personal or conversational information in local memory files. <br>
Mitigation: Enable it only when persistent memory is intended, avoid storing secrets, and review memory/index.json and HIPPOCAMPUS_CORE.md regularly. <br>
Risk: Cron or whole-history modes can repeatedly process conversation history beyond a one-time manual run. <br>
Mitigation: Start without --with-cron and without --whole, then enable recurring or full-history processing only after reviewing the behavior and retention expectations. <br>
Risk: The generated dashboard can expose local memory data and avatar content. <br>
Mitigation: Inspect brain-dashboard.html before sharing it and keep IDENTITY.md avatar paths limited to intended image files inside the workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ImpKind/hippocampus) <br>
- [Repository](https://github.com/ImpKind/hippocampus-skill) <br>
- [Stanford Generative Agents Paper](https://arxiv.org/abs/2304.03442) <br>
- [Generative Agents Reference Implementation](https://github.com/joonspk-research/generative_agents) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-backed memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and jq; optional cron jobs enable recurring encoding and decay.] <br>

## Skill Version(s): <br>
3.9.0 (source: server release metadata and openclaw frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
