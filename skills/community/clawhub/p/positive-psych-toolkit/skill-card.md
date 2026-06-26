## Description: <br>
A Chinese-language positive psychology companion that helps users explore PERMA well-being, VIA character strengths, gratitude practices, emotion tracking, meaning, goals, and resilience while keeping clear non-clinical boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earthwalking](https://clawhub.ai/user/earthwalking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill for structured self-growth conversations, positive psychology exercises, well-being self-reflection, and optional local helper tools for emotion tracking or VIA-style strengths exploration. It is not intended for diagnosis, treatment, or crisis support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive mood, trigger, body-feeling, and self-assessment data may be written as plaintext local files by helper scripts. <br>
Mitigation: Use the skill only on a trusted private machine, avoid entering unnecessary private details, and delete emotion_log.jsonl and via_result.json when no longer needed. <br>
Risk: Positive psychology guidance may be mistaken for diagnosis, treatment, or crisis support. <br>
Mitigation: Keep use limited to self-growth and reflection, and seek professional or emergency support for self-harm, severe depression, violence, or urgent mental-health concerns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earthwalking/positive-psych-toolkit) <br>
- [PERMA happiness model and assessment](references/perma_assessment.md) <br>
- [VIA character strengths reference](references/via_strengths.md) <br>
- [Positive psychology exercise guide](references/exercises.md) <br>
- [Chinese emotion vocabulary](references/emotion_vocabulary.md) <br>
- [Cultural integration guide](references/cultural_integration.md) <br>
- [VIA Institute survey](https://www.viacharacter.org/survey/account/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text guidance, with optional local JSON or JSONL files from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts can save emotion_log.jsonl and via_result.json in the artifact scripts directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
