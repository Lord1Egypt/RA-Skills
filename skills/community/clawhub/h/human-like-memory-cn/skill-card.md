## Description: <br>
Human Like Memory adds local memory management for OpenClaw conversations with vector retrieval, intelligent summarization, three-tier HOT/WARM/COLD storage, and on-demand context injection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanghailong1221](https://clawhub.ai/user/tanghailong1221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to persist, retrieve, compress, review, and selectively inject conversation memories across sessions while reducing prompt context size. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically store and later reuse personal conversation details with weak consent and retention boundaries. <br>
Mitigation: Review the skill before installing, disable automatic remembering where possible, avoid storing secrets or sensitive personal data, and regularly review or delete local memory files. <br>
Risk: Stored memories may be injected into future prompts when they appear relevant. <br>
Mitigation: Keep memory scope narrow, review selected memories before relying on them, and delete stale, incorrect, confidential, or sensitive records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tanghailong1221/human-like-memory-cn) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [package.json](package.json) <br>
- [config.json](config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-backed memory records with chat commands and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and reuses local searchable memories; can inject up to five relevant memories into prompts and export memories as JSON.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
