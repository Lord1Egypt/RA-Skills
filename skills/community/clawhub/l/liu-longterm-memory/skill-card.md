## Description: <br>
Provides AI agents with persistent long-term memory using session files, curated Markdown archives, optional vector search, Git notes, and backup or restore commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louiseliu](https://clawhub.ai/user/louiseliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to initialize and maintain persistent agent memory, recall prior context, and back up or restore memory across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad long-term memory can store sensitive conversation details beyond the current session. <br>
Mitigation: Install only when persistent agent memory is intended, review stored memory files regularly, and avoid capturing confidential work without consent. <br>
Risk: Optional remote LLM, embedding, Git backup, or restore flows may expose memory-derived content to external providers or repositories. <br>
Mitigation: Prefer local-only options for confidential work, avoid remote providers unless approved, and inspect memory files before backup or restore. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/louiseliu/liu-longterm-memory) <br>
- [README](artifact/README.md) <br>
- [Chinese README](artifact/README_CN.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create or update local memory Markdown files and backup archives.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact files report 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
