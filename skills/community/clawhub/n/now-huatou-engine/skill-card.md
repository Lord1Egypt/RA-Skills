## Description: <br>
Generates Zen-style huatou prompts from scene-based templates, with documented future support for LLM-generated self-inquiry prompts from user context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[perrykono-debug](https://clawhub.ai/user/perrykono-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents use this skill to produce short Zen-style prompts for mindfulness or self-inquiry based on scenes such as anxiety, overthinking, decisions, emotion, or free reflection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive emotional or crisis-related user input may be routed to an external model service in the dynamic flow without clear privacy controls. <br>
Mitigation: Avoid personal identifiers, private health details, and crisis details unless clear disclosure, opt-in, and data-minimization guidance are added. <br>
Risk: Generated self-inquiry prompts may be inappropriate when a user expresses self-harm or severe psychological crisis. <br>
Mitigation: Do not generate huatou prompts for self-harm or severe-crisis language; route those cases to help information as described in the skill. <br>


## Reference(s): <br>
- [Source skill instructions](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/perrykono-debug/now-huatou-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Plain text prompts or JSON for dynamic generation output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MVP output is selected from static scene-tagged templates with emotion and time-word variable filling; the dynamic flow targets one short huatou.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
