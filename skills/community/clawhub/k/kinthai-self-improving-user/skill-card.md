## Description: <br>
Provides OpenClaw agents with per-user memory instructions and hooks for storing corrections, preferences, errors, profiles, and follow-ups in isolated .learnings directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kinthaiofficial](https://clawhub.ai/user/kinthaiofficial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent operators use this skill to let a multi-user agent remember user-specific corrections, preferences, recurring errors, and follow-ups without mixing one user's learnings with another user's context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists and reloads per-user profiles, follow-ups, and learned facts in ways users may not expect. <br>
Mitigation: Disclose the memory behavior before use, add opt-in or opt-out controls, and provide inspect and delete controls for stored user memory. <br>
Risk: The skill's instructions make the memory system silent and can reload stored .learnings content into future prompts. <br>
Mitigation: Remove or change silent and never-mention rules, constrain what may be stored, and review stored .learnings content before it is reloaded. <br>
Risk: User IDs are used to choose per-user memory directories. <br>
Mitigation: Validate user IDs before path use and keep the per-user directory boundary enforced so one user's files are not read for another user. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/kinthaiofficial/kinthai-self-improving-user) <br>
- [KinthAI](https://kinthai.ai) <br>
- [Hindsight memory integration](https://hindsight.vectorize.io/) <br>
- [Self-Improving Agent inspiration](https://clawhub.ai/pskoett/self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with command snippets and OpenClaw hook configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update persistent .learnings files containing per-user profiles, follow-ups, errors, and learned preferences.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
