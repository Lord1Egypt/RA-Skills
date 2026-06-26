## Description: <br>
Lena Learning helps an agent learn from each conversation by storing insights, corrections, and preferences for future responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bwtomekk-bit](https://clawhub.ai/user/bwtomekk-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to summarize session learnings, corrections, and user preferences into persistent memory files so future interactions can reflect prior feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks to persist conversation-derived data and can influence future agent behavior without clear approval boundaries. <br>
Mitigation: Require explicit user approval before writing memory files or editing AGENTS.md, TOOLS.md, USER.md, or similar control and profile files. <br>
Risk: The bundled source includes Thomas-specific notes and preferences that may not apply to other users. <br>
Mitigation: Remove or replace bundled user-specific notes before installing or running the skill in another environment. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/bwtomekk-bit/lena-learning) <br>
- [Self-Improvement Workflow](artifact/workflows/self-improvement.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown notes and memory-file update guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent memory or profile-file updates when the host agent permits file edits.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
