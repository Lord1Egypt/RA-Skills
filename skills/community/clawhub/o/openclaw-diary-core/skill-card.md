## Description: <br>
An OpenClaw journaling assistant that records user thoughts, article discussions, and collaboration notes into timeline-based diary entries with configurable local storage and optional sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smorzandos](https://clawhub.ai/user/smorzandos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to preserve personal journal entries, article-reading notes, and AI collaboration decisions as Markdown records. It supports configurable journaling style, local monthly files, and optional Feishu sync when credentials are provided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates durable records of personal journal content, which may include sensitive user thoughts, article notes, and collaboration history. <br>
Mitigation: Review the configured local diary path before use and avoid sharing prompts or entries that should not be persisted. <br>
Risk: User identity loading can personalize diary behavior from profile files. <br>
Mitigation: Disable user_identity in the configuration if profile-based personalization is not desired. <br>
Risk: Optional third-party sync can store diary entries in an external service. <br>
Mitigation: Keep Feishu, Flomo, or Notion sync disabled unless the user accepts the privacy implications and has reviewed the destination configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smorzandos/openclaw-diary-core) <br>
- [Project Homepage](https://github.com/openclaw-community/diary-system) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diary entries with brief user-facing status messages and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append entries to local Markdown diary files and, when configured, synchronize content to Feishu documents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
