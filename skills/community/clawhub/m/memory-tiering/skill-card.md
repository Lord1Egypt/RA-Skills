## Description: <br>
Automated multi-tiered memory management (HOT, WARM, COLD). Use this skill to organize, prune, and archive context during memory operations or compactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SarielWang93](https://clawhub.ai/user/SarielWang93) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to organize memory into hot, warm, and cold tiers, prune completed context, and archive durable summaries during manual memory maintenance or post-compaction cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can summarize and prune remembered context, which may remove details that are still useful. <br>
Mitigation: Preview or back up memory changes before pruning and verify that critical information remains available after tier redistribution. <br>
Risk: Memory files may contain sensitive values or temporary credentials. <br>
Mitigation: Avoid storing raw secrets in memory files and keep references to root secret locations instead. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/SarielWang93/memory-tiering) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance for memory file organization and summarization] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or perform edits to HOT, WARM, COLD, and daily memory markdown files when the hosting agent has file access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
