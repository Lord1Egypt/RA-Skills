## Description: <br>
Multi-Agent CN is a Chinese-language dispatcher skill that has the primary agent coordinate tasks across five persistent sub-agent sessions with round-robin assignment, task splitting, and result reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Be1Human](https://clawhub.ai/user/Be1Human) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to operate a Chinese-language task coordinator that delegates independent work to named sub-agents and summarizes returned results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task details may be copied into reusable sub-agent sessions without clear reset, retention, or sensitive-task controls. <br>
Mitigation: Avoid sending secrets, account data, production credentials, or unrelated private context through this dispatcher unless additional confirmation, project separation, and session reset rules are added. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Be1Human/multi-agent-cn) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/Be1Human) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, API calls] <br>
**Output Format:** [Markdown text with structured delegation instructions and sub-agent dispatch calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses fixed session keys for five reusable sub-agent sessions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill.json; SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
