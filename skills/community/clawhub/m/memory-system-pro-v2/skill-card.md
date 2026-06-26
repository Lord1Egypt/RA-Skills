## Description: <br>
Memory System Pro V2 gives an agent persistent Markdown-based memory with user, feedback, project, and reference categories, semantic search, automatic loading, flushing, and AutoDream consolidation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minmengxhw-cpu](https://clawhub.ai/user/minmengxhw-cpu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external ClawHub users use this skill to let an agent save, retrieve, search, and consolidate local Markdown memory across sessions for personalization, feedback capture, and project context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores conversation-derived memory locally, which may include sensitive personal, project, or preference data if users save it. <br>
Mitigation: Use a dedicated non-sensitive memory directory, avoid saving secrets or sensitive personal data, and review memory contents regularly. <br>
Risk: AutoDream may send memory contents to MiniMax for analysis and consolidation. <br>
Mitigation: Disable AutoDream or heartbeat-triggered consolidation when external processing is not acceptable, and configure API keys only in approved environments. <br>
Risk: Automatic consolidation can edit or delete memory files, including removing information judged outdated or duplicate. <br>
Mitigation: Keep backups or require manual review before deletions and overwrites, especially for shared or project-critical memory stores. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minmengxhw-cpu/memory-system-pro-v2) <br>
- [README](README.md) <br>
- [Product documentation](PRODUCT.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance, files] <br>
**Output Format:** [Markdown memory files, JSON tool responses, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read, write, search, consolidate, and delete local memory files depending on tool use and AutoDream settings.] <br>

## Skill Version(s): <br>
2.0.1 (source: changelog and server release metadata, released 2026-03-31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
