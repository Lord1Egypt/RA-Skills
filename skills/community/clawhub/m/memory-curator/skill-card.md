## Description: <br>
Distill verbose daily logs into compact, indexed digests for managing agent memory files, compressing logs, summarizing past activity, and building index-first memory architectures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[77Darius77](https://clawhub.ai/user/77Darius77) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to turn large daily memory logs into compact digests that preserve summaries, stats, key events, learnings, connections, open questions, and next priorities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Clawdbot memory logs that may contain names, activity details, and other sensitive context. <br>
Mitigation: Run it only on intended memory files and review generated digests before committing or sharing them. <br>
Risk: The suggested scheduled workflow can create digest skeletons without a fresh manual command each day. <br>
Mitigation: Enable scheduling deliberately and keep the manual fill-in and review step before relying on generated digests. <br>


## Reference(s): <br>
- [Memory Curator on ClawHub](https://clawhub.ai/77Darius77/memory-curator) <br>
- [Milo profile](https://moltbook.com/user/milo) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest skeletons with shell command examples and concise setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates dated digest files under $HOME/clawd/memory/digests and leaves comment prompts for manual completion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
