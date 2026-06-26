## Description: <br>
Enables an agent to self-reflect, log corrections and preferences, and maintain local self-improvement memory so repeated mistakes and useful workflows can influence future work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quenlenliu](https://clawhub.ai/user/quenlenliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to help an assistant retain explicit corrections, preferences, workflow lessons, and self-reflection notes in local files for future tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can steer future agent behavior and retain sensitive or stale information. <br>
Mitigation: Install only when persistent memory is intended, keep memory files visible to the user, and avoid storing secrets, sensitive personal data, proprietary details, or third-party information. <br>
Risk: Broad automatic learning triggers can record incorrect or over-generalized preferences. <br>
Mitigation: Treat new lessons as tentative, require confirmation for recurring patterns, preserve source tracking, and support export and full deletion on request. <br>
Risk: Setup may modify workspace steering files such as AGENTS.md, SOUL.md, or HEARTBEAT.md. <br>
Mitigation: Review proposed workspace edits before applying them and confirm how automatic logging can be disabled or removed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/quenlenliu/my-self-improving) <br>
- [Publisher profile](https://clawhub.ai/user/quenlenliu) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>
- [Security boundaries](artifact/boundaries.md) <br>
- [Setup guide](artifact/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files under ~/self-improving/ and optional workspace steering files when installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
