## Description:

Huanling Skill Zhihu lets an agent speak as Huanling, the authorial voice of AI Linghun De Bianjie, to answer book-related reader questions, prepare reader interview material, and draft chapter release notes while refusing unrelated topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-innopower](https://clawhub.ai/user/ai-innopower)

### License/Terms of Use:

MIT-0

## Use Case:

External readers and content operators use this skill to discuss AI Linghun De Bianjie, generate structured reader interview questions and follow-ups, and draft concise Zhihu chapter announcements in the book's voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a strong book-specific persona and asks reader profiling questions.

Mitigation: Review the persona boundaries and profiling prompts before deployment, and use it only where book-focused reader interaction is appropriate.

Risk: The optional voice workflow may require installing and running third-party Python code.

Mitigation: Do not enable voice until the package, script behavior, external data flow, and retention behavior are clarified and approved.

Risk: Broad activation terms may trigger the skill in conversations that only loosely mention the book or Zhihu activity.

Mitigation: Require clear user intent for activation and verify that unrelated topics are refused or left unanswered as documented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-innopower/skills/huanling-skill-zhihu)
- [Skill definition](artifact/SKILL.md)
- [Installation guide](artifact/焕灵Skill-知乎内测版-安装说明.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style conversational text with optional inline shell commands and configuration guidance for voice setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are constrained to the book topic, short-form reader dialogue, interview drafts, chapter notes, and optional local voice setup guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter states 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
