## Description: <br>
效率倍增器 helps agents create and maintain a lightweight personal productivity system with energy-aware planning, overload triage, contextual guidance, and recurring reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and productivity-focused agents use this skill to turn goals, tasks, commitments, habits, and energy patterns into a maintainable local planning system. It is useful when users feel overloaded, need a weekly plan or review, or need context-specific productivity guidance for situations such as burnout, ADHD, remote work, management, studying, or freelancing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requests shell execution even though the artifact describes a Markdown-only workflow that does not need exec. <br>
Mitigation: Remove the exec permission or document narrow command rules before routine use. <br>
Risk: The skill may create and reorganize local files under ~/productivity/. <br>
Mitigation: Review proposed file changes and store only user-approved productivity notes or preferences. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/productivity-boost) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files, Configuration] <br>
**Output Format:** [Markdown guidance and local Markdown productivity files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, read, and reorganize files under ~/productivity/ when the user approves local storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
