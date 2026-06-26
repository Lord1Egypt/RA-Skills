## Description: <br>
Convert AI chat links, pasted conversations, and rough AI drafts into structured, reviewed learning notes and a separate cheat sheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyharry](https://clawhub.ai/user/hyharry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, researchers, and developers use this skill to turn transient AI chat material into durable study notes with definitions, key ideas, worked examples, derivations, Q&A, further reading, and a distilled cheat sheet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI chat material may contain sensitive or private information that would be processed by a subagent and saved into local notes. <br>
Mitigation: Use only source material you are comfortable processing this way, or explicitly request inline output, no subagent, or a different save location. <br>
Risk: Source links are preserved in the main note when present, which may retain traceable references to shared chats or private locations. <br>
Mitigation: Review generated notes before sharing and remove or redact links that should not be distributed. <br>
Risk: Generated notes may overwrite or conflict with existing durable notes if file naming is not reviewed. <br>
Mitigation: Follow the skill's pre-search step for notes/ and create a new subject-specific filename unless the user explicitly requests revision of an existing note. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hyharry/learned-from-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown files saved as a main note and separate cheat sheet] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [By default the skill saves outputs under notes/, preserves the original source link when present, and uses a subagent unless the user asks otherwise.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
