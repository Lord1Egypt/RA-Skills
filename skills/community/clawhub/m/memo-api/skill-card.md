## Description: <br>
MaiMemo Open API skill for vocabulary learning workflows, including vocabulary lookup, custom definitions, mnemonics, word lists, example sentences, study progress, review schedules, and study records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[celend](https://clawhub.ai/user/celend) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to guide authenticated MaiMemo Open API calls for managing vocabulary learning content and study data. It helps resolve vocabulary IDs, prepare curl requests, and choose the correct endpoint and request body for read, create, update, delete, bulk-add, export, and review-advance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user-provided MaiMemo Open API token that can grant access to vocabulary and study data. <br>
Mitigation: Keep MAIMEMO_TOKEN out of shared logs and transcripts, pass it through the environment, and avoid exposing Authorization headers. <br>
Risk: The skill can guide delete, export, bulk add, and review-advance operations that may change or expose user study data. <br>
Mitigation: Require an explicit preview and user confirmation before destructive, bulk, export, or review-advance operations. <br>
Risk: Study endpoints are documented as beta and may depend on automatic sync and app initialization. <br>
Mitigation: Tell users when beta study results may be incomplete or unavailable, and verify critical study data in MaiMemo before relying on it. <br>


## Reference(s): <br>
- [ClawHub Memo Api Skill Page](https://clawhub.ai/celend/memo-api) <br>
- [MaiMemo Open API Base URL](https://open.maimemo.com/open/api/v1) <br>
- [Vocabulary API](references/vocabulary-api.md) <br>
- [Interpretations API](references/interpretations-api.md) <br>
- [Notes API](references/notes-api.md) <br>
- [Notepads API](references/notepads-api.md) <br>
- [Phrases API](references/phrases-api.md) <br>
- [Study API](references/study-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON request or response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MAIMEMO_TOKEN from the environment and guides calls against the MaiMemo Open API.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
