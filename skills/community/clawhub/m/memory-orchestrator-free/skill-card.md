## Description: <br>
Provides basic two-layer short-term and long-term memory management for agents, with keyword search, simple summaries, and local persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to store, retrieve, summarize, save, and load basic memory entries for simple agent memory workflows such as current-session context and user preference records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory contents are stored in local files and may contain sensitive personal data if users save it. <br>
Mitigation: Avoid saving secrets, credentials, or highly sensitive personal data, and choose a private storage path. <br>
Risk: Callback URLs can send completion details to an external destination. <br>
Mitigation: Use callback URLs only when the destination is trusted and expected for the workflow. <br>
Risk: The free version does not provide concurrent write conflict handling, so multiple agents writing at once may overwrite memory data. <br>
Mitigation: Use single-writer workflows or coordinate writes externally when multiple agents share the same memory file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/memory-orchestrator-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples and JSON result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local memory store files at the configured persistPath.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; SKILL.md frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
