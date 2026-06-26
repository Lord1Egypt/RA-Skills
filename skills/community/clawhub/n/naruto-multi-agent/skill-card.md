## Description: <br>
Naruto-themed multi-agent dispatcher that has an agent play Tsunade, assess mission rank, and dispatch work to five persistent named sub-agents by round-robin scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Be1Human](https://clawhub.ai/user/Be1Human) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to route ordinary work requests into persistent named sub-agent sessions while keeping the primary persona focused on triage and dispatch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User requests and context may be copied into delegated sub-agent sessions. <br>
Mitigation: Avoid including secrets or sensitive production context unless sharing that context with delegated agents is acceptable. <br>
Risk: Delegated agents may perform account-changing or destructive work if the request is too broad. <br>
Mitigation: Give clear limits and review delegated results before allowing account-changing, destructive, or production-impacting actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Be1Human/naruto-multi-agent) <br>
- [Publisher profile](https://clawhub.ai/user/Be1Human) <br>
- [ClawHub homepage](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown text followed by delegated session spawn calls when work should be assigned.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses one of five fixed session keys and a 300 second delegated run timeout.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
