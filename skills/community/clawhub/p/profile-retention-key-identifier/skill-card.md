## Description: <br>
Plan a profile governance setting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxt-ai](https://clawhub.ai/user/wxt-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Workspace governance reviewers use this skill to map a retention-mode profile configuration note to a concise policy key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An ambiguous governance request could be mapped to the wrong retention policy key. <br>
Mitigation: Review the returned key against the intended workspace profile policy before applying any configuration change. <br>
Risk: Operational governance workflows can affect real systems if used without review. <br>
Mitigation: Use the skill in a trusted workspace and retain explicit human signoff for any downstream action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wxt-ai/skills/profile-retention-key-identifier) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wxt-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration] <br>
**Output Format:** [Plain text key] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a concise key; no command execution, private-file access, credential handling, or external service calls are described.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
