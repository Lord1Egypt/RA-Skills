## Description: <br>
Provides a neuroscience-inspired persistent memory system for OpenClaw agents with multi-tier storage, semantic search, emotional tagging, value-based retention, and error learning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Broedkrummen](https://clawhub.ai/user/Broedkrummen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill to give agents persistent memory across sessions, including memory capture, search, diary entries, error tracking, self-reflection, and optional automated maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory may capture sensitive conversation, diary, habit, correction, and error data across sessions. <br>
Mitigation: Avoid storing secrets or confidential data, restrict permissions on ~/.openclaw memory files, and review retained memories regularly. <br>
Risk: Optional cron and transcript-analysis workflows can process conversation text without direct user attention once enabled. <br>
Mitigation: Enable automation only after reviewing the configured commands, schedule, input paths, and retention behavior. <br>
Risk: Optional cloud and external model integrations can send memory or conversation text to configured services. <br>
Mitigation: Use offline mode unless cloud sync or external model analysis is required, and verify API keys, service endpoints, and ACC_MODELS commands before use. <br>
Risk: Long-lived local memory files can accumulate stale or excessive personal context. <br>
Mitigation: Set a retention and purge process for daily notes, diary entries, caches, vector stores, and exported backups. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Broedkrummen/overkill-memory-system) <br>
- [Quick Start](README.md) <br>
- [Complete skill documentation](SKILL.md) <br>
- [Final Architecture](FINAL_ARCHITECTURE.md) <br>
- [File Search Integration](FILE_SEARCH_INTEGRATION.md) <br>
- [Knowledge Graph Integration](KG_INTEGRATION.md) <br>
- [Self-Reflection Framework](SELF_REFLECTION_FRAMEWORK.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands, shell commands, JSON state files, and local memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local memory artifacts under user-controlled OpenClaw memory directories and can optionally use local or cloud services when configured.] <br>

## Skill Version(s): <br>
1.9.5 (source: server release evidence; artifact documentation also references 1.9.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
