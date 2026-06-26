## Description: <br>
Coding workflow with planning, implementation, verification, and testing for clean software development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpzhengcn](https://clawhub.ai/user/jpzhengcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to plan, implement, verify, and deliver software changes while keeping user control over execution and preference storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact version and release metadata do not match, which can make package identity harder to confirm. <br>
Mitigation: Confirm the installed package identity and intended release version before using the skill in a shared or production workflow. <br>
Risk: Saved preferences in ~/code/memory.md may influence future coding sessions. <br>
Mitigation: Save only non-sensitive preferences that the user explicitly asks to remember. <br>
Risk: Coding guidance or proposed changes can be incorrect or insufficiently tested. <br>
Mitigation: Review proposed changes and run the relevant tests, scans, or UI checks before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpzhengcn/openclaw-code) <br>
- [Skill homepage](https://clawic.com/skills/code) <br>
- [Planning reference](planning.md) <br>
- [Execution guidance](execution.md) <br>
- [Verification reference](verification.md) <br>
- [Preference storage criteria](criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file changes, tests, screenshots, and user-approved preference updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
