## Description: <br>
my study pal is a Chinese study assistant for adults that explains unfamiliar concepts, terms, abbreviations, and distinctions, then can maintain local study records and user preferences in a mystudy workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivanyqw](https://clawhub.ai/user/ivanyqw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to get concise Chinese explanations of unfamiliar concepts, terms, abbreviations, and similar-concept distinctions. It can also initialize and maintain local study summaries, topic detail records, and long-term learning preferences for later sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to automatically save learning conversations and user profile details in local files, which may surprise users or capture sensitive context. <br>
Mitigation: Install and use it only when local recording is acceptable; avoid sensitive personal, workplace-confidential, medical, legal, financial, or credential-related explanations unless recording is constrained or disabled. <br>
Risk: Saved study records and preferences may persist longer than the user expects in the workspace. <br>
Mitigation: Periodically review, edit, or delete the files under mystudy/ and confirm that recorded topics and preferences remain appropriate for reuse. <br>


## Reference(s): <br>
- [Setup - my-study-pal](setup.md) <br>
- [Filesystem Blueprint](references/blueprint.md) <br>
- [Study Storage Specification](references/study-storage.md) <br>
- [Recording Rules](references/recording-rules.md) <br>
- [Response Contract](references/response-contract.md) <br>
- [Direct Teaching Method](references/method-direct.md) <br>
- [Expository Teaching Method](references/method-expository.md) <br>
- [Guided Teaching Method](references/method-guided.md) <br>
- [Contrastive Teaching Method](references/method-contrastive.md) <br>
- [Applied Teaching Method](references/method-applied.md) <br>
- [Retention Teaching Method](references/method-retention.md) <br>
- [Style Analysis](references/style-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and local Markdown files, with optional shell commands for workspace initialization and profile refresh] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local mystudy/ folder containing study summaries, topic detail records, user-profile preferences, and a runtime-profile cache.] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
