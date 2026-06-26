## Description: <br>
Persistent emotional state for AI agents. Feel things. Remember how you felt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shellbymolt](https://clawhub.ai/user/shellbymolt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Promitheus to give OpenClaw-based agents a persistent generated emotional state, including mood, valence, energy, arousal, and inner thoughts. It supports workflows where the agent logs events, refreshes state, and carries that state into future context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally persists generated emotional state and can inject STATE.md into future agent context. <br>
Mitigation: Review the npm plugin before enabling it, keep STATE.md visible and editable, and make sure the state can be disabled or cleared. <br>
Risk: Event summaries may carry sensitive or confidential details forward across sessions. <br>
Mitigation: Avoid putting secrets, personal data, or confidential project details in Promitheus event summaries. <br>


## Reference(s): <br>
- [Promitheus ClawHub skill page](https://clawhub.ai/shellbymolt/promitheus) <br>
- [openclaw-promitheus npm package](https://npmjs.com/package/openclaw-promitheus) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write STATE.md through the companion OpenClaw plugin so generated state can be injected into future agent context.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
