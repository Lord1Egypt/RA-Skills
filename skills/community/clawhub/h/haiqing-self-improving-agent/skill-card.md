## Description: <br>
AI Self-Improving Agent v2 helps agents learn from mistakes, corrections, and successful tasks through passive memory capture, proactive memory checks, and reusable skill generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haiqingge](https://clawhub.ai/user/haiqingge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to persist local lessons from command errors, user corrections, and best practices, then check those memories before similar future work. It can also generate draft reusable Skills after complex successful tasks or repeated patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores long-lived local agent memory that may capture secrets, proprietary context, or stale preferences. <br>
Mitigation: Avoid storing sensitive data and regularly review, clean, or delete records under ~/.openclaw/memory/self-improving. <br>
Risk: Generated skills may preserve incorrect patterns or unsafe assumptions if accepted without review. <br>
Mitigation: Human-review and scan generated Skills before use, and keep generated drafts separate from trusted skills until validated. <br>
Risk: Skill generation uses user-supplied names for generated skill paths with weak safeguards. <br>
Mitigation: Restrict generated skill names to safe slugs before using the generation workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haiqingge/haiqing-self-improving-agent) <br>
- [Publisher profile](https://clawhub.ai/user/haiqingge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown and plain text guidance with generated SKILL.md files, JSONL memory records, and JSON registry entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes long-lived local memory under ~/.openclaw/memory/self-improving and generated skill drafts under ~/.openclaw/skills-generated.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter, skill.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
