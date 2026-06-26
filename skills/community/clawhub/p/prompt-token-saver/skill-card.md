## Description: <br>
Saves 20-40% of LLM tokens by teaching the agent to write compressed responses, compressed memory logs, and compressed pre-compaction summaries, and provides manual prompt compression guidance when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckpxgfnksd-max](https://clawhub.ai/user/ckpxgfnksd-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to reduce LLM token usage and API cost by adding concise-response, memory-log, and compaction-summary instructions to OpenClaw. It can also guide one-off prompt compression while preserving exact code, URLs, paths, numbers, and quoted requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional hook can silently rewrite user messages before the model sees them. <br>
Mitigation: Avoid enabling the hook for legal, medical, security, debugging, policy, or exact-wording tasks. <br>
Risk: Installing the SOUL.md snippet changes persistent response, memory, log, and compaction behavior. <br>
Mitigation: Install it only when persistent concise behavior is desired, append rather than overwrite, and back up SOUL.md first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckpxgfnksd-max/prompt-token-saver) <br>
- [Project homepage from ClawHub metadata](https://github.com/ckpxgfnksd-max/prompt-compressor-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and compression rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent SOUL.md guidance and optional hook-install guidance; users should review behavior before enabling prompt rewriting.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
