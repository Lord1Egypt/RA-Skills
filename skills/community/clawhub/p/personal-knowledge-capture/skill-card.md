## Description: <br>
Knowledge Capture saves selected conversation highlights into structured Markdown notes, creates self-test questions, and maintains local mastery and review-plan files for spaced repetition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qy-zhang](https://clawhub.ai/user/qy-zhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn selected chat content into a persistent local knowledge base with notes, quiz questions, mastery tracking, and adaptive review scheduling. It also scores quiz answers and updates learning status based on review performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected conversation highlights may be retained in a persistent local knowledge base, including sensitive content if the user chooses to save it. <br>
Mitigation: Use the trigger phrases only for information suitable for retention, and periodically review or delete the local knowledge directory when it contains sensitive material. <br>
Risk: Generated notes, self-test questions, and scoring feedback may be incomplete or inaccurate if the source conversation is ambiguous. <br>
Mitigation: Review saved notes and generated questions before relying on them for study or decision-making. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qy-zhang/personal-knowledge-capture) <br>
- [Note template](artifact/references/note-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown notes and feedback with JSON learning-state records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent local knowledge files, question-bank entries, mastery status updates, and review schedules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
