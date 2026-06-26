## Description: <br>
Long Text Tracker helps agents create coherent multi-part long-form content by tracking outlines, segment drafts, summaries, continuity checks, checkpoints, and recovery steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sjj2026](https://clawhub.ai/user/sjj2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, writing teams, and agent users use this skill to plan and draft series content such as tweet threads, tutorials, reports, and serialized writing while preserving continuity across at least three segments and 3000 or more expected words. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves drafts, settings, progress, and summaries as local project files, which can retain sensitive or unpublished material. <br>
Mitigation: Use a dedicated project folder, avoid sensitive material unless needed, and review or remove generated project files when the work is complete. <br>
Risk: The completion workflow includes optional email delivery of generated content. <br>
Mitigation: Confirm the recipient and exact content before allowing any email delivery. <br>
Risk: Continuity summaries and status files can become inaccurate if earlier segments are changed without updating dependent summaries. <br>
Mitigation: Review saved summaries before resuming and use the skill's feedback-adjustment and cascade-update steps when segment changes affect later content. <br>


## Reference(s): <br>
- [Expansion Techniques](references/expansion-techniques.md) <br>
- [Summary Template](references/summary-template.md) <br>
- [ClawHub Release Page](https://clawhub.ai/sjj2026/long-text-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown drafts, progress files, summaries, checkpoint/status messages, and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local project files under projects/{project_name}/ and may use /tmp/long-text-tracker/ as a fallback; optional email delivery should only occur after explicit confirmation.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
