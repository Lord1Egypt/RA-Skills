## Description: <br>
Learning Cards is a spaced-repetition flashcard skill backed by Feishu Bitable that creates cards from books or knowledge bases, quizzes the user, tracks progress, and schedules reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqunabc](https://clawhub.ai/user/guoqunabc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners, knowledge workers, and educators use this skill to turn books, courses, or documents into Feishu-backed flashcards and run interactive review sessions that update progress and scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and updates Feishu Bitable records, so using the wrong table could alter unrelated learning data. <br>
Mitigation: Confirm the target Feishu Bitable app and table before starting a study session or creating cards. <br>
Risk: Flashcards may contain confidential or sensitive study material stored in a Feishu workspace. <br>
Mitigation: Use only Feishu tables with permissions appropriate for the material being studied. <br>


## Reference(s): <br>
- [Learning Cards ClawHub Page](https://clawhub.ai/guoqunabc/learning-cards) <br>
- [System Design](references/system-design.md) <br>
- [OpenClaw Feishu Setup](https://docs.openclaw.ai/channels/feishu) <br>
- [Feishu Bitable API Documentation](https://open.feishu.cn/document/server-docs/docs/bitable-v1) <br>
- [The Eighty Five Percent Rule for Optimal Learning](https://doi.org/10.1038/s41467-019-12552-4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Conversational Markdown and plain text with Feishu Bitable setup fields, quiz prompts, progress summaries, and card-generation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update Feishu Bitable records through the configured OpenClaw Feishu plugin.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
