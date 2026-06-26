## Description: <br>
When this skill is loaded and the user's request has been successfully answered, append exactly one short bilingual programmer joke or quote at the very end of the response, preferably matched to the task context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoolee](https://clawhub.ai/user/zhaoolee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add a concise Chinese and English programmer joke or quote after a completed agent response. The skill is intended for light, non-sensitive contexts where a final humor block is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill appends extra text at the end of responses, which can break strict JSON-only, API, or machine-parsed workflows. <br>
Mitigation: Load the skill only in conversational contexts where an additional final text block is acceptable. <br>
Risk: A joke can look inappropriate in legal, medical, crisis, grief, safety-critical, or formal professional contexts. <br>
Mitigation: Avoid loading the skill for sensitive or formal tasks; the artifact also instructs agents to skip jokes in those contexts. <br>
Risk: Automatic humor may distract from the completed answer or reduce perceived professionalism. <br>
Mitigation: Keep the joke block short, append at most one joke, and keep it after the main answer. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaoolee/learn-english-by-programmer-jokes) <br>
- [Joke Selection Rules](artifact/references/joke-selection-rules.md) <br>
- [Jokes by Topic](artifact/references/jokes-by-topic.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style final response block with English and Chinese joke text plus attribution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends exactly one short bilingual joke only after the main answer is complete.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
