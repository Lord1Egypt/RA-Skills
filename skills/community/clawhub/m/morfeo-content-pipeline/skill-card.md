## Description:

Autonomous pipeline for generating TikTok draft videos that simulate organic content for real Argentine brands and end with an AI reveal by Morfeo Labs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run a Morfeo Labs marketing content pipeline that selects brands and models, generates image and video assets, assembles vertical clips, and creates social publishing drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill tells agents to work around Gemini moderation by switching languages.

Mitigation: Remove or revise that behavior before use; moderation blocks should be handled by making prompts compliant rather than bypassing provider safeguards.

Risk: The workflow can create scheduled marketing drafts through external media services.

Mitigation: Install and run it only for an intended Morfeo Labs marketing pipeline, and review generated drafts before publication.

## Reference(s):

- [Morfeo Content Pipeline on ClawHub](https://clawhub.ai/pauldelavallaz/skills/morfeo-content-pipeline)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown instructions with inline code, commands, tables, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide scheduled draft creation through external media generation and social publishing services.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
