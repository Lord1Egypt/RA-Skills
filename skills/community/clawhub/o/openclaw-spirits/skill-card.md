## Description: <br>
Companion spirit system for OpenClaw agents that deterministically generates a unique virtual companion from a user identity seed and supports spirit display, stats, conversation, and bilingual card output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahaaiclub](https://clawhub.ai/user/ahaaiclub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to add a lightweight companion presence to OpenClaw-style agents. It produces deterministic spirit profiles, formatted spirit cards, stats, and brief in-character companion responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill generates a companion from a stable user identifier or username and saves companion data locally in the skill directory. <br>
Mitigation: Use the least sensitive stable identifier available, avoid secrets or private identifiers as seeds, and review or remove assets/companion.json when local storage is not desired. <br>
Risk: Passive companion messages may distract users or appear when companion behavior is not wanted. <br>
Mitigation: Configure the agent to respond only to explicit commands such as `spirit`, `spirit show`, or `spirit talk` when unsolicited companion messages would be distracting. <br>


## Reference(s): <br>
- [OpenClaw Spirits skill page](https://clawhub.ai/ahaaiclub/openclaw-spirits) <br>
- [OpenClaw Spirits product spec](artifact/openclaw-spirits/SPEC.md) <br>
- [OpenClaw Spirits species guide](artifact/openclaw-spirits/references/species-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with ASCII sprites, command guidance, and JSON companion data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save companion data locally in assets/companion.json; deterministic output is seeded by a user identity or username.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
