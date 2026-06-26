## Description: <br>
Context Manager helps an agent maintain a local personal context system for journals, imported information, personal judgments, bridge notes, distilled principles, and cognitive maps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through personal knowledge-management workflows: recording daily observations, adding judgments to external material, creating bridge notes, distilling a concise minimal kernel, and generating cognitive maps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store journals, imported messages, links, and distilled personal context in local files. <br>
Mitigation: Review what will be saved, avoid importing third-party or work conversations without permission, and keep sensitive context in an appropriately protected workspace. <br>
Risk: Entropy reduction can permanently delete saved notes when run with forceful deletion behavior. <br>
Mitigation: Run dry-run or report-only flows first, keep backups, and review every deletion candidate before using forceful deletion. <br>
Risk: Broad scans and summaries can mix personal judgments with external content and produce misleading or outdated context. <br>
Mitigation: Treat generated summaries and cognitive maps as drafts, verify important claims against source notes, and periodically prune or correct stale entries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lj22503/lj22503-context-manager) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Entropy Reduction Script](artifact/scripts/entropy_reduce.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown notes, reports, templates, command guidance, and local file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local Markdown files under data/ and may propose or perform deletions during entropy reduction.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
